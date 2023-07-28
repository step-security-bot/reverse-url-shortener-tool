from decouple import config as getenv

from utils.constants import SHORTURL_DOMAINS
from data_generator import DataGenerator

def main():
    
    domain_option = 1
    domain = SHORTURL_DOMAINS[domain_option][0]
    path_length = SHORTURL_DOMAINS[domain_option][1]

    data_generator = DataGenerator()
    data_generator.start()

    print(getenv("APP_DEBUG"))

if __name__ == "__main__":
    main()
    