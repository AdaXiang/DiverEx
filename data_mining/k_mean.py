# =========================================================
# K-MEANS DE LUGARES
# Couchbase + Memgraph + Python
# =========================================================
#
# OBJETIVO:
# Agrupar lugares similares usando:
# - geolocalización
# - likes
# - media
# - características del lugar
# =========================================================

# =========================================================
# LIBRERÍAS
# =========================================================

from pathlib import Path

import numpy as np

import os
import requests
import pandas as pd

# Couchbase
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Memgraph
from neo4j import GraphDatabase

# Machine Learning
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Visualización
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# CONFIGURACIÓN
# =========================================================
# ---------- COUCHBASE ----------
load_dotenv()

COUCHBASE_HOST = os.getenv("COUCHBASE_HOST")
COUCHBASE_USER = os.getenv("COUCHBASE_USER")
COUCHBASE_PASSWORD = os.getenv("COUCHBASE_PASSWORD")
COUCHBASE_BUCKET = os.getenv("COUCHBASE_BUCKET")
COUCHBASE_KV_PORT= os.getenv("COUCHBASE_KV_PORT")
COUCHBASE_API_PORT= os.getenv("COUCHBASE_API_PORT")

# Auth HTTP
auth = HTTPBasicAuth(
    COUCHBASE_USER,
    COUCHBASE_PASSWORD
)

# ---------- MEMGRAPH ----------

MEMGRAPH_HOST = os.getenv("MEMGRAPH_HOST")
MEMGRAPH_PORT = os.getenv("MEMGRAPH_PORT")
MEMGRAPH_URL = os.getenv(
    "MEMGRAPH_URL",
    f"bolt://{MEMGRAPH_HOST}:{MEMGRAPH_PORT}"
)


# =========================================================
# EXTRAER DATOS DE COUCHBASE
# =========================================================

print("\nExtrayendo datos desde Couchbase...")

# Endpoint N1QL
query_url = f"http://{COUCHBASE_HOST}:{COUCHBASE_API_PORT}/query/service"

# =========================================================
# QUERY N1QL
# =========================================================
query_couchbase = f"""
SELECT
    META().id AS document_id,
    
    _id,
    
    tipo_lugar,
    properties.acceso_silla_ruedas,
    properties.estado,
    
    properties.superficie_aire,
    properties.superficie_cubierta,

    geo_point.coordinates[0] AS longitud,
    geo_point.coordinates[1] AS latitud

FROM `{COUCHBASE_BUCKET}`

WHERE geo_point IS NOT NULL
"""

# =========================================================
# EJECUTAR QUERY
# =========================================================

response = requests.post(
    query_url,
    auth=auth,
    headers={
        "Content-Type": "application/json"
    },
    json={
        "statement": query_couchbase
    }
)

# =========================================================
# VALIDACIÓN
# =========================================================

if response.status_code != 200:
    print("❌ Error ejecutando query N1QL")
    print(response.text)
    exit()

# =========================================================
# PARSEAR RESULTADOS
# =========================================================

data = response.json()

rows = data.get("results", [])

df_couchbase = pd.DataFrame(rows)

# =========================================================
# RESULTADOS
# =========================================================

print(f"\n✅ Lugares obtenidos: {len(df_couchbase)}")
print("\nPrimeros registros:\n")
print(df_couchbase.head())

# =========================================================
# CONEXIÓN A MEMGRAPH
# =========================================================

print("\nConectando a Memgraph...")

driver = GraphDatabase.driver(MEMGRAPH_URL)

print("Conexión Memgraph OK")

# =========================================================
# FUNCIÓN PARA EJECUTAR QUERIES
# =========================================================

def run_query(query, params=None):

    with driver.session() as session:

        result = session.run(
            query,
            params or {}
        )

        return [record.data() for record in result]

# =========================================================
# EXTRAER DATOS DE MEMGRAPH
# =========================================================

print("\nExtrayendo datos de Memgraph...")

