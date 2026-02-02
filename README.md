# Teste Técnico - Coleta, Transformação e Análise de Dados ANS

Este repositório contém a resolução completa dos quatro desafios técnicos propostos, focados no ecossistema de dados da ANS (Agência Nacional de Saúde Suplementar). O projeto abrange desde a extração de dados brutos até a disponibilização de uma interface analítica moderna.

---

## 🚀 Visão Geral do Projeto

O objetivo principal é processar as demonstrações contábeis das operadoras de saúde brasileiras, realizando validações rigorosas, cruzamento de dados cadastrais e disponibilização de insights através de SQL e uma aplicação Web Full-Stack.

### 📁 Estrutura do Repositório

- **[desafio_01_api_ans](./desafio_01_api_ans)**: Integração com API pública, download e consolidação dos últimos 3 trimestres de despesas.
- **[desafio_02_transformacao_validacao](./desafio_02_transformacao_validacao)**: Limpeza de dados, validação de CNPJ e enriquecimento com dados cadastrais.
- **[desafio_03_banco_dados](./desafio_03_banco_dados)**: Modelagem SQL (DDL), scripts de importação e queries analíticas de negócio.
- **[desafio_04_api_interface](./desafio_04_api_interface)**: API RESTful (FastAPI) e Dashboard Web (Vue.js 3) para visualização dos dados.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.13
- **Processamento de Dados**: Pandas, Requests, BeautifulSoup4.
- **Banco de Dados**: SQLite (para simulação e API).
- **Backend API**: FastAPI, Uvicorn, Pydantic.
- **Frontend**: Vue.js 3 (Vite), Pinia, Chart.js, Lucide Icons.
- **Padronização**: UTF-8-SIG (Garantia de acentuação brasileira em todos os arquivos).

---

## 🚥 Como Executar os Desafios

### Pré-requisitos
- Python 3.x instalado.
- Node.js e NPM (para o Desafio 4).

### Passo 1: Consolidação (Desafio 1)
Prepara a base bruta de despesas dos últimos 3 trimestres.
```bash
python desafio_01_api_ans/src/main.py
```

### Passo 2: Transformação (Desafio 2)
Valida e enriquece os dados, gerando o arquivo pronto para análise.
```bash
python desafio_02_transformacao_validacao/src/main.py
```

### Passo 3: Banco de Dados (Desafio 3)
Executa a validação das regras de negócio via SQL.
```bash
cd desafio_03_banco_dados
python src/sqlite_test.py
```

### Passo 4: Interface Web (Desafio 4)
Inicia o ecossistema completo (API + Dashboard).

**Terminal 1 (Backend):**
```bash
cd desafio_04_api_interface/backend
pip install -r requirements.txt
python main.py
```

**Terminal 2 (Frontend):**
```bash
cd desafio_04_api_interface/frontend
npm install
npm run dev
```

---

## 🛡️ Decisões Técnicas de Destaque

1.  **Resolução de Acentuação**: Implementada a padronização global com `utf-8-sig` e camadas de limpeza de string para eliminar bugs de caracteres especiais em nomes de operadoras e modalidades.
2.  **Performance de Dados**: Processamento incremental de arquivos CSV massivos (mais de 2 milhões de linhas) para garantir estabilidade em qualquer máquina.
3.  **Modernidade Web**: Utilização de Vue 3 com Composition API e Pinia para um gerenciamento de estado escalável e reativo.
4.  **Integridade**: Validação algorítmica de CNPJ e tratamento de operadoras sem dados no período histórico.

---

**Autor**: Thiago Rodrigues
**Repositório**: [GitHub - Teste-WebScraping-py](https://github.com/ThiagoRodrigues11/Teste-WebScraping-py)
