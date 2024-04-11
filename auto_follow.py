import requests
import json
from colorama import init, Fore
import time
from fake_useragent import UserAgent

# Initialize colorama
init(autoreset=True)

# Meminta masukan token Authorization dari pengguna
authorization_token = input("Masukkan token Authorization: ")

# Generate a fake user agent
ua = UserAgent()
fake_user_agent = ua.random

headers = {
    'User-Agent': fake_user_agent,
    'Authorization': f'Bearer {authorization_token}',
    'Content-Type': 'application/json'
}

# Daftar untuk menyimpan ID channel yang sudah difollow
followed_channels = []

response = requests.get('https://api.warpcast.com/v2/all-channels', headers=headers)
data = json.loads(response.text)

for channel in data['result']['channels']:
    # Check if 'leadFid' key exists in the channel dictionary
    if 'leadFid' not in channel:
        print(Fore.RED + f"Channel {channel['id']} does not have 'leadFid' key.")
        continue

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
    except requests.exceptions.HTTPError as e:
        print(Fore.RED + f"Failed to follow channel with name {channel['id']}. HTTP error occurred:", e.response.status_code)
        print(e.response.text)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + f"Failed to follow channel with name {channel['id']}. JSON decoding error:", e)
    except Exception as e:
        print(Fore.RED + f"Failed to follow channel with name {channel['id']}. An unexpected error occurred:", e)
    
    time.sleep(5)  # Jeda selama 5 detik
