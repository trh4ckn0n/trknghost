import os
import sys
import tempfile
import platform
import zipfile
import subprocess
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

URL = "https://github.com/trh4ckn0n/trknghost/releases/download/dl/trknghost.zip"

def download_file(url, dest_path):
    try:
        print(f"[*] Téléchargement de l'archive depuis {url}...")
        with urlopen(url) as response, open(dest_path, 'wb') as out_file:
            out_file.write(response.read())
        print("[+] Téléchargement terminé.")
    except (URLError, HTTPError) as e:
        print(f"Erreur lors du téléchargement: {e}")
        sys.exit(1)

def extract_zip(zip_path, extract_to):
    try:
        print(f"[*] Extraction de l'archive vers {extract_to} ...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("[+] Extraction terminée.")
    except zipfile.BadZipFile as e:
        print(f"Erreur lors de l'extraction : {e}")
        sys.exit(1)

def run_executable(folder):
    system = platform.system()
    os.chdir(folder)
    if system == "Windows":
        exe_path = os.path.join(folder, "trknghost")
        if os.path.isfile(exe_path):
            print("[*] Lancement de trknghost")
            subprocess.run([exe_path])
        else:
            print("Erreur: trknghost.exe non trouvé.")
            sys.exit(1)
    else:
        py_path = os.path.join(folder, "trknghost.py")
        if os.path.isfile(py_path):
            print("[*] Lancement de trknghost.py avec Python")
            python = sys.executable or "python3"
            subprocess.run([python, py_path])
        else:
            print("Erreur: trknghost.py non trouvé.")
            sys.exit(1)

def main():
    with tempfile.TemporaryDirectory(prefix="trknghost_") as tmpdir:
        zip_path = os.path.join(tmpdir, "trknghost.zip")
        download_file(URL, zip_path)
        extract_zip(zip_path, tmpdir)
        run_executable(tmpdir)
        print("[*] Nettoyage terminé.")

if __name__ == "__main__":
    main()
