# 🚀 DiverEx v1

## 📍 Descripción

**DiverEx v1** es una aplicación web centrada en la exploración de lugares de interés dentro de la provincia de Badajoz.  
La plataforma permite descubrir ubicaciones turísticas, culturales y naturales mediante sistemas de geolocalización, recomendaciones inteligentes y análisis de similitud entre lugares.

La aplicación puede utilizarse sin necesidad de iniciar sesión, aunque los usuarios registrados disponen de funcionalidades avanzadas de interacción social.

---

# ✨ Características principales

## 🔓 Uso sin autenticación
- Navegación libre por los lugares de interés.
- Consulta de información de los lugares.
- Visualización en mapas interactivos.

## 👤 Funcionalidades para usuarios registrados
- ✅ Marcar lugares como visitados.
- ❤️ Dar “Me gusta” a lugares.
- ⭐ Añadir lugares a favoritos.
- 💬 Comentar lugares.

A partir de estas interacciones se generan:
- 📊 Medias de valoración.
- 👍 Conteo de likes.
- 📈 Métricas de popularidad.

---

# 🌍 Funcionalidades avanzadas

## 📌 Geolocalización
La aplicación incorpora filtros geoespaciales para encontrar lugares cercanos o dentro de zonas específicas.

## 🎯 Sistema de recomendación
DiverEx implementa recomendaciones basadas en:
- Gustos similares entre usuarios.
- Interacciones previas.
- Preferencias compartidas.

## 🧠 Lugares similares mediante clustering
Los lugares similares son calculados mediante técnicas de clustering y minería de datos para ofrecer recomendaciones relacionadas.

---

# 🛠️ Tecnologías utilizadas

## Backend
- Python
- FastAPI

## Bases de datos
- Memgraph
- CouchBase

## Frontend
- React
- JavaScript
- Leaflet

---

# 🏗️ Arquitectura del proyecto

La arquitectura de DiverEx se basa en un flujo ETL construido a partir de archivos GeoJSON.

```text
GeoJSON → Procesos ETL → Memgraph + CouchBase → Servicios Backend → Frontend React
```

## Flujo de trabajo

1. Extracción de datos desde archivos GeoJSON.
2. Transformación y limpieza mediante procesos ETL.
3. Inserción de datos en:
   - Memgraph
   - CouchBase
4. Exposición de servicios backend independientes:
   - Servicio para Memgraph.
   - Servicio para CouchBase.
5. Integración de ambos servicios dentro del frontend React.

---

# ⚙️ Instalación y puesta en marcha

# 1️⃣ Iniciar CouchBase

Ejecutar el contenedor Docker:

```bash
docker run -d --name couchbase -p 8091-8097:8091-8097 -p 11210:11210 couchbase
```

Abrir:

```text
http://localhost:8091/
```

## Configuración inicial
- Crear Server:
  - Todo por defecto
  - Nombre: `DiverEx`

- Crear Bucket:
  - Nombre recomendado: `places`

- Crear usuario en Security:
  - Usuario: `admin`
  - Contraseña: `admin123`
  - Permisos: `Full Admin`

---

# 🌍 Creación de índice geoespacial

```json
{
 "name": "idx_geo",
 "type": "fulltext-index",
 "params": {
  "doc_config": {
   "docid_prefix_delim": "",
   "docid_regexp": "",
   "mode": "type_field",
   "type_field": "type"
  },
  "mapping": {
   "default_analyzer": "standard",
   "default_datetime_parser": "dateTimeOptional",
   "default_field": "_all",
   "default_mapping": {
    "dynamic": false,
    "enabled": true,
    "properties": {
     "geo_point": {
      "dynamic": false,
      "enabled": true,
      "properties": {
       "coordinates": {
        "enabled": true,
        "dynamic": false,
        "fields": [
         {
          "index": true,
          "name": "coordinates",
          "type": "geopoint"
         }
        ]
       }
      }
     }
    }
   },
   "default_type": "_default",
   "docvalues_dynamic": false,
   "index_dynamic": false,
   "scoring_model": "tf-idf",
   "store_dynamic": false,
   "type_field": "_type"
  },
  "store": {
   "indexType": "scorch",
   "segmentVersion": 16,
   "spatialPlugin": "s2"
  }
 },
 "sourceType": "gocbcore",
 "sourceName": "places",
 "sourceUUID": "db47ef5d7c0283ad1eabef799a62271e",
 "sourceParams": {},
 "planParams": {
  "maxPartitionsPerPIndex": 128,
  "indexPartitions": 1,
  "numReplicas": 0
 },
 "uuid": "550c8ae9fa8fcb83"
}
```

---

# 📑 Creación de índices comunes

```sql
CREATE PRIMARY INDEX ON `places`;

CREATE INDEX idx_tipo_estado
ON `places`(tipo_lugar, properties.estado);

CREATE INDEX idx_municipio
ON `places`(properties.municipio_nombre);

CREATE INDEX idx_nombre
ON `places`(properties.nombre);
```

---

# 🧠 Instalación de Memgraph

Ejecutar:

```powershell
iwr https://windows.memgraph.com | iex
```

---

# ▶️ Ejecución de servicios

Ir a la carpeta:

```text
script
```

Ejecutar:

```bash
start_services.bat
```

## ¿Qué hace este script?

- Prepara el entorno virtual.
- Instala dependencias necesarias.
- Ejecuta los ETL de:
  - CouchBase
  - Memgraph
- Limpia y prepara las bases de datos.
- Lanza automáticamente:
  - `backend_couchdb.bat`
  - `backend_memgraph.bat`

---

# 💻 Lanzamiento del Frontend

Ir a la carpeta:

```text
frontend_diverEx
```

Ejecutar:

```bash
npm install
```

Posteriormente:

```bash
npm start
```

---

# ℹ️ Información importante

## 🔁 Reutilización de ETL
Una vez ejecutados los ETL por primera vez, los servicios pueden iniciarse posteriormente sin necesidad de volver a procesar los datos.

## 🖥️ Recomendación
Se recomienda lanzar los scripts desde terminal y no desde entornos gráficos.

## 🧠 Actualización del clustering
Si desea recalcular los lugares similares o modificar el clustering:

- Acceder a la carpeta:

```text
data_mining
```

- Ejecutar el archivo `.py` correspondiente.

---

# 📷 Funcionalidades visuales

- Mapas interactivos con Leaflet.
- Visualización geoespacial.
- Filtros dinámicos.
- Recomendaciones inteligentes.
- Exploración de lugares similares.

---

# 👨‍💻 Creadores

- Manuel Solis Gomez
- Ada Xiang Ramos Grano de Oro

---

# 📄 Licencia

Proyecto académico y experimental desarrollado con fines educativos y de investigación.
