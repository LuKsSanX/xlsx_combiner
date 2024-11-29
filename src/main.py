import shutil
import os
import logging

import pandas as pd

from .pastas import Pastas
from .setup import setup


def main() -> None:
    logging.getLogger().setLevel(logging.DEBUG)

    caminho_local = os.path.abspath(os.path.dirname(__file__))
    logging.debug(f"caminho_local: {caminho_local}")

    pastas = Pastas(caminho_local)
    logging.debug(pastas)

    setup()

    logging.info(pastas.entrada.conteudo())
    arquivos = pastas.entrada.procurar("xlsx")

    arquivos = [ArquivoExcel(arquivo) for arquivo in arquivos]
    arquivo_colunas = procurar_arquivo_colunas(arquivos)

    if not arquivo_colunas:
        logging.error("arquivo de colunas nao definido")
        return

    colunas = list(arquivo_colunas.dataframe.columns.values)
    colunas = [str(coluna) for coluna in colunas]

    dataframes = [
        arquivo.dataframe
        for arquivo in arquivos
        if filtro_verificacao_colunas(colunas, arquivo, pastas.erros.caminho)
    ]

    saida = pd.concat(dataframes, ignore_index=True)
    saida.to_excel(pastas.saida.caminho + "/arquivo.xlsx", index=False)


class ArquivoExcel:
    def __init__(self, caminho: str) -> None:
        self.caminho = caminho
        self.dataframe = pd.read_excel(caminho)


def procurar_arquivo_colunas(arquivos: list[ArquivoExcel]) -> ArquivoExcel | None:
    if len(arquivos) < 1:
        return

    arquivo = arquivos.pop(0)

    if not arquivo.caminho.endswith("colunas.xlsx"):
        return procurar_arquivo_colunas(arquivos)

    return arquivo


def filtro_verificacao_colunas(
    colunas: list[str], arquivo: ArquivoExcel, caminho_erros: str
) -> bool:
    colunas_validas = verificar_colunas(colunas, arquivo.dataframe)

    if not colunas_validas:
        shutil.move(arquivo.caminho, caminho_erros)

    return colunas_validas


def verificar_colunas(colunas: list[str], dataframe: pd.DataFrame) -> bool:
    return all(coluna in dataframe.columns.values for coluna in colunas)


if __name__ == "__main__":
    main()
