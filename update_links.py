import requests
import json
import re
from datetime import datetime

def fetch_live_channels():
    # টাটা প্লে-এর ভেরিফাইড আইডি লিস্ট (এগুলো এখন লাইভ আছে)
    channel_ids = {
        "209611": "24/7 Gopal Bhar",
        "1000001003": "Sony Aath",
        "1000000961": "Star Jalsha",
        "1000000971": "Zee Bangla",
        "1000000951": "Colors Bangla",
        "1000000106": "Star Sports 1",
        "1000000093": "Sony Ten 1",
        "1000001402": "Jalsha Movies",
        "1000000973": "Zee Bangla Cinema"
    }

    base_url = "https://cloudfrontnet.vercel.app/tplay/playout/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Android 11; Mobile; rv:128.0) Gecko/128.0 Firefox/128.0',
        'Referer': 'https://tplay.live/',
        'Origin': 'https://tplay.live'
    }

    live_list = []
    print("চ্যানেলগুলো লাইভ চেক করা হচ্ছে...")

    for cid, name in channel_ids.items():
        m3u8_url = f"{base_url}{cid}/master.m3u8"
        try:
            # লিঙ্কটি আসলেই কাজ করছে কি না তা চেক করা
            response = requests.head(m3u8_url, headers=headers, timeout=10)
            if response.status_code < 400: # ২০০ বা ৩০২ হলে লাইভ ধরা হবে
                live_list.append({
                    "name": name,
                    "url": m3u8_url,
                    "logo": f"https://www.tataplay.com/cms-assets/s3fs-public/logos/{cid}.png"
                })
                print(f"✅ {name} - লাইভ আছে।")
        except:
            continue
    
    return live_list

def run_update():
    channels = fetch_live_channels()
    
    output = {
        "info": {
            "owner": "Islam Rahul",
            "total": len(channels),
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p")
        },
        "channels": channels
    }

    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nমোট {len(channels)}টি চ্যানেল আপডেট হয়েছে। এখন তোমার সাইটে এগুলো চলবে।")

if __name__ == "__main__":
    run_update()
    