query_memgraph = """
MATCH (p:Lugar)

RETURN
    p.id AS place_id,
    p.likes AS likes,
    p.media AS media
"""

memgraph_data = run_query(query_memgraph)

df_memgraph = pd.DataFrame(memgraph_data)

print(f"\n✅ Lugares obtenidos: {len(df_memgraph)}")

print("\nPrimeros registros:\n")

print(df_memgraph.head())

# =========================================================
# MERGE DE DATOS
# =========================================================

print("\nUniendo datasets...")

# IMPORTANTE:
# _id de Couchbase == place_id de Memgraph

df = pd.merge(
    df_couchbase,
    df_memgraph,
    left_on="_id",
    right_on="place_id",
    how="inner"
)

print(f"Dataset final: {len(df)} lugares")

# =========================================================
# LIMPIEZA DE DATOS
# =========================================================

print("\nPreparando datos...")

# Convertir booleanos a enteros

boolean_columns = [
    "acceso_silla_ruedas"
]

for col in boolean_columns:
    if col in df.columns:
        df[col] = df[col].fillna(False).astype(int)
        
# =========================================================
# CONVERSIÓN A NUMÉRICOS
# =========================================================

numeric_columns = [
    "likes",
    "media",
    "superficie_aire",
    "superficie_cubierta",
    "latitud",
    "longitud"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )
    
# =========================================================
# LIMPIEZA DE NULOS
# =========================================================

df = df.dropna(
    subset=[
        "latitud",
        "longitud"
    ]
)

df = df.fillna(0)

# =========================================================
# ONE HOT ENCODING
# =========================================================

df = pd.get_dummies(
    df,
    columns=[
        "tipo_lugar",
        "estado"
    ]
)

# =========================================================
# FEATURES PARA K-MEANS
# =========================================================
features = [
    "acceso_silla_ruedas",

    "superficie_aire",
    "superficie_cubierta",

    "latitud",
    "longitud",

    "likes",
    "media"
]

# Añadir columnas one-hot automáticamente

features += [
    col for col in df.columns
    if col.startswith("tipo_lugar_")
]

features += [
    col for col in df.columns
    if col.startswith("estado_")
]

X = df[features]

# =========================================================
# NORMALIZACIÓN
# =========================================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================================================
# MÉTODO DEL CODO
# =========================================================

inertia_values = []

K_range = range(1, 30)

for k in K_range:
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    inertia_values.append(model.inertia_)

# Gráfica

plt.figure(figsize=(8, 5))

plt.plot(
    K_range,
    inertia_values,
    marker="o"
)

plt.title("Método del Codo")
plt.xlabel("Número de clusters (k)")
plt.ylabel("Inercia")

plt.grid(True)

plt.show()

# =========================================================
# K-MEANS
# =========================================================

print("\nEjecutando K-Means...")
k = 15 #segun el metodo del codo
kmeans = KMeans(
    n_clusters=k,
    random_state=42,
    n_init=10
)

df["cluster"] = kmeans.fit_predict(X_scaled)
print("K-Means completado")

# =========================================================
# RESULTADOS
# =========================================================

print("\nRESULTADOS DEL CLUSTERING\n")
print(
    df[
        [
            "_id",
            "likes",
            "media",
            "cluster"
        ]
    ].head(20)
)

# =========================================================
# VISUALIZACIÓN 1
# MAPA DE CLUSTERS
# =========================================================

print("\nGenerando visualización...")

plt.figure(figsize=(12, 8))

# Colores discretos
colors = plt.cm.viridis(np.linspace(0, 1, k))

# Dibujar cada cluster por separado
for cluster_id in range(k):

    cluster_data = df[df["cluster"] == cluster_id]

    plt.scatter(
        cluster_data["longitud"],
        cluster_data["latitud"],
        s=60,
        color=colors[cluster_id],
        label=f"Cluster {cluster_id}"
    )

plt.title("Clusters de lugares - K-Means")

plt.xlabel("Longitud")
plt.ylabel("Latitud")

