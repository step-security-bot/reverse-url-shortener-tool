from components.url.url import URL
from components.url.url_manager import URLManager
from database.database_connection import Database
from utils.constants import SHORTURL_DOMAINS


def main():
    global url_manager
    database = Database()

    domain_option = 1
    domain = SHORTURL_DOMAINS[domain_option][0]
    path_length = SHORTURL_DOMAINS[domain_option][1]

    url = URL(domain, path_length)
    url_manager = URLManager(url, database)

    url_manager.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("#" * 94, "executor.shutdown(cancel_futures=True)\n")
        url_manager.executor.shutdown(cancel_futures=True)
        print("*" * 94, "database.conn.close()")
        url_manager.database.conn.close()
        print("&" * 94, "Done!")
        exit()
