import requests
import json
import re
from datetime import datetime

def fetch_channels():
    # আরও বেশি এবং সরাসরি সোর্স যোগ করা হয়েছে
    sources = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/bd.m3u",
        "https://raw.githubusercontent.com/TofazzalHossain/BD-IPTV/main/bd-iptv.m3u",
        "https://raw.githubusercontent.com/MohaiminIslam/Bangladesh-IPTV-List/main/bd.m3u",
        "https://raw.githubusercontent.com/byte-capsule/Fanai-Video-Player-Scripts/main/tv_channels.m3u",
        "https://iptv-org.github.io/iptv/countries/bd.m3u"
    ]
    
    channels_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for source in sources:
        try:
            print(f"Fetching from: {source}")
            response = requests.get(source, headers=headers, timeout=20)
            if response.status_code == 200:
                content = response.text
                # M3U ফরম্যাট থেকে নাম এবং লিঙ্ক বের করার রেগুলার এক্সপ্রেশন
                matches = re.findall(r'#EXTINF:.*?,(.*?)\n(http.*?)(?:\n|$)', content)
                
                for name, url in matches:
                    clean_name = name.strip()
                    clean_url = url.strip()
                    
                    if clean_name and clean_url:
                        channels_list.append({
                            "name": clean_name,
                            "url": clean_url
                        })
            else:
                print(f"Failed to load: {source} (Status: {response.status_code})")
        except Exception as e:
            print(f"Error fetching {source}: {e}")

    # ডুপ্লিকেট রিমুভ করা (একই নামের চ্যানেল একবারই থাকবে)
    unique_channels = {}
    for ch in channels_list:
        if ch['name'] not in unique_channels:
            unique_channels[ch['name']] = ch
            
    return list(unique_channels.values())

def update_json():
    all_channels = fetch_channels()
    
    # তোমার দেওয়া নির্দিষ্ট ফরম্যাট
    final_data = {
        "info": {
            "owner": "Rahul Islam",
            "total_channels": len(all_channels),
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M %p")
        },
        "channels": all_channels
    }
    
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    if len(all_channels) > 0:
        print(f"Success! {len(all_channels)} channels found and saved to channels.json.")
    else:
        print("Still getting 0 channels. Please check your internet connection or GitHub Action logs.")

if __name__ == "__main__":
    update_json()
