from argparse import ArgumentParser

from controller.shorturl_controller import ShortURLController
from view.shorturl_view import ShortURLView
from utils.constants import SHORTURL_DOMAINS

def main():

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

    controller = ShortURLController(domain, domain_length)
    view = ShortURLView(controller)
    
    view.start(domain_option)


if __name__ == "__main__":
    main()
    