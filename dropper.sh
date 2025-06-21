#!/bin/bash

# URL de téléchargement
URL="https://github.com/trh4ckn0n/trknghost/releases/download/dl/trknghost.zip"

# Dossier temporaire
TMPDIR=$(mktemp -d)
ZIPFILE="$TMPDIR/trknghost.zip"

echo "[*] Téléchargement de l'archive..."
curl -L -o "$ZIPFILE" "$URL"
if [ $? -ne 0 ]; then
  echo "Erreur lors du téléchargement."
  exit 1
fi

echo "[*] Décompression de l'archive..."
unzip -q "$ZIPFILE" -d "$TMPDIR"
if [ $? -ne 0 ]; then
  echo "Erreur lors de la décompression."
  exit 1
fi

cd "$TMPDIR" || exit

# Détection OS basique
OS_TYPE=$(uname -s)
echo "[*] OS détecté: $OS_TYPE"

if [[ "$OS_TYPE" == "Linux" ]]; then
    if [[ -f "trknghost.py" ]]; then
        echo "[*] Lancement de trknghost.py sur Linux..."
        python3 trknghost.py
    else
        echo "Erreur : trknghost.py non trouvé."
        exit 1
    fi
elif [[ "$OS_TYPE" =~ (CYGWIN|MINGW|MSYS) ]]; then
    if [[ -f "trknghost" ]]; then
        echo "[*] Lancement de trknghost sur Windows..."
        ./trknghost.exe
    else
        echo "Erreur : trknghost non trouvé."
        exit 1
    fi
else
    echo "OS non supporté."
    exit 1
fi

# Nettoyage optionnel
rm -rf "$TMPDIR"
