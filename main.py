from argparse import ArgumentParser
from string import ascii_letters, digits

from controller.shorturl_controller import ShortURLController
from view.shorturl_view import ShortURLView

def main():
    CHARACTERS = ascii_letters + digits
    SHORTURL_DOMAINS = {
        1: ["https://t.ly/", 4],
        2: ["https://rb.gy/", 5],
        3: ["https://www.shorturl.at/", 5],
        4: ["https://tinyurl.com/", 6],
    }

    # Configurar el análisis de argumentos
    parser = ArgumentParser()
    parser.add_argument("-d", "--domain_option", type=int, help="Opción de dominio (1-4)")
    args = parser.parse_args()

    # Obtener la opción de dominio del argumento
    domain_option = args.domain_option

    # Verificar si se proporcionó la opción de dominio
    if domain_option is None:
        parser.error("Debe proporcionar una opción de dominio (-d / --domain_option)")
    
    if domain_option not in SHORTURL_DOMAINS:
        parser.error("Opción de dominio inválida")
    
    domain = SHORTURL_DOMAINS[domain_option][0]
    domain_length = SHORTURL_DOMAINS[domain_option][1]

    controller = ShortURLController(domain, domain_length, CHARACTERS) # Domain option, para globalizar
    view = ShortURLView(controller)
    
    view.start(domain_option)


if __name__ == "__main__":
    main()