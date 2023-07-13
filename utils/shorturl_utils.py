import requests

def get_url_available(domain, path, model):
    code = [str(model.characters.index(character)) for character in path]
    code = int("".join(code))

    try:
        url = domain + path
        response = requests.get(url, timeout=10)
        response.encoding = "utf-8"
        status_code = response.status_code

        if (
            response.history
            and response.url != domain
            and path != model.id_state
        ):
            result = response.url[8:]
            if path != model.id_state:
                print(f"({status_code}) {url} -> https://{result}\n")
                model.response_list.append((path, status_code, result, code))

    except requests.exceptions.RequestException as e:
        print(f"\nError ({url}):", e)
