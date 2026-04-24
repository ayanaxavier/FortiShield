import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from datetime import datetime

from modules.monitor import start_monitoring
from modules.scanner import scan_file

# -------- GLOBAL --------
quarantine_list = []

# -------- LOG FUNCTION --------
def log(message, status="INFO"):
    time = datetime.now().strftime("%H:%M:%S")

    colors = {
        "SAFE": "#22c55e",
        "MALWARE": "#ef4444",
        "WARNING": "#facc15",
        "INFO": "#38bdf8"
    }

    log_box.insert(tk.END, f"[{time}] {message}\n", status)
    log_box.tag_config(status, foreground=colors.get(status, "white"))
    log_box.see(tk.END)


def update_status(text, color):
    status_label.config(text=f"Status: {text}", fg=color)


# -------- POPUP --------
def show_malware_popup(file):
    popup = tk.Toplevel(root)
    popup.title("⚠ Malware Alert")
    popup.geometry("350x200")
    popup.configure(bg="#0f172a")

    tk.Label(
        popup,
        text="🚨 THREAT DETECTED!",
        fg="#ef4444",
        bg="#0f172a",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    tk.Label(
        popup,
        text=f"{file}\nhas been quarantined.",
        fg="white",
        bg="#0f172a"
    ).pack(pady=10)

    tk.Button(
        popup,
        text="OK",
        bg="#ef4444",
        fg="white",
        command=popup.destroy
    ).pack(pady=10)


# -------- MONITOR --------
def process_event(message):
    if "malware" in message.lower():
        log(message, "MALWARE")
        update_status("Threat Detected!", "#ef4444")

        file_name = message.split(":")[-1].strip()
        quarantine_list.append(file_name)
        update_quarantine()

        show_malware_popup(file_name)

    elif "safe" in message.lower():
        log(message, "SAFE")
        update_status("System Safe", "#22c55e")

    else:
        log(message, "INFO")


def run_monitor():
    update_status("Monitoring...", "#22c55e")
    log("Started monitoring Downloads folder")

    try:
        downloads_path = r"C:\Users\ayana\Downloads"
        start_monitoring(downloads_path, callback=process_event)

    except Exception as e:
        log(f"Error: {str(e)}", "MALWARE")

# -------- MANUAL SCAN --------
def select_file():
    file_path = filedialog.askopenfilename()

    if file_path:
        log(f"Manual scan: {file_path}", "INFO")
        update_status("Scanning...", "#facc15")

        threading.Thread(target=scan_selected_file, args=(file_path,)).start()


def scan_selected_file(file_path):
    try:
        result = scan_file(file_path)

        if isinstance(result, dict):
            if result.get("prediction", "").lower() == "malware":
                log(f"{file_path} → MALWARE", "MALWARE")
                update_status("Threat Detected!", "#ef4444")

                quarantine_list.append(file_path)
                update_quarantine()
                show_malware_popup(file_path)

            else:
                log(f"{file_path} → SAFE", "SAFE")
                update_status("System Safe", "#22c55e")

        else:
            log("Scan completed", "INFO")

    except Exception as e:
        log(f"Error: {str(e)}", "MALWARE")


# -------- QUARANTINE UI --------
def update_quarantine():
    quarantine_box.delete(0, tk.END)
    for item in quarantine_list:
        quarantine_box.insert(tk.END, item)


# -------- GUI --------
root = tk.Tk()
root.title("FortiShield")
root.geometry("900x550")
root.configure(bg="#010C3F")

# Title
tk.Label(
    root,
    text="FortiShield",
    font=("Arial", 24, "bold"),
    bg="#010C3F",
    fg="#6cc9f1"
).pack(pady=10)

# Status
status_label = tk.Label(
    root,
    text="Status: Idle",
    font=("Arial", 12, "bold"),
    bg="#020617",
    fg="#facc15"
)
status_label.pack()

# Buttons
btn_frame = tk.Frame(root, bg="#010C3F")
btn_frame.pack(pady=10)

tk.Button(
    btn_frame,
    text="▶ Start Monitoring",
    bg="#6bc6f0",
    fg="black",
    padx=20,
    pady=10,
    font=("Arial", 14, "bold"),
    command=lambda: threading.Thread(target=run_monitor).start()
).grid(row=0, column=0, padx=10)

tk.Button(
    btn_frame,
    text="🔍 Scan File",
    bg="#6bc6f0",
    fg="black",
    padx=20,
    pady=10,
    font=("Arial", 14, "bold"),
    command=select_file
).grid(row=0, column=1, padx=10)

# Main layout
main_frame = tk.Frame(root, bg="#020617")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Logs
log_frame = tk.Frame(main_frame, bg="#020617")
log_frame.pack(side="left", fill="both", expand=True)

tk.Label(
    log_frame,
    text="Activity Log",
    bg="#010C3F",
    fg="#38bdf8",
    font=("Arial", 16, "bold")
).pack()

log_box = tk.Text(
    log_frame,
    bg="#010C3F",
    fg="white",
    insertbackground="white",
    font=("Consolas", 12)
)
log_box.pack(fill="both", expand=True)

# Quarantine Panel
quarantine_frame = tk.Frame(main_frame, bg="#010C3F")
quarantine_frame.pack(side="right", fill="y", padx=10)

tk.Label(
    quarantine_frame,
    text="Quarantine",
    bg="#010C3F",
    fg="#ef4444",
    font=("Arial", 12, "bold"),
).pack()

quarantine_box = tk.Listbox(
    quarantine_frame,
    bg="#010C3F",
    fg="white",
    width=30
)
quarantine_box.pack(fill="y", expand=True)

root.mainloop()