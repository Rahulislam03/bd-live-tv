import requests
import json
import re
from datetime import datetime

def fetch_tplay_full():
    # মেইন সোর্স এবং এপিআই সোর্স
    url = "https://tplay.live/tv"
    vercel_base = "https://cloudfrontnet.vercel.app/tplay/playout/"
    
    channels = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print(f"চ্যানেল ডাটা সংগ্রহ করা হচ্ছে...")
        response = requests.get(url, headers=headers, timeout=25)
        
        if response.status_code == 200:
            # TPlay-এর কার্ড থেকে লোগো এবং চ্যানেল আইডি বের করা
            # সাধারণত লিঙ্কে আইডি থাকে যেমন: /play/209611
            pattern = r'class="card.*?src="(.*?)".*?href=".*?/play/(\d+)".*?class="card-title">(.*?)<'
            matches = re.findall(pattern, response.text, re.DOTALL)

            for logo, ch_id, name in matches:
                # তোমার দেওয়া cloudfrontnet ফরম্যাটে লিঙ্ক তৈরি করা
                direct_url = f"{vercel_base}{ch_id}/master.m3u8"
                
                channels.append({
                    "name": name.strip(),
                    "url": direct_url,
                    "logo": logo if logo.startswith('http') else f"https://tplay.live{logo}"
                })
        
        # যদি কিছু না পায় তবে ব্যাকআপ হিসেবে সরাসরি Vercel ইনডেক্স চেক করা
        if not channels:
            print("TPlay scraping failed, trying Vercel index...")
            v_res = requests.get("https://cloudfrontnet.vercel.app/", headers=headers, timeout=15)
            v_matches = re.findall(r'href=".*?/playout/(\d+)/master.m3u8".*?>(.*?)<', v_res.text)
            for ch_id, name in v_matches:
                channels.append({
                    "name": name.strip(),
                    "url": f"{vercel_base}{ch_id}/master.m3u8",
                    "logo": "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                })

    except Exception as e:
        print(f"Error: {e}")
    
    return channels

def update_json():
    all_channels = fetch_tplay_full()
    
    final_data = {
        "info": {
            "owner": "Islam Rahul",
            "total_channels": len(all_channels),
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p")
        },
        "channels": all_channels
    }

    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ সাকসেস! মোট {len(all_channels)}টি চ্যানেল সরাসরি .m3u8 লিঙ্কসহ সেভ হয়েছে।")

if __name__ == "__main__":
    update_json()
                    
