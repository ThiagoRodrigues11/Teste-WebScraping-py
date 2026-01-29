# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"
DEMONSTRACOES_URL = BASE_URL + "demonstracoes_contabeis/"


def get_soup(url: str) -> BeautifulSoup:
    """Faz requisição HTTP e retorna o BeautifulSoup da página."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def listar_anos_disponiveis():
    """
    Lista os anos disponíveis dentro de demonstracoes_contabeis/.
    """
    soup = get_soup(DEMONSTRACOES_URL)

    anos = []

    for link in soup.find_all("a"):
        href = link.get("href", "").strip("/")

        if href.isdigit() and len(href) == 4:
            anos.append(href)

    return sorted(anos)


def main():
    print("Buscando anos disponíveis em demonstracoes_contabeis...\n")

    anos = listar_anos_disponiveis()

    if not anos:
        print("Nenhum ano encontrado. Verifique a estrutura da ANS.")
        return

    print(f"Anos encontrados: {anos}")


if __name__ == "__main__":
    main()
