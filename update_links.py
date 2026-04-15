import requests

# এখানে সেইসব সোর্স লিঙ্ক দাও যেগুলো নিয়মিত আপডেট হয়
sources = [
    "https://raw.githubusercontent.com/byte-capsule/gj_ts_m3u/main/gj_ts.m3u",
    "https://raw.githubusercontent.com/MohammadSiam/bangla-iptv/main/bangla-iptv.m3u"
]

def update_m3u():
    all_content = "#EXTM3U\n"
    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # প্রথম লাইন (#EXTM3U) বাদ দিয়ে বাকিটুকু নেওয়া হচ্ছে
                content = response.text.replace("#EXTM3U", "").strip()
                all_content += content + "\n"
        except:
            print(f"Failed to fetch: {url}")

    with open("live_tv.m3u", "w", encoding="utf-8") as f:
        f.write(all_content)
    print("M3U Playlist Updated!")

if __name__ == "__main__":
    update_m3u()
