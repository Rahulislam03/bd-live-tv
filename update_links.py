import requests
import json
import concurrent.futures
from datetime import datetime

# শুধু বাংলাদেশি এবং স্পোর্টস চ্যানেলের সম্ভাব্য রেঞ্জগুলো
SCAN_RANGES = [
    range(1000000050, 1000000150), # Sports HD (Star Sports, Sony Ten)
    range(1000000950, 1000001050), # Bengali HD (Star Jalsha, Zee Bangla)
    range(1000001400, 1000001500), # Movies & News (Jalsha Movies, etc.)
    range(1000001150, 1000001250), # Additional Bengali Channels
    range(209580, 209650)          # Kids/Gopal Bhar Zone
]

def check_id(ch_id):
    # তোমার বর্তমান প্রক্সি ইউআরএল
    url = f"https://cloudfrontnet.vercel.app/tplay/playout/{ch_id}/master.m3u8"
    try:
        # দ্রুত চেক করার জন্য HEAD রিকোয়েস্ট এবং কম টাইমআউট
        r = requests.head(url, timeout=3)
        if r.status_code == 200 or r.status_code == 302:
            print(f"✅ Found: {ch_id}")
            return {
                "id": ch_id,
                "name": f"Channel {ch_id}",
                "url": url,
                "logo": f"https://www.tataplay.com/cms-assets/s3fs-public/logos/{ch_id}.png"
            }
    except:
        return None
    return None

def main():
    all_found = []
    print("স্মার্ট বাংলাদেশি ও স্পোর্টস চ্যানেল স্ক্যান শুরু হচ্ছে...")
    
    # থ্রেড বাড়িয়ে দেওয়া হয়েছে যেন দ্রুত শেষ হয়
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for r in SCAN_RANGES:
            results = list(executor.map(check_id, r))
            all_found.extend([res for res in results if res is not None])

    # channels.json আপডেট
    output = {
        "info": {"owner": "Islam Rahul", "total": len(all_found), "updated": str(datetime.now())},
        "channels": all_found
    }
    
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nসফলভাবে {len(all_found)}টি চ্যানেল পাওয়া গেছে। গিটহাব আর এটি ক্যান্সেল করবে না।")

if __name__ == "__main__":
    main()
    
