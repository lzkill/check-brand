import socket
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType


def is_instagram_available(username, proxy_address=None):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # SOCKS5 proxy
    if proxy_address:
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.socks_proxy = proxy_address
        prox.socks_version = 5
        options.proxy = prox

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


def is_domain_available(username, domain):
    """Check if a domain is available using DNS."""
    try:
        socket.gethostbyname(f"{username}.{domain}")
        return False  # Domain exists
    except socket.gaierror:
        return True  # Domain does not exist
    except Exception as e:
        print(f"Error checking domain '{username}.{domain}': {e}", file=sys.stderr)
        return False


def get_available_domain(word):
    """Check if domains are available."""
    if is_domain_available(f"{word}", "com.br"):
        return "com.br"
    elif is_domain_available(f"{word}", "shop"):
        return "shop"
    return None


def main(): 
    try:
        for line in sys.stdin:
            word = line.strip()

            if word:  # Ignore empty lines
                try:
                    is_instagram_available = is_instagram_available(word)
                    available_domain = get_available_domain(word)

                    if is_instagram_available and available_domain:
                        print(
                            f'<a href="http://{word}.{available_domain}/" target="_blank">{word}.{available_domain}</a> | '
                            f'<a href="https://www.instagram.com/{word}/" target="_blank">instagram.com/{word}</a><br>',
                            flush=True,
                        )
                        print()  # For human readability if reviewing the file directly
                except Exception as e:
                    print(f"Unexpected error for word '{word}': {e}", file=sys.stderr)
                
                time.sleep(5)
    except KeyboardInterrupt:
        sys.exit(0)  # Exit cleanly


if __name__ == "__main__":
    main()
