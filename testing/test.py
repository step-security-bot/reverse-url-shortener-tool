import asyncio
import aiohttp
import random
import string

SHORTURL_DOMAINS = {
    "https://t.ly/": 4,
    # "https://shorturl.lol/": 4,
    # "https://www.shorturl.at/": 5,
    # "https://tinyurl.com/": 6,
}

MAX_ITERATIONS = 2
CHARACTERS = string.ascii_letters + string.digits
DELAY_RANGE = (0.5, 1.5)  # Set your desired range of delay in seconds


def generate_random_path(length):
    """Generate a random alphanumeric string of given length."""
    return "".join(random.choices(CHARACTERS, k=length))


def generate_path_list(seed):
    """Use a seed to create a list of paths"""
    url_list = []
    for i in seed:
        for j in CHARACTERS:
            new = seed.replace(i, j)
            url_list.append(new)
    return url_list


async def check_url_available(session, url):
    """Check if a short URL is available."""
    try:
        async with session.head(url) as response:
            if response.status == 200:
                if response.history and response.url != url:
                    return f"{url} -> {response.url}\n"
            print(response.status)
    except aiohttp.ClientError:
        pass
    return None


async def main():
    """Main function to find available short URLs."""

    print("Searching for available short URLs...\n")

    # Configure the HTTP client
    connector = aiohttp.TCPConnector(limit=30)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        # Create an empty list to store the tasks that we will submit to the event loop
        tasks = []

        for _ in range(MAX_ITERATIONS):
            for domain, path_length in SHORTURL_DOMAINS.items():
                path = generate_random_path(path_length)

                # Submit a task to the event loop to check if the short URL formed by the domain and path is available
                tasks.append(
                    asyncio.create_task(check_url_available(session, domain + path))
                )

                # Generate a list of all possible variations of the path by replacing each character with a different one
                for i in generate_path_list(path):
                    # Submit a task to the event loop to check if each variation of the short URL is available
                    tasks.append(
                        asyncio.create_task(check_url_available(session, domain + i))
                    )

        # Loop over each completed task in the list of tasks
        for task in asyncio.as_completed(tasks):
            # Get the result of the completed task
            result = await task

            # If the result is not None (i.e. a short URL was found), print it to the console
            if result is not None:
                print(result)

            # Sleep for a random amount of time between each request to avoid rate limiting
            delay = random.uniform(*DELAY_RANGE)
            await asyncio.sleep(delay)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nUser interruption. Exiting...")
