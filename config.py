import os
import queue

PROTECTED_DIR = "protected_files"
BACKUP_DIR = "vault_backup"
KEY_FILE = os.path.join(BACKUP_DIR, "secret.key")
LOG_FILE = "shield_activity.log"
CANARY_NAME = "000_canary.txt"

os.makedirs(PROTECTED_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# Shared global dictionaries and states across dynamic module boundaries
STATE = {
    "system_compromised": False,
    "baselines": {},
    "last_alert_times": {}
}

ui_queue = queue.Queue()