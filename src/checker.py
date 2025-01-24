import socket
import sys
import time
import instaloader
import tempfile


def is_instagram_available(username):
    """Check if an Instagram username is available."""
    with tempfile.TemporaryDirectory() as temp_dir:
        L = instaloader.Instaloader(save_metadata=False, quiet=True)
        try:
            # Try to fetch the profile with the username
            L.context.max_connection_attempts = 1
            L.download_profile(username)
            return False
        except Exception:
            return True

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
