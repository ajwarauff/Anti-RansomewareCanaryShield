import os
import time
import hashlib
import ctypes
from cryptography.fernet import Fernet
import config

try:
    ctypes.windll.kernel32.SetFileAttributesW(config.BACKUP_DIR, 2)
except Exception:
    pass

def log_event(message, color="#00ff00"):
    """Writes to the text file AND pushes to the GUI live log box safely."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {message}"
    
    # 1. Permanent File Write
    try:
        with open(config.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted_msg + "\n")
    except Exception:
        pass
    
    # 2. Push to Tkinter GUI Thread-Safe Queue
    config.ui_queue.put({
        "type": "GENERIC_LOG",
        "message": message,  # GUI formats its own timestamp or shows clean message
        "color": color
    })

# Setup cryptographic keys
if not os.path.exists(config.KEY_FILE):
    secret_key = Fernet.generate_key()
    with open(config.KEY_FILE, "wb") as f:
        f.write(secret_key)
else:
    with open(config.KEY_FILE, "rb") as f:
        secret_key = f.read()

cipher = Fernet(secret_key)

# Auto deploy canary bait
canary_path = os.path.join(config.PROTECTED_DIR, config.CANARY_NAME)
if not os.path.exists(canary_path):
    with open(canary_path, "w", encoding="utf-8") as f:
        f.write("SECURITY CANARY VALUE: DO NOT MODIFY OR EDIT THIS FILE. ANTI-RANSOMWARE SHIELD ACTIVE.")

def calculate_sha256(file_path):
    hasher = hashlib.sha256()
    for _ in range(5): 
        try:
            with open(file_path, "rb") as f:
                buf = f.read()
                if len(buf) == 0:
                    time.sleep(0.1)
                    continue
                hasher.update(buf)
            return hasher.hexdigest()
        except (FileNotFoundError, PermissionError):
            time.sleep(0.1) 
    return None

def create_encrypted_backup(file_path):
    file_name = os.path.basename(file_path)
    backup_path = os.path.join(config.BACKUP_DIR, file_name + ".enc")
    try:
        with open(file_path, "rb") as f:
            original_data = f.read()
        encrypted_data = cipher.encrypt(original_data)
        with open(backup_path, "wb") as f:
            f.write(encrypted_data)
    except Exception:
        pass

def initialize_existing_files():
    for file_name in os.listdir(config.PROTECTED_DIR):
        file_path = os.path.join(config.PROTECTED_DIR, file_name)
        if os.path.isfile(file_path):
            file_hash = calculate_sha256(file_path)
            if file_hash:
                config.STATE["baselines"][file_name] = file_hash
                create_encrypted_backup(file_path)
    log_event("INTEGRITY: Existing directory assets baselined and backed up successfully.", "#00ff00")