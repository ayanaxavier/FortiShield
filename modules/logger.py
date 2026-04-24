import os
from datetime import datetime

LOG_FILE = "database/threat_log.txt"


def log_event(file_path, status, action):

    os.makedirs("database", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_name = os.path.basename(file_path)

    log_entry = (
        f"Time: {timestamp} | "
        f"File: {file_name} | "
        f"Status: {status} | "
        f"Action: {action}\n"
    )

    with open(LOG_FILE, "a") as file:
        file.write(log_entry)