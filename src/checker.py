import requests
import socket
import sys
import time

def is_instagram_available(username):
    """Check if an Instagram username is available by parsing the HTML."""
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    if response.status_code == 200:
        user_id_start = response.text.find('"profilePage_', 0) + len('"profilePage_')
        user_id_end = response.text.find('"', user_id_start)
        user_id = response.text[user_id_start:user_id_end]
        return not user_id.isdigit()
    else:
        return None

def is_domain_available(domain):
    """Check if a domain is available using DNS."""
    try:
        socket.gethostbyname(domain)
        return False  # Domain exists
    except socket.gaierror:
        return True  # Domain does not exist

def main():
    for line in sys.stdin:
        word = line.strip()

        if word:  # Ignore empty lines
            instagram_available = is_instagram_available(word)
            domain_available = is_domain_available(f"{word}.com.br")

            if instagram_available and domain_available:
                print(word)
            
            time.sleep(2)

if __name__ == "__main__":
    main()
