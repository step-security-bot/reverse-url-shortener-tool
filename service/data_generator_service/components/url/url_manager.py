from url import URL

class URLManager:

    def __init__(self):
        self.url_list = []

    def start(self):
        for url in self.url_list:
            characters = url.path_characters
            permutation = [0] * url.path_length
            for iteration in range(url.number_of_path_permutations):
                pass
                # TODO: generate permutations


                