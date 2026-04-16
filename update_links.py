import requests

# নতুন এবং কার্যকরী কিছু সোর্স লিঙ্ক
sources = [
    "https://raw.githubusercontent.com/byte-capsule/gj_ts_m3u/main/gj_ts.m3u",
    "https://raw.githubusercontent.com/MohammadSiam/bangla-iptv/main/bangla-iptv.m3u",
    "https://raw.githubusercontent.com/arshun/TV/master/Bangla.m3u"
]

def update_m3u():
    all_content = "#EXTM3U\n"
    found_any = False
    
    for url in sources:
        try:
            print(f"Fetching from: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                content = response.text
                # ফাইলটি যদি খালি না থাকে
                if "#EXTINF" in content:
                    # মেইন কন্টেন্ট থেকে এক্সট্রা #EXTM3U থাকলে সরিয়ে ফেলা
                    clean_content = content.replace("#EXTM3U", "").strip()
                    all_content += clean_content + "\n"
                    found_any = True
                    print(f"Successfully added channels from: {url}")
                else:
                    print(f"No channels found in: {url}")
            else:
                print(f"Error {response.status_code} for: {url}")
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    if found_any:
        with open("live_tv.m3u", "w", encoding="utf-8") as f:
            f.write(all_content.strip())
        print("Success: live_tv.m3u has been updated with channels!")
    else:
        print("Critical Error: No channels were found in any source!")

if __name__ == "__main__":
    update_m3u()
        
