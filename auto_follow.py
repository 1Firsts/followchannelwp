import requests
import json
from colorama import init, Fore
import time

# Initialize colorama
init(autoreset=True)

# Meminta masukan token Authorization dari pengguna
authorization_token = input("Masukkan token Authorization: ")

headers = {
    'authority': 'api.warpcast.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Authorization': f'Bearer {authorization_token}'  # Gunakan token Authorization yang dimasukkan pengguna
}

# Daftar untuk menyimpan ID channel yang sudah difollow
followed_channels = []

response = requests.get(
    'https://api.warpcast.com/v2/all-channels', headers=headers)
data = json.loads(response.text)

for channel in data['result']['channels']:
    output = {
        "id": channel['id'],
        "url": f"https://warpcast.com/~/channel/{channel['id']}",
        "name": channel['name'],
        "description": channel['description'],
        "imageUrl": channel['imageUrl'],
        "leadFid": channel['leadFid'],
        "createdAt": channel['createdAt']
    }

    # Periksa apakah channel sudah difollow sebelumnya
    if channel['id'] in followed_channels:
        print(Fore.YELLOW + f"Channel {channel['id']} sudah difollow sebelumnya.")
        continue

    try:
        response = requests.put(
            'https://client.warpcast.com/v2/feed-follows', headers=headers, json={"feedKey": channel['id']})
        response.raise_for_status()  # Raise an exception for bad responses
        print(Fore.GREEN + f"Successfully followed channel with name {channel['id']}:")
        print(json.dumps(output, indent=4))
        print("------------------------")
        
        # Tambahkan ID channel ke dalam daftar
        followed_channels.append(channel['id'])
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Failed to follow channel with name {channel['id']}. Request failed:", e)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + f"Failed to follow channel with name {channel['id']}. JSON decoding error:", e)
    
    time.sleep(5)  # Jeda selama 5 detik
