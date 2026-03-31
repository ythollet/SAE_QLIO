@echo off
echo =======================================================
echo    Lancement de l'environnement SAE QLIO (Docker)
echo =======================================================
echo.

echo 1. Lancement des conteneurs (MySQL, phpMyAdmin, Streamlit)...
docker-compose up -d --build

echo.
echo 2. Attente du demarrage complet des services (15 secondes)...
timeout /t 15 /nobreak > NUL

echo.
echo 3. Ouverture de l'application dans votre navigateur par defaut...
start http://localhost:8501

echo.
echo =======================================================
echo L'application est en cours d'execution en arriere-plan !
echo - Streamlit  : http://localhost:8501
echo - phpMyAdmin : http://localhost:8082
echo =======================================================
echo.
echo Pour TOUT ARRETER, appuyez sur une touche. Cela coupera les conteneurs.
pause

echo.
echo Arret des conteneurs en cours...
docker-compose down
echo Environnement arrete avec succes.
pause