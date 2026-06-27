import tkinter as tk
from tkinter import filedialog
import os
import shutil
import threading
import time
import winsound
import queue

import config
import crypto_utils
import monitor
import network_listener

# Track dynamic session metrics
session_metrics = {
    "attacks_blocked": 0,
    "integrity_score": "100%"
}

# Initialize existing records
crypto_utils.initialize_existing_files()

# ========================================================
# GUI LIVE METRICS REFRESHER
# ========================================================
def update_dashboard_counters():
    """Dynamically recalculates secure assets and health updates."""
    try:
        total_files = len([f for f in os.listdir(config.PROTECTED_DIR) if os.path.isfile(os.path.join(config.PROTECTED_DIR, f))])
        stat_files_val.config(text=f"{total_files:02d}")
        stat_attacks_val.config(text=f"{session_metrics['attacks_blocked']:02d}")
        stat_health_val.config(text=session_metrics["integrity_score"])
    except Exception:
        pass

# ========================================================
# INTERACTIVE HOVER GLOW SYSTEM
# ========================================================
def add_cyber_hover_effect(widget, hover_bg, hover_fg, normal_bg, normal_fg):
    """Creates a smooth tactical glowing response when mouse pointer hovers over elements."""
    widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg, fg=hover_fg))
    widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg, fg=normal_fg))

# ========================================================
# GUI CORE ACTION HANDLERS
# ========================================================

def refresh_file_list():
    file_list_box.delete(0, tk.END)
    for file_name in sorted(os.listdir(config.PROTECTED_DIR)):
        if os.path.isfile(os.path.join(config.PROTECTED_DIR, file_name)):
            if file_name == config.CANARY_NAME:
                file_list_box.insert(tk.END, f" 🛡️  {file_name} [CANARY]")
            else:
                file_list_box.insert(tk.END, f" 📄  {file_name}")
    update_dashboard_counters()

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        
        if file_name.lower() == config.CANARY_NAME.lower():
            crypto_utils.log_event("[⚠️ SYSTEM] Upload Denied: Signature matches protected honey-token canary nomenclature.", "#ff3333")
            return

        if file_name < config.CANARY_NAME:
            old_name = file_name
            file_name = "asset_" + file_name
            crypto_utils.log_event(f"[SHIELD] Cryptographic Lexicographical re-indexing: {old_name} -> {file_name}", "#ffaa00")
        
        dest_path = os.path.join(config.PROTECTED_DIR, file_name)
        shutil.copy(file_path, dest_path)
        
        file_hash = crypto_utils.calculate_sha256(dest_path)
        if file_hash:
            config.STATE["baselines"][file_name] = file_hash
            crypto_utils.create_encrypted_backup(dest_path)
        
        refresh_file_list()
        crypto_utils.log_event(f"[VAULT] New data node sealed and mirrored: {file_name}", "#39ff14")

def view_selected_file():
    try:
        selected_index = file_list_box.curselection()
        if not selected_index:
            crypto_utils.log_event("[⚠️ INTERFACE] Operator warning: Kernel view called without asset target anchor.", "#ffaa00")
            return
            
        selected_text = file_list_box.get(selected_index[0])
        file_name = selected_text.replace(" 📄  ", "").replace(" 🛡️  ", "").replace(" [CANARY]", "").strip()
        file_path = os.path.join(config.PROTECTED_DIR, file_name)
        
        if os.path.exists(file_path):
            os.startfile(file_path)
            crypto_utils.log_event(f"[SYSTEM] Sandboxed memory execution verified for token node: {file_name}", "#00f0ff")
        else:
            crypto_utils.log_event(f"[ERROR] Asset pointer tracking corrupted on drive sector: {file_name}", "#ff3333")
    except Exception as e:
        crypto_utils.log_event(f"[ERROR] Base sub-shell pipeline execution fault: {str(e)}", "#ff3333")

