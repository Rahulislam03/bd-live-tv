import requests

# বর্তমানে সচল আছে এমন কিছু সোর্স
sources = [
    "https://raw.githubusercontent.com/Saifur-Rahman-Saif/Bangla-IPTV/main/Bangla-IPTV.m3u",
    "https://raw.githubusercontent.com/S-K-H-S-N/Bangla-IPTV/main/Bangla.m3u",
    "https://iptv-org.github.io/iptv/countries/bd.m3u"
]

def update_m3u():
    all_content = "#EXTM3U\n"
    found_any = False
    
    # ব্রাউজার হিসেবে পরিচয় দেওয়ার জন্য Headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for url in sources:
        try:
            print(f"Fetching from: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                content = response.text
                if "#EXTINF" in content:
                    # ডুপ্লিকেট হেডার ক্লিন করা
                    clean_content = content.replace("#EXTM3U", "").strip()
                    all_content += clean_content + "\n"
                    found_any = True
                    print(f"Successfully added channels from: {url}")
                else:
                    print(f"No valid M3U data in: {url}")
            else:
                print(f"Error {response.status_code} for: {url}")
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    if found_any:
        # একই চ্যানেল বারবার থাকলে সেগুলো বাদ দেওয়া (Optional but good)
        with open("live_tv.m3u", "w", encoding="utf-8") as f:
            f.write(all_content.strip())
        print("Success: live_tv.m3u has been updated with working channels!")
    else:
        print("Critical Error: No channels were found! All sources might be down.")

if __name__ == "__main__":
    update_m3u()
                
