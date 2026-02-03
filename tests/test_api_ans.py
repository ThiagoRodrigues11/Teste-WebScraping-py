import pytest
from fastapi.testclient import TestClient
import sys
import os

# Adiciona a raiz do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from desafio_04_api_interface.backend.main import app

client = TestClient(app)

def test_status_api():
    """Testa se a API está online"""
    response = client.get("/api/estatisticas")
    assert response.status_code == 200

def test_pagination_structure():
    """Testa se a paginação retorna a estrutura de metadados correta"""
    response = client.get("/api/operadoras?page=1&limit=5")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert "total" in json_data
    assert len(json_data["data"]) <= 5

def test_operadora_nao_encontrada():
    """Testa o tratamento de erro para CNPJ inexistente"""
    response = client.get("/api/operadoras/00000000000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Operadora não encontrada"
