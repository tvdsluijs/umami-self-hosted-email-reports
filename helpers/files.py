# helpers/files.py
import json
from datetime import datetime

def load_last_sent(file_path):
    try:
        with open(file_path, "r") as f:
            return datetime.fromisoformat(json.load(f)["last_sent"])
    except FileNotFoundError:
        return datetime.min

def save_last_sent(file_path, timestamp):
    with open(file_path, "w") as f:
        json.dump({"last_sent": timestamp.isoformat()}, f)
