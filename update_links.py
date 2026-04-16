import requests
import json
import re

def fetch_channels():
    # গিটহাব বাদেও আরও ডাইনামিক সোর্স অ্যাড করা হয়েছে
    sources = [
        # GitHub Sources
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/bd.m3u",
        "https://raw.githubusercontent.com/TofazzalHossain/BD-IPTV/main/bd-iptv.m3u",
        "https://raw.githubusercontent.com/MohaiminIslam/Bangladesh-IPTV-List/main/bd.m3u",
        
        # External IPTV Index Sources (Public APIs/Lists)
        "https://iptv-org.github.io/iptv/countries/bd.m3u",
        "http://m3u.cl/playlist/BD.m3u"
    ]
    
    channels_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for source in sources:
        try:
            # সোর্স থেকে ডাটা রিকোয়েস্ট করা
            response = requests.get(source, headers=headers, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                for i in range(len(lines)):
                    if "#EXTINF" in lines[i]:
                        # চ্যানেল নাম ক্লিন করা
                        name_match = re.search(r',(.+)$', lines[i])
                        name = name_match.group(1).strip() if name_match else "Unknown"
                        
                        # লোগো এক্সট্রাকশন
                        logo = ""
                        logo_match = re.search(r'tvg-logo="([^"]+)"', lines[i])
                        if logo_match:
                            logo = logo_match.group(1)
                        
                        # পরবর্তী লাইনে থাকা লিঙ্ক সংগ্রহ
                        url = ""
                        if i + 1 < len(lines) and lines[i+1].startswith('http'):
                            url = lines[i+1].strip()
                        
                        if url and name != "Unknown":
                            channels_list.append({
                                "name": name,
                                "url": url,
                                "logo": logo if logo else "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                            })
        except Exception as e:
            print(f"Error skipping {source}: {e}")

    # ডুপ্লিকেট চ্যানেল ফিল্টার (নামের ওপর ভিত্তি করে)
    unique_channels = {}
    for ch in channels_list:
        if ch['name'] not in unique_channels:
            unique_channels[ch['name']] = ch
    
    return list(unique_channels.values())

def update_json():
    new_channels = fetch_channels()
    
    if new_channels:
        # তোমার চ্যানেলের ডাটা স্ট্রাকচার
        data = {
            "info": {
                "owner": "Rahul Islam",
                "total": len(new_channels),
                "last_updated": "2026-04-17"
            },
            "channels": new_channels
        }
        
        # ফাইল সেভ করা
        with open('channels.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Update Success! {len(new_channels)} channels added.")
    else:
        print("Update Failed: No data found.")

if __name__ == "__main__":
    update_json()
                            
