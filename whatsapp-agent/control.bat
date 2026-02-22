@echo off
chcp 65001 > nul
REM HIM WhatsApp Agent Controller

cd /d "%~dp0"

echo =========================================
echo    HIM WhatsApp Agent 🤖
echo =========================================
echo.
echo 1. Configurer l'agent (setup)
echo 2. Démarrer l'agent (start)
echo 3. Mode test
echo 4. Démarrer le serveur webhook
echo 5. Voir les logs
echo 6. Quitter
echo.

set /p choice="Choix: "

if "%choice%"=="1" goto :setup
if "%choice%"=="2" goto :start
if "%choice%"=="3" goto :test
if "%choice%"=="4" goto :webhook
if "%choice%"=="5" goto :logs
if "%choice%"=="6" goto :end

echo Choix invalide.
pause
exit /b

:setup
python agent.py setup
pause
goto :end

:start
python agent.py start
pause
goto :end

:test
python agent.py test
pause
goto :end

:webhook
echo Démarrage du serveur webhook...
echo URL: http://localhost:5000/webhook/whatsapp
start python webhook_server.py
goto :end

:logs
type conversations.log | more
goto :end

:end
