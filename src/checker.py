import requests
import socks
import socket
import sys
import time

# Configuration
PROXY_HOST = "localhost"
PROXY_PORT = 1338  # Replace with your SOCKS5 proxy port

# Set up SOCKS5 proxy
socks.set_default_proxy(socks.SOCKS5, PROXY_HOST, PROXY_PORT)
socket.socket = socks.socksocket

def is_instagram_available(username):
    """Check if an Instagram username is available by parsing the HTML."""
    url = f"https://www.instagram.com/{username}/"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if "Sorry, this page isn't available." in response.text:
                return True
            return False
        return response.status_code == 404
    except requests.RequestException:
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
                print(word)
            
            time.sleep(2)

if __name__ == "__main__":
    main()
