@echo off
color 0A
cls

echo ===============================
echo 🚀 ARRANQUE DE SERVICIOS
echo ===============================

REM Ruta base (IMPORTANTE con comillas)
set "BASE_DIR=%~dp0.."

REM ===============================
REM 1. MEMGRAPH
REM ===============================
echo.
echo 🧠 Iniciando Memgraph...

docker start memgraph-mage >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo 🔄 Contenedor no existe, creando...
    docker run -d --name memgraph-mage -p 7687:7687 memgraph/memgraph-mage
) ELSE (
    echo ✅ Memgraph ya estaba iniciado
)

echo ⏳ Esperando a Memgraph...
timeout /t 5 >nul


REM ===============================
REM 2. ENTORNO VIRTUAL
REM ===============================
echo.
echo 🧪 Activando entorno virtual...

call "%BASE_DIR%\venv\Scripts\activate.bat"

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Error activando el entorno virtual
    pause
    exit /b
)

echo ✅ Entorno activado

REM ===============================
REM 3. ETL
REM ===============================
echo.
echo 📊 Ejecutando ETL...

cd /d "%BASE_DIR%\db\memgraph"

type init.cypher | docker exec -i memgraph-mage mgconsole

IF %ERRORLEVEL% NEQ 0 (
    echo Error ejecutando init.cypher
    pause
    exit /b
)

cd /d "%BASE_DIR%\etl"

python importGeoJson_Memgraph.py

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Error en ETL
    pause
    exit /b
)

python importGeoJson_CouchDB.py

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Error en ETL
    pause
    exit /b
)

cd /d "%BASE_DIR%"


REM ===============================
REM 4. BACKEND
REM ===============================
echo.
echo 🌐 Iniciando FastAPI...

cd /d "%BASE_DIR%\backend"

start cmd /k "%BASE_DIR%\script\backend_memgraph.bat"
start cmd /k "%BASE_DIR%\script\backend_couchdb.bat"

echo ⏳ Esperando backend...
timeout /t 5 >nul

echo.
echo ===============================
echo ✅ TODO LISTO
echo ===============================

echo 📍 API: http://127.0.0.1:8000
echo 📍 Docs: http://127.0.0.1:8000/docs

pause