@echo off
setlocal enabledelayedexpansion

REM URL du fichier ZIP
set "URL=https://github.com/trh4ckn0n/trknghost/releases/download/dl/trknghost.zip"

REM Dossier temporaire
set "TMPDIR=%TEMP%\trknghost_%RANDOM%"

REM Création dossier temporaire
mkdir "%TMPDIR%"

REM Chemin complet du fichier zip
set "ZIPFILE=%TMPDIR%\trknghost.zip"

echo [*] Téléchargement de l'archive...
powershell -Command "Invoke-WebRequest -Uri '%URL%' -OutFile '%ZIPFILE%'"
if errorlevel 1 (
    echo Erreur lors du téléchargement.
    exit /b 1
)

echo [*] Décompression de l'archive...
powershell -Command "Expand-Archive -Path '%ZIPFILE%' -DestinationPath '%TMPDIR%' -Force"
if errorlevel 1 (
    echo Erreur lors de la décompression.
    exit /b 1
)

cd /d "%TMPDIR%"

REM Vérification et lancement
if exist "trknghost" (
    echo [*] Lancement de trknghost
    trknghost
) else if exist "trknghost.py" (
    echo [*] Lancement de trknghost.py avec Python
    python trknghost.py
) else (
    echo Fichier exécutable non trouvé.
    exit /b 1
)

REM Nettoyage optionnel
rd /s /q "%TMPDIR%"
