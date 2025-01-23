import requests
import socket
import sys
import time
from bs4 import BeautifulSoup
from datetime import datetime


def is_instagram_available(username):
    """Check if an Instagram username is available by parsing the HTML."""
    url = f"https://www.instagram.com/{username}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find_all('meta', property="og:title")[-1] if soup.find_all('meta', property="og:title") else None
            if not title_tag:
                return True
        return False
    except requests.exceptions.RequestException:
        return False

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
                print(word, flush=True)
            
            time.sleep(2)

if __name__ == "__main__":
    main()
