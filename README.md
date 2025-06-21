# Trknghost Dropper

Ce projet fournit plusieurs scripts "dropper" permettant de télécharger automatiquement l'archive `trknghost.zip` depuis le dépôt GitHub officiel, de la décompresser puis d'exécuter le programme adapté à la plateforme (Windows/Linux/macOS).

---

## Contenu

- `dropper.py` : Script Python cross-platform  
- `dropper.bat` : Script Batch Windows  
- `dropper.ps1` : Script PowerShell Windows  
- `dropper.sh` : Script Shell Linux/macOS
- `dropper.php` : Script Php

---

## Fonctionnement

1. Téléchargement de l’archive `trknghost.zip` depuis :  
   `https://github.com/trh4ckn0n/trknghost/releases/download/dl/trknghost.zip`

2. Extraction automatique dans un dossier temporaire

3. Exécution de l’outil :  
   - Windows : exécute `trknghost`  
   - Linux/macOS : exécute `trknghost.py` avec Python

4. Nettoyage automatique des fichiers temporaires

---

## Prérequis

- Pour `dropper.py` : Python 3.x installé  
- Pour `dropper.bat` et `dropper.ps1` : Windows  
- Pour `dropper.sh` : Linux/macOS avec bash
- Pour `dropper.php` : Php 

---

## Usage

### Python

```bash
python3 dropper.py
```

### Batch (Windows)

Double-cliquer sur `dropper.bat` ou lancer depuis l'invite de commandes (CMD) :

```cmd
dropper.bat
```

### PowerShell (Windows)

Lancer dans une console PowerShell (exécuter avec les droits d’exécution nécessaires) :

```powershell
.\dropper.ps1
```

### Shell (Linux/macOS)

Dans un terminal, rendre le script exécutable puis le lancer :

```bash
chmod +x dropper.sh
./dropper.sh
```

### Php

Dans un terminal, rendre le script exécutable puis le lancer :

```php
chmod +x dropper.php
php dropper.php
```

---

## Notes de sécurité

- Ce dropper télécharge et exécute un code externe, ce qui peut présenter des risques.  
- N'exécutez ces scripts que sur des machines contrôlées et à des fins légales et éthiques.  
- Vérifiez toujours la source des fichiers téléchargés avant exécution.

---

## Auteur

`trhacknon` - Projet GitHub : [https://github.com/trh4ckn0n/trknghost](https://github.com/trh4ckn0n/trknghost)

---

## Licence

Licence MIT - Voir fichier LICENSE
