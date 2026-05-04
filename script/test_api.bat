@echo off
color 0E
cls

echo ===============================
echo 🧪 TEST API DIVEREX
echo ===============================

set BASE_URL=http://127.0.0.1:8000

REM ===============================
REM 1. CREAR USUARIO
REM ===============================
echo.
echo 👤 Crear usuario...

curl -X POST %BASE_URL%/usuarios/signup ^
-H "Content-Type: application/json" ^
-d "{\"id\":\"1\",\"name\":\"Manuel\",\"email\":\"manuel@test.com\"}"

pause

REM ===============================
REM 2. CREAR LUGAR
REM ===============================
echo.
echo 📍 Crear lugar (Parque)...

curl -X POST %BASE_URL%/lugares ^
-H "Content-Type: application/json" ^
-d "{\"tipo\":\"Parque\",\"name\":\"Parque Central\",\"codigo\":\"06001\",\"estado\":\"activo\",\"accesible\":true,\"tipo_detalle\":\"urbano\",\"agua\":true,\"electricidad\":true,\"comedor\":false,\"juegos\":true}"

pause

REM ===============================
REM 3. OBTENER LUGARES
REM ===============================
echo.
echo 📍 Obtener todos los lugares...

curl %BASE_URL%/lugares

pause

REM ===============================
REM 4. FAVORITO
REM ===============================
echo.
echo ⭐ Añadir favorito...

curl -X POST %BASE_URL%/favoritos ^
-H "Content-Type: application/json" ^
-d "{\"user_id\":\"1\",\"lugar_id\":\"parques_1\"}"

pause

REM ===============================
REM 5. VISITA
REM ===============================
echo.
echo 👣 Marcar visita...

curl -X POST %BASE_URL%/visitas ^
-H "Content-Type: application/json" ^
-d "{\"user_id\":\"1\",\"lugar_id\":\"parques_1\"}"

pause

REM ===============================
REM 6. ME GUSTA
REM ===============================
echo.
echo ❤️ Dar like...

curl -X POST %BASE_URL%/likes ^
-H "Content-Type: application/json" ^
-d "{\"user_id\":\"1\",\"lugar_id\":\"parques_1\"}"

pause

REM ===============================
REM 7. COMENTARIO
REM ===============================
echo.
echo 💬 Crear comentario...

curl -X POST %BASE_URL%/comentarios ^
-H "Content-Type: application/json" ^
-d "{\"user_id\":\"1\",\"lugar_id\":\"parques_1\",\"mensaje\":\"Muy buen sitio\",\"ranking\":5}"

pause

REM ===============================
REM 8. COMENTARIOS DEL LUGAR
REM ===============================
echo.
echo 💬 Ver comentarios del lugar...

curl %BASE_URL%/comentarios/lugar/Parque_1

pause

REM ===============================
REM 9. TOP LUGARES
REM ===============================
echo.
echo 🏆 Top lugares...

curl "%BASE_URL%/preferencias/top?codigo_municipio=018&tipo=Parque"

pause

REM ===============================
REM 10. RECOMENDACIONES
REM ===============================
echo.
echo 🤖 Recomendaciones...

curl %BASE_URL%/preferencias/recomendaciones/1

pause

echo.
echo ===============================
echo ✅ TEST COMPLETADO
echo ===============================

pause