import requests
import json
import concurrent.futures
from datetime import datetime

# Scanning settings
START_ID = 1
END_ID = 300000  # Gopal Bhar 209611 er moddhe thake
THREADS = 50     # Eksathe koiti ID check hobe (beshi dile fast hobe)

headers = {
    'User-Agent': 'Mozilla/5.0 (Android 11; Mobile; rv:128.0) Gecko/128.0 Firefox/128.0',
    'Referer': 'https://tplay.live/',
    'Origin': 'https://tplay.live'
}

base_url = "https://cloudfrontnet.vercel.app/tplay/playout/"
found_channels = []

def check_id(ch_id):
    m3u8_url = f"{base_url}{ch_id}/master.m3u8"
    try:
        # Timeout 2 second jate bondho channel e somoy nosto na hoy
        response = requests.head(m3u8_url, headers=headers, timeout=2)
        if response.status_code == 200 or response.status_code == 302:
            print(f"✅ Active ID Found: {ch_id}")
            return {
                "name": f"Channel {ch_id}",
                "url": m3u8_url,
                "logo": f"https://www.tataplay.com/cms-assets/s3fs-public/logos/{ch_id}.png"
            }
    except:
        return None
    return None

def start_scanning():
    print(f"Scanning shuru hocche {START_ID} theke {END_ID} porjonto...")
    
    # Multithreading bebohar kora hocche jate loop fast hoy
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(check_id, range(START_ID, END_ID)))
    
    # Shudhu valid channel gula ke filter kora
    final_list = [res for res in results if res is not None]
    
    # Gopal Bhar (209611) pawa gele ota list e thakbe
    output = {
        "info": {
            "owner": "Islam Rahul",
            "total_found": len(final_list),
            "last_scan": datetime.now().strftime("%Y-%m-%d %I:%M %p")
        },
        "channels": final_list
    }

    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nScan complete! Mot {len(final_list)} ti active channel pawa geche.")

if __name__ == "__main__":
    start_scanning()
