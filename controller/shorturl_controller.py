from model.shorturl_model import ShortURLModel

class ShortURLController:
    def __init__(self, domain, domain_length):
        try:
            ShortURLModel(domain, domain_length)
        except Exception as e:
            print(e)
            exit()

        self.model = ShortURLModel(domain, domain_length)

    def generate_short_url(self) -> None:
        try:
            self.model.start_process()
        except Exception as e:
            print(f"Controller: {e}")
            self.model.save_state()
            