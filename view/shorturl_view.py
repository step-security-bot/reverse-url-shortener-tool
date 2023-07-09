class ShortURLView:
    def __init__(self, controller):
        self.controller = controller

    def start(self, domain_option):
            self.controller.generate_short_url()
        # try:
        #     self.controller.generate_short_url()
        # except Exception as e:
        #     print("Error:", e)
