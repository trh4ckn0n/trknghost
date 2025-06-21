# Variables
$URL = "https://github.com/trh4ckn0n/trknghost/releases/download/dl/trknghost.zip"
$TMPDIR = Join-Path -Path $env:TEMP -ChildPath ("trknghost_" + [guid]::NewGuid())
$ZIPFILE = Join-Path -Path $TMPDIR -ChildPath "trknghost.zip"

# Création du dossier temporaire
New-Item -ItemType Directory -Path $TMPDIR -Force | Out-Null

Write-Host "[*] Téléchargement de l'archive..."
try {
    Invoke-WebRequest -Uri $URL -OutFile $ZIPFILE -ErrorAction Stop
} catch {
    Write-Error "Erreur lors du téléchargement : $_"
    exit 1
}

Write-Host "[*] Décompression de l'archive..."
try {
    Expand-Archive -Path $ZIPFILE -DestinationPath $TMPDIR -Force
} catch {
    Write-Error "Erreur lors de la décompression : $_"
    exit 1
}

Set-Location $TMPDIR

if (Test-Path "trknghost") {
    Write-Host "[*] Lancement de trknghost"
    Start-Process -FilePath ".\trknghost" -Wait
} elseif (Test-Path "trknghost.py") {
    Write-Host "[*] Lancement de trknghost.py avec Python"
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        Write-Error "Python n'est pas installé ou non trouvé dans le PATH."
        exit 1
    }
    & python trknghost.py
} else {
    Write-Error "Fichier exécutable non trouvé."
    exit 1
}

# Nettoyage optionnel
Remove-Item -LiteralPath $TMPDIR -Recurse -Force
