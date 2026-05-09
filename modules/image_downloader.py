import requests
from modules.logger import log

def download_image(url, pid):
    if not url:
        return None

    fn = f"temp_{pid}.jpg"

    try:
        r = requests.get(url, stream=True, timeout=15)
        if r.status_code != 200:
            log(f"Image download failed: HTTP {r.status_code}")
            return None

        with open(fn, "wb") as f:
            for c in r.iter_content(1024):
                if c:
                    f.write(c)

        return fn

    except Exception as e:
        log(f"Image download error: {e}")
        return None
