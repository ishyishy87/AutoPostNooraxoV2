from datetime import datetime
from config import LOG_FILE

def log(msg):
    line = f"{datetime.now()} - {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
