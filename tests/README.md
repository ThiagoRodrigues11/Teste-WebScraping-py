# Suíte de Testes Automatizados

Este diretório contém os testes automatizados para garantir a integridade dos dados e o funcionamento correto da API do projeto.

## Objetivo
Os testes servem para validar:
1. **Lógica de Negócio**: Garantir que funções críticas (como a validação de CNPJ) funcionam conforme o esperado.
2. **Estabilidade da API**: Verificar se as rotas do backend estão respondendo corretamente e entregando o formato de dados esperado pelo frontend.
3. **Resiliência**: Testar o comportamento do sistema diante de erros (ex: busca por dados inexistentes).

## Ferramentas Utilizadas
- **Pytest**: Framework principal de testes.
- **FastAPI TestClient**: Para simular requisições à API sem precisar subir o servidor manualmente.
- **HTTPX**: Dependência necessária para o TestClient realizar chamadas assíncronas.

## Como Executar

### 1. Requisitos
Certifique-se de ter as dependências de teste instaladas:
```bash
pip install pytest httpx
```

### 2. Rodando os Testes
Para executar todos os testes, basta rodar o comando abaixo na raiz do projeto:
```bash
pytest
```

## Estrutura de Testes

### test_validation.py (Testes Unitários)
Foca na validação individual de funções do Desafio 2.
- Verifica se CNPJs válidos (formatados ou não) são aceitos.
- Garante que CNPJs inválidos (tamanho errado, sequências repetidas) são bloqueados.

### test_api_ans.py (Testes de Integração)
Valida as rotas do Backend (Desafio 4).
- Verifica se o servidor está online e retornando status 200.
- Valida se a estrutura de paginação (data + total) está correta para o Frontend.
- Testa se o sistema retorna erro 404 de forma amigável para registros não encontrados.

## Boas Práticas
- Os testes utilizam **Mocks** ou dados sintéticos (como CNPJs matematicamente válidos mas fictícios) para evitar o uso de dados sensíveis ou reais no código de teste.
