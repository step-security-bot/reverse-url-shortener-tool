import requests

from utils.constants import CHARACTERS


class URL:
    def __init__(self, domain: str, path_length: int):
        self.domain = domain
        self.path_length = path_length
        self.path_characters: str = CHARACTERS
        self.current_path: str = None
        self.current_id: int = 0

        self.current_permutation_notation = []
        self.number_of_path_permutations: int = (
            len(self.path_characters) ** self.path_length
        )

    def get_redirect_url(self, id: int, path: str, url_manager):
        url = f"https://{self.domain}/{path}"

        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"\nError ({url}):", e)
            return

        response.encoding = "utf-8"
        status_code = response.status_code

        if response.history and response.url != self.domain:
            redirect_url = response.url[8:]
            # print(f"{id}. ({status_code}) {url} -> https://{redirect_url}\n")
            url_manager.add_url_data((id, path, status_code, redirect_url))
