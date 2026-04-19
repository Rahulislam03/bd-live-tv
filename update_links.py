import requests
import json
import concurrent.futures
import os
from datetime import datetime

# সোর্স কনফিগারেশন
CHANNELS_FILE = "channels.json"
STATE_FILE = "last_id.txt"
WORKERS = 50

# তোমার সেই ১২৯টি চ্যানেলের ডাটা (নমুনা হিসেবে সেরাগুলো দেওয়া হলো)
EXTERNAL_SOURCES = [
    {"name": "Gopal Bhar", "url": "https://live20.bozztv.com/giatvplayout7/giatv-209611/tracks-v1a1/mono.ts.m3u8", "cat": "Kids"},
    {"name": "IPL 2026 Live", "url": "http://206.212.244.183:25461/live/qdxkt3R5pH/5118349267/15965.m3u8", "cat": "Sports"},
    {"name": "Star Jalsha HD", "url": "https://playztv-apps.pages.dev/star-jalsha/index.m3u8", "cat": "Entertainment"},
    {"name": "Motu Patlu", "url": "https://live20.bozztv.com/giatvplayout7/giatv-209622/tracks-v1a1/mono.ts.m3u8", "cat": "Kids"},
    {"name": "Radio Bater BD", "url": "http://as31.digitalsynapsebd.com:8446/;stream.mp3", "cat": "Radio"},
    {"name": "Antarjal Movie", "url": "http://103.225.94.27/Infobase/hdd-2/Bangla/Antarjal%20(2023)%201080p%20WEBDL.mp4", "cat": "Movies"}
]

def get_mime_type(url):
    url = url.lower()
    if ".m3u8" in url: return "application/x-mpegURL"
    if ".ts" in url: return "video/mp2t"
    if ".mp4" in url: return "video/mp4"
    if ".mp3" in url or ";stream.mp3" in url: return "audio/mpeg"
    return "application/x-mpegURL" # Default

def check_tplay(ch_id):
    url = f"https://cloudfrontnet.vercel.app/tplay/playout/{ch_id}/master.m3u8"
    try:
        r = requests.head(url, timeout=2)
        if r.status_code == 200:
            return {
                "id": f"tplay_{ch_id}",
                "name": f"TataPlay {ch_id}",
                "link": url,
                "mime": "application/x-mpegURL",
                "category": "Tata Play",
                "logo": f"https://www.tataplay.com/cms-assets/s3fs-public/logos/{ch_id}.png"
            }
    except: return None

def start_scan():
    final_channels = []
    
    # ১. এক্সটার্নাল সোর্স প্রসেস করা
    for src in EXTERNAL_SOURCES:
        final_channels.append({
            "id": src["name"].lower().replace(" ", "_"),
            "name": src["name"],
            "link": src["url"],
            "mime": get_mime_type(src["url"]),
            "category": src["cat"],
            "logo": "https://cdn-icons-png.flaticon.com/512/716/716429.png"
        })

    # ২. টাটা প্লে স্ক্যান (লিমিটেড রেঞ্জ দ্রুত হওয়ার জন্য)
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        tplay_list = list(executor.map(check_tplay, range(1, 100))) # টেস্টের জন্য ১০০ পর্যন্ত
    
    final_channels.extend([ch for ch in tplay_list if ch])

    # ৩. JSON সেভ করা (Universal Structure)
    output = {
        "info": {"updated": str(datetime.now()), "total": len(final_channels)},
        "channels": final_channels,
        "response": final_channels # দুইভাবেই রাখা হলো যাতে সমস্যা না হয়
    }

    with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated! Total: {len(final_channels)}")

if __name__ == "__main__":
    start_scan()
