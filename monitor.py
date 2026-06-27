import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import config
import crypto_utils

class CanaryHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            if file_name not in config.STATE["baselines"]: return
            
            new_hash = crypto_utils.calculate_sha256(event.src_path)
            if not new_hash or new_hash == config.STATE["baselines"][file_name]: return
                
            current_time = time.time()
            if file_name in config.STATE["last_alert_times"] and current_time - config.STATE["last_alert_times"][file_name] < 1.5: return
            
            config.STATE["last_alert_times"][file_name] = current_time
            is_canary_attack = (file_name == config.CANARY_NAME)
            
            if is_canary_attack:
                config.STATE["system_compromised"] = True
            
            config.ui_queue.put({
                "type": "ALERT",
                "action": "MODIFIED",
                "file_name": file_name,
                "baseline": config.STATE["baselines"].get(file_name, 'None'),
                "current": new_hash,
                "is_canary": is_canary_attack
            })

    def on_deleted(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            if file_name == config.CANARY_NAME:
                config.STATE["system_compromised"] = True
                config.ui_queue.put({
                    "type": "ALERT",
                    "action": "DELETED",
                    "file_name": file_name,
                    "baseline": config.STATE["baselines"].get(file_name, 'Active'),
                    "current": "NULL_FILE_ERASED",
                    "is_canary": True
                })

def start_folder_monitoring():
    event_handler = CanaryHandler()
    observer = Observer()
    observer.schedule(event_handler, path=config.PROTECTED_DIR, recursive=False)
    observer.start()
    while True:
        time.sleep(1)