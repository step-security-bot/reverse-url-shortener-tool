#
# Author: Meyer Pidiache <meyer.pidiache@gmail.com>
# Co-Authors: ChatGTP 3.5, Debugcode.ai
#

import concurrent.futures
import random
import requests
import string


SHORTURL_DOMAINS = {
    "https://t.ly/": 4,
    # "https://shorturl.lol/": 4,
    # "https://rb.gy/": 5,
    # "https://www.shorturl.at/": 5,
    # "https://tinyurl.com/": 6,
}

MAX_ITERATIONS = 1
CHARACTERS = string.ascii_letters + string.digits


def generate_random_path(length):
    """Generate a random alphanumeric string of given length."""
    return "".join(random.choices(CHARACTERS, k=length))


def get_url_available(domain, path):
    """Check if a short URL is available."""
    try:
        url = domain + path
        response = requests.get(url, timeout=10)
        response.encoding = "utf-8"
        status_code = response.status_code
        if response.history and response.url != domain and not 400 <= status_code < 500:
            return f"{status_code}. {url} -> {response.url}\n"
    except requests.exceptions.RequestException:
        pass
    return None


def get_path_list(seed):
    """Use a seed to create a list of paths"""
    urlList = list()
    for i in seed:
        for j in CHARACTERS:
            new = seed.replace(i, j)
            urlList.append(new)
    return urlList


def main():
    """Main function to find available short URLs."""

    print("Searching for available short URLs...\n")

    # Create a ThreadPoolExecutor instance that will allow us to run multiple tasks concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Create an empty list to store the futures (i.e. tasks) that we will submit to the executor
        futures = []

        for _ in range(MAX_ITERATIONS):
            for domain, path_length in SHORTURL_DOMAINS.items():
                path = generate_random_path(path_length)

                # Submit a task to the executor to check if the short URL formed by the domain and path is available
                futures.append(executor.submit(get_url_available, domain, path))

                # Generate a list of all possible variations of the path by replacing each character with a different one
                for i in get_path_list(path):
                    # Submit a task to the executor to check if each variation of the short URL is available
                    futures.append(executor.submit(get_url_available, domain, i))

        # Loop over each completed future (i.e. task) in the list of futures
        for future in concurrent.futures.as_completed(futures):
            # Get the result of the completed future
            result = future.result()

            # If the result is not None (i.e. a short URL was found), print it to the console
            if result is not None:
                print(result)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nUser interruption. Exiting...")
