from model.shorturl_model import ShortURLModel

class ShortURLController:
    def __init__(self, domain, domain_length, characters):
        self.model = ShortURLModel(domain, domain_length, characters)

    def generate_short_url(self) -> None:
        try:
            self.model.start_process()
        except Exception as e:
            print(f"Controller: {e}")
            data = self.model.response_list
            self.model.response_list.clear()
            self.model.save_state(data)
            self.model.executor.shutdown(cancel_futures=True)
            exit()
