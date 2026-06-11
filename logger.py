import os
from datetime import datetime

LOG_FILE = os.path.join(os.getcwd(), "output", "app.log")

def _ensure_log_dir():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_info(msg: str):
    _ensure_log_dir()
    line = f"[{datetime.utcnow().isoformat()}] INFO: {msg}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(line, end='')

def log_error(msg: str):
    _ensure_log_dir()
    line = f"[{datetime.utcnow().isoformat()}] ERROR: {msg}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(line, end='')
