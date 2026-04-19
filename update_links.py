import requests
import json
import concurrent.futures
import os
from datetime import datetime

# Settings
LIMIT = 999999999999
CHUNK_SIZE = 200000  # প্রতিবার ২ লাখ আইডি চেক করবে
WORKERS = 100        # একসাথে ১০০টি রিকোয়েস্ট পাঠাবে
STATE_FILE = "last_id.txt"
CHANNELS_FILE = "channels.json"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://tplay.live/',
}

def load_last_id():
    """শেষ সেভ করা আইডি লোড করা, ফাইল খালি থাকলে ১ রিটার্ন করবে"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            content = f.read().strip()
            if content:
                return int(content)
    return 1

def check_link(ch_id):
    """লিঙ্কটি সচল কি না তা চেক করা"""
    url = f"https://cloudfrontnet.vercel.app/tplay/playout/{ch_id}/master.m3u8"
    try:
        r = requests.head(url, headers=headers, timeout=1.5)
        if r.status_code == 200 or r.status_code == 302:
            print(f"✔️ Found: {ch_id}")
            return {
                "id": ch_id, 
                "name": f"Channel {ch_id}", 
                "url": url,
                "logo": f"https://www.tataplay.com/cms-assets/s3fs-public/logos/{ch_id}.png"
            }
    except:
        return None
    return None

def start_scan():
    start_id = load_last_id()
    end_id = min(start_id + CHUNK_SIZE, LIMIT)
    
    print(f"স্ক্যান শুরু হচ্ছে: {start_id} থেকে {end_id} পর্যন্ত...")
    
    # মাল্টি-থ্রেডিং ব্যবহার করে দ্রুত স্ক্যান
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        results = list(executor.map(check_link, range(start_id, end_id)))

    # নতুন পাওয়া চ্যানেলগুলো ফিল্টার করা
    new_found = [ch for ch in results if ch is not None]

    # পুরনো ডাটা লোড করা যাতে হারিয়ে না যায়
    all_channels = []
    if os.path.exists(CHANNELS_FILE):
        try:
            with open(CHANNELS_FILE, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                all_channels = old_data.get("channels", [])
        except Exception as e:
            print(f"পুরনো ডাটা লোড করতে সমস্যা: {e}")
            all_channels = []

    # পুরনো এবং নতুন চ্যানেল একসাথে করা
    all_channels.extend(new_found)

    # ডুপ্লিকেট রিমুভ করা (একই আইডি বারবার আসবে না)
    unique_channels = {ch['id']: ch for ch in all_channels}.values()
    final_list = list(unique_channels)

    # ডাটা সেভ করা
    data = {
        "info": {
            "creator": "Islam Rahul",
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_found": len(final_list),
            "last_scanned_id": end_id
        },
        "channels": final_list
    }

    with open(CHANNELS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # পরবর্তী স্ক্যানের জন্য আইডি সেভ করা
    with open(STATE_FILE, "w") as f:
        f.write(str(end_id))

    print(f"স্ক্যান শেষ! মোট {len(final_list)}টি সচল চ্যানেল ডাটাবেজে আছে।")
    print(f"পরবর্তী স্ক্যান শুরু হবে {end_id} থেকে।")

if __name__ == "__main__":
    start_scan()
                          
