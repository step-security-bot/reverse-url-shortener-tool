#
# Author: Meyer Pidiache <meyer.pidiache@gmail.com>
# Co-Authors: ChatGTP 3.5, Debugcode.ai
#

import random
import requests
import string

'''Domain, Path length '''
SHORTURL_DOMAINS = {
    "https://t.ly/": 4,
    # "https://shorturl.lol/": 4,
    # "https://www.shorturl.at/": 5,
    # "https://tinyurl.com/": 6,
}
MAX_ITERATIONS = 100


def generate_random_path(length):
    """Generate a random alphanumeric string of given length."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def get_url_available(domain, path):
    """Check if a short URL is available."""
    try:
        url = domain + path
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()  # raise exception if status code >= 400
        if response.history and response.url != domain:
            print(f"{url} -> {response.url}\n")
    except requests.exceptions.RequestException:
        pass


def main():
    """Main function to find available short URLs."""
    print("Searching for available short URLs...\n")

    for _ in range(MAX_ITERATIONS):
        for domain, path_length in SHORTURL_DOMAINS.items():
            path = generate_random_path(path_length)
            get_url_available(domain, path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nUser interruption. Exiting...")
