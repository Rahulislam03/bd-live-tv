import requests
import json
import re
from datetime import datetime

def fetch_links():
    channels_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://cloudfrontnet.vercel.app/'
    }

    # সোর্স ১: সরাসরি cloudfrontnet সাইট থেকে স্ক্র্যাপ করা
    try:
        print("পদ্ধতি ১: Cloudfrontnet থেকে চ্যানেল খোঁজা হচ্ছে...")
        response = requests.get("https://cloudfrontnet.vercel.app/", headers=headers, timeout=20)
        if response.status_code == 200:
            # আইডি এবং নাম খোঁজার রেগুলার এক্সপ্রেশন
            # এটি লিঙ্ক থেকে আইডি (যেমন ২০৯৬১১) এবং টেক্সট থেকে নাম নেবে
            matches = re.findall(r'playout/(\d+)/master\.m3u8.*?<td>(.*?)</td>', response.text, re.DOTALL)
            
            for ch_id, name in matches:
                channels_list.append({
                    "name": name.strip(),
                    "url": f"https://cloudfrontnet.vercel.app/tplay/playout/{ch_id}/master.m3u8",
                    "logo": f"https://www.tataplay.com/cms-assets/s3fs-public/logos/{ch_id}.png"
                })
    except Exception as e:
        print(f"Error in Method 1: {e}")

    # সোর্স ২: যদি পদ্ধতি ১ ব্যর্থ হয়, তবে কমন আইডি ব্যবহার করে জেনারেট করা
    if not channels_list:
        print("পদ্ধতি ২: স্ট্যাটিক আইডি লিস্ট ব্যবহার করা হচ্ছে...")
        # এখানে জনপ্রিয় কিছু চ্যানেলের আইডি (গোপাল ভাঁড়, সনি, ইত্যাদি)
        common_ids = {
            "209611": "24/7 Gopal Bhar",
            "1000001003": "Sony Aath",
            "1000000961": "Star Jalsha",
            "1000000971": "Zee Bangla",
            "1000000951": "Colors Bangla"
        }
        for ch_id, ch_name in common_ids.items():
            channels_list.append({
                "name": ch_name,
                "url": f"https://cloudfrontnet.vercel.app/tplay/playout/{ch_id}/master.m3u8",
                "logo": f"https://www.tataplay.com/cms-assets/s3fs-public/logos/{ch_id}.png"
            })

    # ডুপ্লিকেট রিমুভ করা
    unique_data = {ch['url']: ch for ch in channels_list}.values()
    return list(unique_data)

def update_json():
    all_channels = fetch_links()
    
    final_json = {
        "info": {
            "owner": "Islam Rahul",
            "total": len(all_channels),
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p")
        },
        "channels": all_channels
    }
    
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)
    
    print(f"✅ সাকসেস! মোট {len(all_channels)}টি চ্যানেল আপডেট হয়েছে।")

if __name__ == "__main__":
    update_json()
    
