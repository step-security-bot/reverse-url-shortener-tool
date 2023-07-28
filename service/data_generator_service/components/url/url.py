from utils.constants import CHARACTERS

class URL:

    def __init__(self, domain: str, path_length: int):
        self.domain = domain
        self.path_length = path_length
        self.path_characters:str = CHARACTERS
        self.number_of_path_permutations:int = len(self.path_characters) ** self.path_length
        self.current_path:str = None

    def get_url_by_permutation_notation(self, permutation_notation: list[int]) -> str:
        # permutation_notation = [int, int, ..., int]
        self.path = "".join([self.path_characters[position] for position in permutation_notation])

        return f"https://{self.domain}/{self.path}"
