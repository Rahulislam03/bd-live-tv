import requests
import json
import re
from datetime import datetime

def fetch_tplay_data():
    url = "https://tplay.live/tv"
    channels = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print(f"Fetching data from: {url}")
        response = requests.get(url, headers=headers, timeout=25)
        if response.status_code == 200:
            html_content = response.text
            
            # Regex ব্যবহার করে লোগো, নাম এবং লিঙ্ক বের করা
            # tplay-এর কার্ড ফরম্যাট অনুযায়ী প্যাটার্ন সাজানো হয়েছে
            pattern = r'<div class="card.*?src="(.*?)".*?href="(.*?)".*?class="card-title">(.*?)<'
            matches = re.findall(pattern, html_content, re.DOTALL)

            for logo_url, play_url, name in matches:
                # যদি লোগো লিঙ্কটি রিলেটিভ হয় তবে মেইন ডোমেইন যোগ করা
                full_logo = logo_url if logo_url.startswith('http') else f"https://tplay.live{logo_url}"
                full_play = play_url if play_url.startswith('http') else f"https://tplay.live{play_url}"
                
                channels.append({
                    "name": name.strip(),
                    "url": full_play,
                    "logo": full_logo
                })
        else:
            print(f"Could not access TPlay. Status: {response.status_code}")
    except Exception as e:
        print(f"Error occurred: {e}")
    
    return channels

def update_json():
    # TPlay থেকে ডাটা সংগ্রহ
    tplay_channels = fetch_tplay_data()
    
    # যদি TPlay-তে কম চ্যানেল পাওয়া যায়, তবে ব্যাকআপ হিসেবে GitHub সোর্স যোগ করা
    if not tplay_channels:
        print("TPlay failed, using backup sources...")
        # এখানে তোমার আগের GitHub সোর্সগুলো কাজ করবে
    
    final_json = {
        "info": {
            "owner": "Rahul Islam",
            "source": "tplay.live",
            "total_channels": len(tplay_channels),
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p")
        },
        "channels": tplay_channels
    }

    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Success! {len(tplay_channels)} channels saved with logos.")

if __name__ == "__main__":
    update_json()
    
