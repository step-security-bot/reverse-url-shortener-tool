import requests

from utils.constants import CHARACTERS

class URL:

    def __init__(self, domain: str, path_length: int):
        self.domain = domain
        self.path_length = path_length
        self.path_characters:str = CHARACTERS
        self.number_of_path_permutations:int = len(self.path_characters) ** self.path_length
        self.current_path:str = None
        self.current_id:int = 0

    def set_current_path_by_permutation_notation(self, permutation_notation: list[int]) -> str:
        # permutation_notation = [int, int, ..., int]
        self.current_path = "".join([self.path_characters[position] for position in permutation_notation])
        self.current_id += 1

    def get_redirect_url(self, path):

        url = f"https://{self.domain}/{path}"

        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"\nError ({url}):", e)
            return

        response.encoding = "utf-8"
        status_code = response.status_code

        if (
            response.history
            and response.url != self.domain
        ):
            result = response.url[8:]
            print(f"({status_code}) {url} -> https://{result}\n")
