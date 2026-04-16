import requests
import json
import re

# সোর্স ইউআরএল
M3U_URL = "https://raw.githubusercontent.com/abusaeeidx/M3u8-URL-Extractor-from-Live-Server/master/IPTV.m3u"

def fetch_and_convert():
    try:
        response = requests.get(M3U_URL, timeout=15)
        if response.status_code != 200: return
        
        lines = response.text.split('\n')
        channels = []
        current_name = ""
        current_logo = ""
        current_group = ""

        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF:'):
                # নাম, লোগো এবং গ্রুপ এক্সট্র্যাক্ট করা
                name_match = re.search(r',(.+)', line)
                logo_match = re.search(r'tvg-logo="([^"]+)"', line)
                group_match = re.search(r'group-title="([^"]+)"', line)
                
                current_name = name_match.group(1) if name_match else "Unknown Channel"
                current_logo = logo_match.group(1) if logo_match else ""
                current_group = group_match.group(1) if group_match else "General"
                
            elif line.startswith('http'):
                channels.append({
                    "name": current_name,
                    "url": line,
                    "logo": current_logo,
                    "group": current_group
                })

        # JSON ফাইল হিসেবে সেভ করা
        with open('channels.json', 'w', encoding='utf-8') as f:
            json.dump({"channels": channels}, f, indent=4, ensure_ascii=False)
        
        print(f"Successfully updated {len(channels)} channels!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_convert()
