@echo off
color 0B

REM Ruta base del proyecto
set "BASE_DIR=%~dp0.."

REM Ir a backend (ROOT DEL PROYECTO PYTHON)
cd /d "%BASE_DIR%\backend\microservicio_couchdb"

echo Activando entorno...
call "%BASE_DIR%\venv\Scripts\activate.bat"

echo Configurando PYTHONPATH...
set PYTHONPATH=%CD%

echo Iniciando FastAPI...
uvicorn main:app --reload --port 8001 

pause