import requests
import json
import re
from datetime import datetime

def fetch_channels():
    # সোর্স লিস্ট (তুমি চাইলে এখানে আরও সোর্স বাড়াতে পারো)
    sources = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/bd.m3u",
        "https://raw.githubusercontent.com/TofazzalHossain/BD-IPTV/main/bd-iptv.m3u"
    ]
    
    channels_list = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for source in sources:
        try:
            response = requests.get(source, headers=headers, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                for i in range(len(lines)):
                    if "#EXTINF" in lines[i]:
                        # চ্যানেল নাম ক্লিন করা
                        name = lines[i].split(',')[-1].strip()
                        
                        # লোগো এক্সট্রাকশন
                        logo = "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                        if 'tvg-logo="' in lines[i]:
                            logo = lines[i].split('tvg-logo="')[1].split('"')[0]
                        
                        # লিঙ্ক সংগ্রহ
                        url = ""
                        if i + 1 < len(lines) and lines[i+1].startswith('http'):
                            url = lines[i+1].strip()
                        
                        if url and name:
                            channels_list.append({
                                "name": name,
                                "url": url,
                                "logo": logo
                            })
        except Exception as e:
            print(f"Error skipping {source}")

    # ডুপ্লিকেট রিমুভ করা
    unique_channels = {ch['name']: ch for ch in channels_list}.values()
    return list(unique_channels)

def update_json():
    all_channels = fetch_channels()
    
    # তোমার দেওয়া নির্দিষ্ট ফরম্যাট অনুযায়ী ডাটা সাজানো
    final_data = {
        "info": {
            "owner": "Rahul Islam",
            "total_channels": len(all_channels),
            "last_update": datetime.now().strftime("%Y-%m-%d")
        },
        "channels": all_channels
    }
    
    # ফাইল সেভ করা
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"Success! {len(all_channels)} channels saved in your format.")

if __name__ == "__main__":
    update_json()
        
