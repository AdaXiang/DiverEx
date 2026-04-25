// ======================================
// CONSULTAS BASE USUARIO 1
// ======================================

// Favoritos del usuario 1
RETURN "⭐ Favoritos del usuario 1";
MATCH (u:Usuario {id: "1"})-[:FAVORITO]->(l:Lugar)
RETURN l.name
LIMIT 10;

// Lugares que le gustan al usuario 1
RETURN "👍 Lugares que le gustan al usuario 1";
MATCH (u:Usuario {id: "1"})-[:ME_GUSTA]->(l:Lugar)
RETURN l.name
LIMIT 10;

// Lugares visitados por el usuario 1
RETURN "📍 Lugares visitados por el usuario 1";
MATCH (u:Usuario {id: "1"})-[:VISITA]->(l:Lugar)
RETURN l.name
LIMIT 10;

// Comentarios del usuario 1
RETURN "💬 Comentarios del usuario 1";
MATCH (u:Usuario {id: "1"})-[:ESCRIBE]->(c:Comentario)-[:SOBRE]->(l:Lugar)
RETURN c, l.name
LIMIT 10;


// ======================================
// RECOMENDACIONES
// ======================================

// Recomendación básica
RETURN "🤖 Recomendaciones basadas en usuarios similares";
MATCH (u:Usuario {id: "1"})-[:VISITA]->(l:Lugar)<-[:VISITA]-(other:Usuario)
MATCH (other)-[:VISITA]->(rec:Lugar)
WHERE NOT (u)-[:VISITA]->(rec)
RETURN DISTINCT rec
LIMIT 20;

// Recomendación filtrada
RETURN "♿ Recomendaciones accesibles y en buen estado";
MATCH (u:Usuario {id: "1"})-[:VISITA]->(l:Lugar)<-[:VISITA]-(other:Usuario)
MATCH (other)-[:VISITA]->(rec:Lugar)
WHERE NOT (u)-[:VISITA]->(rec)
  AND rec.estado = "B"
  AND rec.acceso_silla_ruedas = true
RETURN DISTINCT rec
LIMIT 20;


// ======================================
// EXPERIENCIA USUARIO
// ======================================

// Visitados pero no comentados
RETURN "📝 Lugares visitados sin comentar";
MATCH (u:Usuario {id: "1"})-[:VISITA]->(l:Lugar)
WHERE NOT EXISTS {
    MATCH (u)-[:ESCRIBE]->(:Comentario)-[:SOBRE]->(l)
}
RETURN l
LIMIT 10;


// ======================================
// ANALÍTICA
// ======================================

// Media de ranking por lugar
RETURN "⭐ Media de valoraciones por lugar";
MATCH (l:Lugar)<-[:SOBRE]-(c:Comentario)
RETURN l.name AS lugar,
       AVG(c.ranking) AS media
ORDER BY media DESC
LIMIT 10;

// Lugares más visitados
RETURN "🔥 Lugares más visitados";
MATCH (:Usuario)-[r:VISITA]->(l:Lugar)
RETURN l.name AS lugar,
       count(r) AS visitas
ORDER BY visitas DESC
LIMIT 10;

// Lugares más favoritos
RETURN "💖 Lugares más favoritos";
MATCH (:Usuario)-[r:FAVORITO]->(l:Lugar)
RETURN l.name AS lugar,
       count(r) AS favoritos
ORDER BY favoritos DESC
LIMIT 10;

// Usuarios más activos
RETURN "🧍 Usuarios más activos";
MATCH (u:Usuario)-[r]->()
RETURN u.id AS usuario,
       count(r) AS interacciones
ORDER BY interacciones DESC
LIMIT 10;


// ======================================
// SIMILITUD Y RECOMENDACIÓN AVANZADA
// ======================================

// Lugares similares
RETURN "🧠 Lugares similares";
MATCH (l:Lugar {id: "lonjas_1"})
MATCH (similar:Lugar)
WHERE similar.codigo_municipio = l.codigo_municipio
  AND similar.tipo = l.tipo
  AND similar.id <> l.id
RETURN similar
LIMIT 10;

// Recomendación híbrida
RETURN "🚀 Recomendación híbrida";
MATCH (u:Usuario {id: "1"})
MATCH (u)-[:VISITA]->(l:Lugar)

MATCH (rec:Lugar)
WHERE rec.codigo_municipio = l.codigo_municipio
  AND NOT (u)-[:VISITA]->(rec)

OPTIONAL MATCH (rec)<-[v:VISITA]-()
WITH rec, count(v) AS popularidad
RETURN rec.name AS lugar,
       popularidad
ORDER BY popularidad DESC
LIMIT 10;


// ======================================
// EXTRAS INTERESANTES
// ======================================

// Usuarios similares
RETURN "👥 Usuarios similares";
MATCH (u1:Usuario {id:"1"})-[:VISITA]->(l)<-[:VISITA]-(u2:Usuario)
RETURN u2.id AS usuario,
       count(l) AS coincidencias
ORDER BY coincidencias DESC
LIMIT 10;

// Lugares sin visitas
RETURN "💤 Lugares sin visitas";
MATCH (l:Lugar)
WHERE NOT (l)<-[:VISITA]-()
RETURN l
LIMIT 10;

// Mejores lugares (mínimo 3 votos)
RETURN "🏆 Mejores lugares (mínimo 3 votos)";
MATCH (l:Lugar)<-[:SOBRE]-(c:Comentario)
WITH l, AVG(c.ranking) AS media, count(c) AS votos
WHERE votos >= 3
RETURN l.name AS lugar,
       media,
       votos
ORDER BY media DESC
LIMIT 10;