# Leyenda categórica
plt.legend()

plt.grid(True)

plt.show()

# =========================================================
# VISUALIZACIÓN 2
# LIKES POR CLUSTER
# =========================================================

plt.figure(figsize=(10, 6))

df.groupby("cluster")["likes"].mean().plot(
    kind="bar"
)

plt.title("Media de likes por cluster")
plt.xlabel("Cluster")
plt.ylabel("Likes medios")

plt.grid(True)

plt.show()

# =========================================================
# CENTROIDES
# =========================================================

print("\nCENTROIDES:\n")

centroides = pd.DataFrame(
    scaler.inverse_transform(kmeans.cluster_centers_),
    columns=features
)

print(centroides)

# =========================================================
# VISUALIZACIÓN 3: HEATMAP DE CENTROIDES TOP
# COINCIDENCIAS Y MOTIVOS DE SU ÉXITO
# =========================================================
print("\nGenerando visualización 3 (Heatmap de Centroides Top)...")

# 1. Encontrar cuáles son los 5 clusters con más likes promedio
top_clusters_indices = df.groupby("cluster")["likes"].mean().nlargest(5).index
print(f"-> Clusters analizados en el Heatmap por su alto rendimiento: {list(top_clusters_indices)}")

# 2. Extraer los centroides ESCALADOS correspondientes a esos grupos.
# Usamos los escalados porque permiten comparar 'likes' (0-100) con 'acceso_silla_ruedas' (0-1) bajo la misma métrica (Z-score).
centroides_escalados = pd.DataFrame(kmeans.cluster_centers_, columns=features)
top_centroides = centroides_escalados.loc[top_clusters_indices]
top_centroides.index = [f"Cluster {c}" for c in top_clusters_indices]

# 3. Filtrar solo las métricas más interesantes para que el gráfico sea muy legible
# (Ignoramos algunas columnas One-Hot secundarias para enfocarnos en la raíz del éxito)
columnas_interes = ["likes", "media", "acceso_silla_ruedas", "superficie_aire", "superficie_cubierta"]
# Añadimos las variables de tipo de lugar que tengan presencia real
columnas_interes += [col for col in features if col.startswith("tipo_lugar_") or col.startswith("estado_")][:5]

plt.figure(figsize=(12, 6))
# Usamos un mapa de calor divergente (Coolwarm) centrado en 0.
# Rojo = Característica muy por ENCIMA de la media global.
# Azul = Característica muy por DEBAJO de la media global.
sns.heatmap(top_centroides[columnas_interes], annot=True, cmap="coolwarm", center=0, fmt=".2f", linewidths=0.5)

plt.title("¿Por qué tienen éxito? - Características Distintivas de los Clusters Top", fontsize=14, pad=15)
plt.ylabel("Clusters con más Likes")
plt.xlabel("Características (Valores Z-Score / Escalados)")
plt.tight_layout()
plt.show()

# =========================================================
# CENTROIDES REALES (VALORES ORIGINALES)
# =========================================================
print("\nCENTROIDES EN VALORES REALES:\n")
centroides_reales = pd.DataFrame(
    scaler.inverse_transform(kmeans.cluster_centers_),
    columns=features
)
# Mostramos solo los relevantes para tu análisis de negocio
print(centroides_reales.loc[top_clusters_indices, ["likes", "media", "acceso_silla_ruedas", "superficie_cubierta"]])

# Exportar resultados
base_dir = Path(__file__).resolve().parent
output_dir = (base_dir / "../backend/microservicio_couchdb").resolve()
df.to_csv(output_dir /"clusters_lugares.csv", index=False)
print("\nProceso finalizado correctamente. Archivo 'clusters_lugares_v2.csv' guardado.")

# =========================================================
# EXPORTAR RESULTADOS
# =========================================================

df.to_csv(
    "clusters_lugares.csv",
    index=False
)

print("\nArchivo exportado:")
print("clusters_lugares.csv")

print("\nProceso finalizado correctamente")