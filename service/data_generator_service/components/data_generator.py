from database.database_connection import Database
from components.url.url import URL
from components.url.url_manager import URLManager
from utils.constants import SHORTURL_DOMAINS

class DataGenerator:
    def __init__(self):
        self.domain_option = 1
        self.domain = SHORTURL_DOMAINS[self.domain_option][0]
        self.path_length = SHORTURL_DOMAINS[self.domain_option][1]

        self.url = URL(self.domain, self.path_length)
        self.url_manager = URLManager(self.url)
        self.database = Database()

    def start(self):
        self.url_manager.start()
        