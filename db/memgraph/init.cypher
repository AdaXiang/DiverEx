// ======================================
// LIMPIEZA DE DATOS (NO INDICE/REGLAS)
// ======================================
MATCH (n) DETACH DELETE n;;

// ======================================
// REGLAS
// ======================================
// Usuario
CREATE CONSTRAINT ON (u:Usuario) ASSERT u.id IS UNIQUE;
CREATE CONSTRAINT ON (u:Usuario) ASSERT u.email IS UNIQUE;

// Lugar
CREATE CONSTRAINT ON (l:Lugar) ASSERT l.id IS UNIQUE;

// Comentario
CREATE CONSTRAINT ON (c:Comentario) ASSERT c.id IS UNIQUE;

// ======================================
// ÍNDICES
// ======================================
// Usuario
CREATE INDEX ON :Usuario(id);

// Lugar 
CREATE INDEX ON :Lugar(id);
CREATE INDEX ON :Lugar(name);
CREATE INDEX ON :Lugar(codigo_municipio);

// Comentario
CREATE INDEX ON :Comentario(id);

// ======================================
// LOG DE CREACION 
// ======================================
SHOW INDEX INFO;
SHOW CONSTRAINT INFO;

// ======================================
// FIN 
// ======================================¡
RETURN "FIN SCRIPT" AS msg; 