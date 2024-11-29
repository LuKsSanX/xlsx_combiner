import os
import logging

from .pastas import Pasta, Pastas


def setup() -> None:
    logging.getLogger().setLevel(logging.DEBUG)

    caminho_local = os.path.abspath(os.path.dirname(__file__))
    logging.debug(f"caminho_local: {caminho_local}")
    logging.info("Verificando pastas")

    pastas = Pastas(caminho_local)
    verificar_pastas(pastas)


def verificar_pastas(pastas: Pastas | list[Pasta]) -> None:
    pastas = list(pastas)

    if len(pastas) < 1:
        return

    pasta = pastas.pop()
    caminho = pasta.caminho
    pasta_existe = os.path.exists(caminho)

    if pasta_existe:
        logging.debug(f"{caminho} ja existe")
    else:
        logging.debug(f"{caminho} nao existe")
        criar_pasta(caminho)

    return verificar_pastas(pastas)


def criar_pasta(pasta: str) -> None:
    logging.debug(f"{pasta} criando")
    try:
        os.mkdir(pasta)
        logging.debug(f"{pasta} criado")
    except Exception as erro:
        logging.error(f"{pasta} nao criado: {erro}")


if __name__ == "__main__":
    setup()
