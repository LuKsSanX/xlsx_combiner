import os


class Pastas:
    def __init__(self, caminho_local: str) -> None:
        self.entrada = Pasta(f"{caminho_local}/entrada")
        self.erros = Pasta(f"{caminho_local}/erros")
        self.saida = Pasta(f"{caminho_local}/saida")

    def __iter__(self):
        return iter([self.entrada, self.erros, self.saida])


class Pasta:
    def __init__(self, caminho: str) -> None:
        self.caminho = caminho

    def conteudo(self) -> list[str]:
        return [f"{self.caminho}/{caminho}" for caminho in os.listdir(self.caminho)]

    def procurar(self, extensao: str):
        if "." not in extensao:
            extensao = f".{extensao}"

        return [item for item in self.conteudo() if item.endswith(extensao)]
