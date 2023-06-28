from flask import Flask, redirect, request
import time

app = Flask(__name__)

@app.route('/')
def index(path):
    return "Hello World!"

def get_url_available(domain, path):
    """Comprueba si una URL corta está disponible."""
    try:
        url = domain + path

        response = requests.get(url, timeout=10)

        response.encoding = "utf-8"

        # response.raise_for_status()  # raise exception if status code >= 400

        if response.history and response.url != domain:
            return f"{url} -> {response.url}\n"

    except requests.exceptions.RequestException:
        pass

    return None

if __name__ == "__main__":
    # while True:
    get_url_available("https://meyer-s-store.vercel.app/", "top-secret")
        # time.sleep(60)