#
# Author: Meyer Pidiache <meyer.pidiache@gmail.com>
# Co-Authors: ChatGTP 3.5, Debugcode.ai
#

import random
import requests
import string

# SHORTURL_DOMAIN = 'https://www.shorturl.at/'
SHORTURL_DOMAIN = 'https://t.ly/'


def generate_random_path(length=5):
    """Generate a random alphanumeric string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def main():
    """Main function to find available short URLs."""
    print("Searching for available short URLs...\n")
    
    for _ in range(500):
        path = generate_random_path(4)
        url = SHORTURL_DOMAIN + path

        try:
            response = requests.get(url)
            response.raise_for_status() # raise exception if status code >= 400
        except requests.exceptions.RequestException as e:
            print(f"Error: {e} ({url})\n")
            continue

        if response.history and response.url != SHORTURL_DOMAIN:
            print(f'{url} -> {response.url}\n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nUser interruption. Exiting...")

