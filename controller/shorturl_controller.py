from model.shorturl_model import ShortURLModel

class ShortURLController:
    def __init__(self, domain, domain_length, characters):
        self.model = ShortURLModel(domain, domain_length, characters)

    def generate_short_url(self) -> None:
        self.model.start_process()
