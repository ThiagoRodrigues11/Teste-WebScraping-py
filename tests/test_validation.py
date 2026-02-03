import pytest
import sys
import os

# Adiciona a raiz do projeto ao path para conseguir importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from desafio_02_transformacao_validacao.src.main import validate_cnpj

def test_cnpj_valido_com_formatacao():
    # Usando um CNPJ que segue o algoritmo mas é voltado para testes/exemplos
    assert validate_cnpj("12.345.678/0001-95") == True

def test_cnpj_valido_apenas_numeros():
    assert validate_cnpj("12345678000195") == True

def test_cnpj_invalido_tamanho_errado():
    assert validate_cnpj("123456") == False

def test_cnpj_invalido_sequencia_igual():
    assert validate_cnpj("11111111111111") == False

def test_cnpj_vazio():
    assert validate_cnpj("") == False
