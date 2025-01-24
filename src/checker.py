import socket
import sys
import time
import instaloader


def is_instagram_available(username):
    """Check if an Instagram username is available."""
    L = instaloader.Instaloader(save_metadata=False, quiet=True)
    try:
        L.context.max_connection_attempts = 1
        instaloader.Profile.from_username(L.context, username)
        return False  # Username exists
    except instaloader.exceptions.ProfileNotExistsException:
        return True  # Username is available
    except Exception as e:
        #print(f"Error checking username: {e}")
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
                print(word, flush=True)
            
            time.sleep(5)

if __name__ == "__main__":
    main()
