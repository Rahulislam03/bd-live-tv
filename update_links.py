import requests
import json
import concurrent.futures
import os
from datetime import datetime

# Settings
LIMIT = 999999999999
CHUNK_SIZE = 200000  # Protibar 2 lakh loop check korbe
WORKERS = 100
STATE_FILE = "last_id.txt" # Jekhane sesh hobe seta save thakbe

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://tplay.live/',
}

# Jekhan theke scan shuru hobe seta load kora
def load_last_id():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return int(f.read().strip())
    return 1 # Default shuru 1 theke

def check_link(ch_id):
    url = f"https://cloudfrontnet.vercel.app/tplay/playout/{ch_id}/master.m3u8"
    try:
        r = requests.head(url, headers=headers, timeout=1.5)
        if r.status_code == 200 or r.status_code == 302:
            print(f"✔️ Found: {ch_id}")
            return {"id": ch_id, "name": f"Channel {ch_id}", "url": url}
    except:
        return None
    return None

def start_scan():
    start_id = load_last_id()
    end_id = min(start_id + CHUNK_SIZE, LIMIT)
    
    print(f"Scanning range: {start_id} theke {end_id} porjonto...")
    valid_channels = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        results = list(executor.map(check_link, range(start_id, end_id)))

    valid_channels = [ch for ch in results if ch is not None]

    # Purono channels load kora jate replace na hoy, add hoy
    all_channels = []
    if os.path.exists('channels.json'):
        try:
            with open('channels.json', 'r') as f:
                old_data = json.load(f)
                all_channels = old_data.get("channels", [])
        except: pass

    all_channels.extend(valid_channels)

    # Save Results
    data = {
        "info": {"creator": "Islam Rahul", "updated": str(datetime.now())},
        "channels": all_channels
    }
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    # Next time-er jonno last ID save kora
    with open(STATE_FILE, "w") as f:
        f.write(str(end_id))

    print(f"Scan shesh! Next scan shuru hobe {end_id} theke.")

if __name__ == "__main__":
    start_scan()
    