def download_selected_file():
    try:
        selected_index = file_list_box.curselection()
        if not selected_index:
            crypto_utils.log_event("[⚠️ INTERFACE] Operator warning: Decryption stream called on empty index.", "#ffaa00")
            return
            
        selected_text = file_list_box.get(selected_index[0])
        file_name = selected_text.replace(" 📄  ", "").replace(" 🛡️  ", "").replace(" [CANARY]", "").strip()
        source_path = os.path.join(config.PROTECTED_DIR, file_name)
        
        if os.path.exists(source_path):
            dest_path = filedialog.asksaveasfilename(initialfile=file_name, title="Decrypt & Export Asset Node")
            if dest_path:
                shutil.copy(source_path, dest_path)
                crypto_utils.log_event(f"[SUCCESS] Integrity verification passed. Sector exported to: {os.path.basename(dest_path)}", "#39ff14")
        else:
            crypto_utils.log_event(f"[ERROR] Extraction failed. Object structural node absent from memory pool.", "#ff3333")
    except Exception as e:
        crypto_utils.log_event(f"[ERROR] Export handling thread faulted: {str(e)}", "#ff3333")

def execute_cryptographic_repair():
    if not config.STATE["system_compromised"]:
        crypto_utils.log_event("[INFO] Diagnostic Scan Complete: System operational integrity optimal.", "#39ff14")
        return

    crypto_utils.log_event("[SYSTEM] Initializing Master Cryptographic Rollback Protocol...", "#00f0ff")
    
    current_time = time.time()
    for file_name in config.STATE["baselines"].keys():
        config.STATE["last_alert_times"][file_name] = current_time + 4
    
    try:
        for file_name in list(config.STATE["baselines"].keys()):
            backup_path = os.path.join(config.BACKUP_DIR, file_name + ".enc")
            target_path = os.path.join(config.PROTECTED_DIR, file_name)
            if os.path.exists(backup_path):
                with open(backup_path, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = crypto_utils.cipher.decrypt(encrypted_data)
                with open(target_path, "wb") as f:
                    f.write(decrypted_data)
        
        time.sleep(0.5)
        status_value.config(text="🛡️ SHIELD SECURED & ACTIVE", fg="#39ff14")
        header_label.config(text="SYSTEM FIREWALL OPERATIONAL", fg="#00f0ff")
        
        crypto_utils.log_event("[SUCCESS] Decryption array deployed! All sector data anomalies repaired.", "#39ff14")
        config.STATE["system_compromised"] = False
        session_metrics["integrity_score"] = "100%"
        
        upload_btn.config(state=tk.NORMAL)
        view_btn.config(state=tk.NORMAL)
        download_btn.config(state=tk.NORMAL)
        
        refresh_file_list()
    except Exception as e:
        crypto_utils.log_event(f"[CRITICAL] Kernel memory reconstruction framework fault: {str(e)}", "#ff3333")

# ========================================================
# HISTORICAL LOGS RELOADER
# ========================================================
def load_historical_logs():
    if os.path.exists(config.LOG_FILE):
        try:
            with open(config.LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-100:]:
                    clean_line = line.strip()
                    log_box.insert(tk.END, clean_line)
                    
                    if any(x in clean_line for x in ["🚨", "CRITICAL", "BREACH"]):
                        log_box.itemconfig(log_box.size() - 1, fg="#ff3333")
                        session_metrics["attacks_blocked"] += 1 
                        session_metrics["integrity_score"] = "00% CRITICAL"
                    elif any(x in clean_line for x in ["⚠️", "WARNING"]):
                        log_box.itemconfig(log_box.size() - 1, fg="#ffaa00")
                    elif any(x in clean_line for x in ["SUCCESS", "VAULT", "INTEGRITY"]):
                        log_box.itemconfig(log_box.size() - 1, fg="#39ff14")
                    elif "[NET]" in clean_line:
                        log_box.itemconfig(log_box.size() - 1, fg="#00f0ff")
                    else:
                        log_box.itemconfig(log_box.size() - 1, fg="#888888")
            log_box.see(tk.END)
        except Exception:
            pass

# ========================================================
# UI MULTI-THREAD PIPELINE REFRESHER
# ========================================================
def process_ui_queue():
    try:
        while True:
            data = config.ui_queue.get_nowait()
            
            if data["type"] == "ALERT":
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                
                if data["is_canary"]:
                    session_metrics["attacks_blocked"] += 1
                    session_metrics["integrity_score"] = "00% COMPROMISED"
                    
                    log_msg = f"[🚨 CYBER BREACH] Honeypot Canary Altered: {data['file_name']}"
                    log_box.insert(tk.END, log_msg)
                    log_box.itemconfig(log_box.size() - 1, fg="#ff3333")
                    
                    status_value.config(text="❌ INTRUSION DETECTED: SYSTEM LOCKED Down", fg="#ff3333")
                    header_label.config(text="🚨 CRITICAL INTRUSION LEVEL 5 🚨", fg="#ff3333")
                    
                    upload_btn.config(state=tk.DISABLED)
                    view_btn.config(state=tk.DISABLED)
                    download_btn.config(state=tk.DISABLED)
                else:
                    log_msg = f"[⚠️ EXPLOIT SUSPECT] Sector structural drift on file: {data['file_name']}"
                    log_box.insert(tk.END, log_msg)
                    log_box.itemconfig(log_box.size() - 1, fg="#ffaa00")
                
                log_box.insert(tk.END, f"       >> EXPECTED KEY: {data['baseline'][:28]}")
                log_box.itemconfig(log_box.size() - 1, fg="#666666")
                log_box.insert(tk.END, f"       >> CURRENT KEY:  {data['current'][:28]}")
                log_box.itemconfig(log_box.size() - 1, fg="#666666")
                log_box.see(tk.END)
                update_dashboard_counters()
            
            elif data["type"] == "GENERIC_LOG":
                gui_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                log_box.insert(tk.END, f"[{gui_timestamp}] {data['message']}")
                if data["color"]:
                    # Adjust older bright green to sleek neon green
                    adj_color = "#39ff14" if data["color"] == "#00ff00" else data["color"]
                    log_box.itemconfig(log_box.size() - 1, fg=adj_color)
                log_box.see(tk.END)
                update_dashboard_counters()
                
    except queue.Empty:
        pass
    root.after(100, process_ui_queue)

# ========================================================
# MAIN DISPLAY WINDOW BUILDER
# ========================================================
root = tk.Tk()
root.title("🦾 Advanced Cyber Ransomware Defense System")
root.geometry("820x620") 
root.configure(bg="#0a0a0a") # Deep dark hacker background
root.withdraw()

def verify_access():
    entered_password = password_entry.get()
    if entered_password == "admin123":
        login_win.destroy()
        root.deiconify()
        crypto_utils.log_event("SESSION INITIALIZED: Security operational authorization valid.", "#39ff14")
        refresh_file_list()
    else:
        error_label.config(text="❌ ACCESS REJECTED: INVALID CREDENTIAL PATH", fg="#ff3333")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(config.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] INCIDENT REPORT: Unauthorized perimeter penetration attempt detected.\n")
        except Exception: pass

# --- Tactical Login Authorization Window ---
login_win = tk.Toplevel()
login_win.title("Core Authentication Terminal")
login_win.geometry("400x240")
login_win.configure(bg="#0d0d0d")
login_win.resizable(False, False)
login_win.protocol("WM_DELETE_WINDOW", root.destroy)

# Border styling trick for cyber frames
tk.Frame(login_win, height=2, bg="#00f0ff").pack(fill="x")

tk.Label(login_win, text="🔓 SECURITY CORE ACCESS REQUIRED", font=("Courier New", 12, "bold"), fg="#00f0ff", bg="#0d0d0d").pack(pady=15)
tk.Label(login_win, text="ENTER MASTER ENCRYPTION KEY:", font=("Courier New", 9), fg="#888888", bg="#0d0d0d").pack(pady=2)

password_entry = tk.Entry(login_win, show="*", font=("Courier New", 12), width=22, bg="#141414", fg="#39ff14", insertbackground="#39ff14", bd=1, relief="solid", highlightthickness=1, highlightcolor="#00f0ff", highlightbackground="#333333")
password_entry.pack(pady=8)
password_entry.focus()
password_entry.bind("<Return>", lambda event: verify_access())

error_label = tk.Label(login_win, text="", font=("Courier New", 9), bg="#0d0d0d")
error_label.pack(pady=2)

login_btn = tk.Button(login_win, text="[ AUTHENTICATE ]", font=("Courier New", 10, "bold"), bg="#111111", fg="#00f0ff", activebackground="#00f0ff", activeforeground="#000000", bd=1, relief="solid", cursor="hand2", width=18, command=verify_access)
login_btn.pack(pady=12)
add_cyber_hover_effect(login_btn, hover_bg="#00f0ff", hover_fg="#000000", normal_bg="#111111", normal_fg="#00f0ff")

# --- Main Dashboard Setup ---
header_label = tk.Label(root, text="SYSTEM FIREWALL OPERATIONAL", font=("Courier New", 15, "bold"), fg="#00f0ff", bg="#0a0a0a")
header_label.pack(pady=12)

# Global Live Status Header Frame
status_frame = tk.Frame(root, bg="#111111", bd=1, relief="solid", highlightthickness=1, highlightbackground="#222222")
status_frame.pack(pady=2, fill="x", padx=20)
status_title = tk.Label(status_frame, text="🛡️ CORE DEFENSE MATRIX:", font=("Courier New", 10, "bold"), fg="#888888", bg="#111111")
status_title.pack(side="left", padx=15, pady=6)
status_value = tk.Label(status_frame, text="🛡️ SHIELD SECURED & ACTIVE", font=("Courier New", 10, "bold"), fg="#39ff14", bg="#111111")
status_value.pack(side="left", padx=5, pady=6)

# ========================================================
# STATS DASHBOARD BOARD (NEW HACKER LOOK PANELS)
# ========================================================
stats_panel_frame = tk.Frame(root, bg="#0a0a0a")
stats_panel_frame.pack(fill="x", padx=20, pady=10)

def build_stat_card(parent, headline, hex_color):
    card = tk.Frame(parent, bg="#111111", bd=1, relief="solid", highlightthickness=1, highlightbackground="#222222", width=170, height=65)
    card.pack_propagate(False)
    tk.Label(card, text=headline, font=("Courier New", 8, "bold"), fg="#666666", bg="#111111").pack(pady=(6,2))
    val_lbl = tk.Label(card, text="--", font=("Courier New", 14, "bold"), fg=hex_color, bg="#111111")
    val_lbl.pack()
    return card, val_lbl

card_files, stat_files_val = build_stat_card(stats_panel_frame, "SECURE DATA ASSETS", "#00f0ff")
card_files.pack(side="left", expand=True, padx=5)

card_attacks, stat_attacks_val = build_stat_card(stats_panel_frame, "THREATS THWANTED", "#ff3333")
card_attacks.pack(side="left", expand=True, padx=5)

card_health, stat_health_val = build_stat_card(stats_panel_frame, "SECTOR HEALTH RATE", "#39ff14")
card_health.pack(side="left", expand=True, padx=5)


# --- Core Functional Grid Panels ---
middle_frame = tk.Frame(root, bg="#0a0a0a")
middle_frame.pack(pady=5, fill="both", expand=True, padx=20)

# Left Layout Component: Inventory File Vault
file_mgmt_frame = tk.Frame(middle_frame, bg="#0a0a0a")
file_mgmt_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

tk.Label(file_mgmt_frame, text="// PROTECTED DIRECTORY ASSETS:", font=("Courier New", 9, "bold"), fg="#888888", bg="#0a0a0a").pack(anchor="w")
file_list_box = tk.Listbox(file_mgmt_frame, height=9, bg="#0f0f0f", fg="#00f0ff", font=("Courier New", 10), selectbackground="#1a3333", selectforeground="#00f0ff", highlightbackground="#222222", bd=0, highlightthickness=1)
file_list_box.pack(fill="both", expand=True, pady=6)

# Customized Cyber UI Function Triggers
upload_btn = tk.Button(file_mgmt_frame, text="[upload new file]", font=("Courier New", 9, "bold"), bg="#111111", fg="#39ff14", activebackground="#39ff14", activeforeground="#000000", bd=1, relief="solid", cursor="hand2", command=upload_file)
upload_btn.pack(pady=2, fill="x")
add_cyber_hover_effect(upload_btn, hover_bg="#39ff14", hover_fg="#000000", normal_bg="#111111", normal_fg="#39ff14")

view_btn = tk.Button(file_mgmt_frame, text="[view file]", font=("Courier New", 9, "bold"), bg="#111111", fg="#00f0ff", activebackground="#00f0ff", activeforeground="#000000", bd=1, relief="solid", cursor="hand2", command=view_selected_file)
view_btn.pack(pady=2, fill="x")
add_cyber_hover_effect(view_btn, hover_bg="#00f0ff", hover_fg="#000000", normal_bg="#111111", normal_fg="#00f0ff")

download_btn = tk.Button(file_mgmt_frame, text="[Export to computer]", font=("Courier New", 9, "bold"), bg="#111111", fg="#b026ff", activebackground="#b026ff", activeforeground="#ffffff", bd=1, relief="solid", cursor="hand2", command=download_selected_file)
download_btn.pack(pady=2, fill="x")
add_cyber_hover_effect(download_btn, hover_bg="#b026ff", hover_fg="#ffffff", normal_bg="#111111", normal_fg="#b026ff")

# Right Layout Component: Realtime Forensic Logs Terminal
activity_frame = tk.Frame(middle_frame, bg="#0a0a0a")
activity_frame.pack(side="right", fill="both", expand=True)

tk.Label(activity_frame, text="// LIVE SECURITY TELEMETRY LOGS:", font=("Courier New", 9, "bold"), fg="#888888", bg="#0a0a0a").pack(anchor="w")
log_box = tk.Listbox(activity_frame, height=9, bg="#050505", fg="#39ff14", font=("Courier New", 9), bd=0, highlightthickness=1, highlightbackground="#222222", selectbackground="#112211")
log_box.pack(fill="both", expand=True, pady=6)

# Trigger immediate asset check
load_historical_logs()
refresh_file_list()

# Bottom Layout Row: Tactical Patch Operations
repair_btn = tk.Button(root, text="[ RUN CRYPTOGRAPHIC COUNTER-REPAIR PROTOCOL ]", font=("Courier New", 11, "bold"), bg="#111111", fg="#ffaa00", activebackground="#ffaa00", activeforeground="#000000", bd=1, relief="solid", cursor="hand2", command=execute_cryptographic_repair)
repair_btn.pack(pady=15, fill="x", padx=20)
add_cyber_hover_effect(repair_btn, hover_bg="#ffaa00", hover_fg="#000000", normal_bg="#111111", normal_fg="#ffaa00")

root.after(100, process_ui_queue)

# Parallel thread systems
monitor_thread = threading.Thread(target=monitor.start_folder_monitoring, daemon=True)
monitor_thread.start()

kali_thread = threading.Thread(target=network_listener.start_kali_listener, daemon=True)
kali_thread.start()

root.mainloop()