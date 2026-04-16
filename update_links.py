import requests
import json
import re
from datetime import datetime

def fetch_channels():
    # তোমার দেওয়া সোর্স এবং সার্ভার ইনডেক্সগুলো এখানে অ্যাড করা হয়েছে
    sources = [
        "https://raw.githubusercontent.com/byte-capsule/Fanai-Video-Player-Scripts/main/tv_channels.m3u",
        "https://raw.githubusercontent.com/tuhin-shubhra/bd-iptv/main/bd-iptv.m3u",
        "https://raw.githubusercontent.com/MohaiminIslam/Bangladesh-IPTV-List/main/bd.m3u",
        "https://raw.githubusercontent.com/TofazzalHossain/BD-IPTV/main/bd-iptv.m3u"
    ]
    
    channels_list = []
    # nCare এবং BozzTV সার্ভারের জন্য হেডার মাস্ট
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': 'https://bozztv.com/'
    }
    
    for source in sources:
        try:
            response = requests.get(source, headers=headers, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                for i in range(len(lines)):
                    if "#EXTINF" in lines[i]:
                        # নাম এক্সট্রাক্ট করা
                        name_match = re.search(r',(.+)$', lines[i])
                        name = name_match.group(1).strip() if name_match else ""
                        
                        # লিঙ্ক এক্সট্রাক্ট করা
                        url = ""
                        if i + 1 < len(lines) and lines[i+1].startswith('http'):
                            url = lines[i+1].strip()
                        
                        # তোমার দেওয়া সার্ভারগুলোর লিঙ্ক কি না তা চেক করা
                        # BozzTV, nCare, Vercel/T-Play, Amagi
                        target_servers = ['bozztv.com', 'ncare.live', 'vercel.app', 'amagi.tv', 'sonarbanglatv.com']
                        
                        if url and name:
                            # যদি লিঙ্কটি তোমার টার্গেট সার্ভারের হয় অথবা বাংলাদেশি চ্যানেল হয়
                            if any(server in url for server in target_servers) or "TV" in name.upper():
                                channels_list.append({
                                    "name": name,
                                    "url": url
                                })
        except Exception as e:
            print(f"Skipping source due to error: {source}")

    # ডুপ্লিকেট নাম এবং লিঙ্ক ফিল্টার করা
    unique_data = []
    seen_names = set()
    for ch in channels_list:
        if ch['name'] not in seen_names:
            unique_data.append(ch)
            seen_names.add(ch['name'])
            
    return unique_data

def update_json():
    all_channels = fetch_channels()
    
    final_json = {
        "info": {
            "owner": "Rahul Islam",
            "total_channels": len(all_channels),
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "channels": all_channels
    }
    
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully updated {len(all_channels)} channels from core servers!")

if __name__ == "__main__":
    update_json()
            
