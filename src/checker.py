import socket
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def is_instagram_available(username):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    try:
        url = f"https://www.instagram.com/{username}/"
        driver.get(url)
        time.sleep(5)

        if "Instagram photos and videos" in driver.page_source:
            return False
        return True
    except Exception as e:
        print(f"Error checking Instagram for username '{username}': {e}", file=sys.stderr)
        return False
    finally:
        driver.quit()


def is_domain_available(domain):
    """Check if a domain is available using DNS."""
    try:
        socket.gethostbyname(domain)
        return False  # Domain exists
    except socket.gaierror:
        return True  # Domain does not exist
    except Exception as e:
        print(f"Error checking domain '{domain}': {e}", file=sys.stderr)
        return False


def main():
    for line in sys.stdin:
        word = line.strip()

        if word:  # Ignore empty lines
            try:
                instagram_available = is_instagram_available(word)
                domain_available = is_domain_available(f"{word}.com.br")

                if instagram_available and domain_available:
                    print(f'<a href="http://{word}.com.br/" target="_blank">{word}.com.br</a> | <a href="https://www.instagram.com/{word}/" target="_blank">instagram.com/{word}</a>', flush=True)
            except Exception as e:
                print(f"Unexpected error for word '{word}': {e}", file=sys.stderr)
            
            time.sleep(5)


if __name__ == "__main__":
    main()
