import requests
from colorama import init, Fore, Style
import time

# Initialize colorama
init(autoreset=True)

# Meminta masukan token Authorization dari pengguna
authorization_token = input("Masukkan token Authorization: ")

headers = {
    'Authorization': f'Bearer {authorization_token}',
    'Content-Type': 'application/json'
}

# Daftar untuk menyimpan ID channel yang sudah difollow
followed_channels = []

def get_all_channels():
    response = requests.get('https://api.warpcast.com/v2/all-channels', headers=headers)
    response.raise_for_status()
    return response.json()['result']['channels']

def follow_channel(channel_id):
    url = 'https://api.warpcast.com/v2/feed-follows'
    data = {"feedKey": channel_id}
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()

def read_saved_channels():
    try:
        with open('channels.txt', 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def follow_channels():
    saved_channels = read_saved_channels()
    channels = get_all_channels()
    with open('channels.txt', 'a', encoding='utf-8') as file:  # Use 'a' to append instead of 'w'
        for channel in channels:
            if 'leadFid' not in channel:
                print(Fore.RED + f"Channel {channel['id']} does not have 'leadFid' key.")
                continue

            if channel['id'] in followed_channels:
                print(Fore.YELLOW + f"Channel {channel['id']} sudah difollow sebelumnya.")
                continue

            if channel['name'] in saved_channels:
                print(Fore.YELLOW + f"Channel {channel['name']} sudah ada di dalam file channels.txt.")
                continue

            try:
                follow_channel(channel['id'])
                print(Fore.GREEN + f"{Style.BRIGHT}[✔] Successfully followed channel:")
                print(f"    Name: {Fore.CYAN}{channel['name']}")
                print(f"    ID: {Fore.CYAN}{channel['id']}")
                print(f"    URL: {Fore.CYAN}{channel['url']}")
                file.write(f"{channel['name']}\n")  # Write name without timestamp
                followed_channels.append(channel['id'])
                print(Fore.YELLOW + "---------------------------------------------------")
                time.sleep(5)
            except requests.exceptions.HTTPError as e:
                print(Fore.RED + f"[✘] Failed to follow channel {channel['id']}. HTTP error occurred:", e.response.status_code)
                print(e.response.text)
            except Exception as e:
                print(Fore.RED + f"[✘] Failed to follow channel {channel['id']}. An unexpected error occurred:", e)
    print(Fore.GREEN + "Data channel telah diperbarui dan disimpan ke dalam file 'channels.txt'.")

def main_menu():
    while True:
        print("\n" + Fore.YELLOW + Style.BRIGHT + "Menu:")
        print(Fore.YELLOW + "1. Follow all channels")
        print(Fore.YELLOW + "2. Exit")
        choice = input(Fore.CYAN + "Enter your choice: ")

        if choice == '1':
            follow_channels()
        elif choice == '2':
            print(Fore.GREEN + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
