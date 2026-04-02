@echo off
chcp 65001 > NUL
title Dashboard T'Elefan - SAE QLIO

echo.
echo  ================================================
echo        Dashboard MES4 T'Elefan - QLIO G8
echo  ================================================
echo.

:: Vérification que Docker est installé et lancé
docker info > NUL 2>&1
if %errorlevel% neq 0 (
    echo  [ERREUR] Docker n'est pas lance.
    echo  Veuillez demarrer Docker Desktop puis relancer ce fichier.
    echo.
    pause
    exit /b 1
)

echo  [1/3] Demarrage des services Docker...
docker compose up -d --build > NUL 2>&1
if %errorlevel% neq 0 (
    echo  [ERREUR] Impossible de demarrer les conteneurs.
    echo  Verifiez que Docker Desktop est bien lance.
    echo.
    pause
    exit /b 1
)

echo  [2/3] Attente que l'application soit prete...
:wait_loop
    docker compose exec -T streamlit_app curl -s http://localhost:8501 > NUL 2>&1
    if %errorlevel% neq 0 (
        timeout /t 3 /nobreak > NUL
        goto wait_loop
    )

echo  [3/3] Ouverture du dashboard dans le navigateur...
start http://localhost:8501

echo.
echo  ================================================
echo   Application disponible sur http://localhost:8501
echo   phpMyAdmin disponible sur  http://localhost:8082
echo  ================================================
echo.
echo  Laissez cette fenetre ouverte tant que vous utilisez
echo  l'application. Appuyez sur une touche pour TOUT ARRETER.
echo.
pause > NUL

echo.
echo  Arret des conteneurs en cours...
docker compose down > NUL 2>&1
echo  Application arretee. Bonne journee !
echo.
pause
