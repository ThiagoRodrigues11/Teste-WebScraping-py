# Desafio 1 - Integração com API Pública (ANS)

Este projeto realiza a extração, processamento e consolidação de dados de Demonstrações Contábeis das operadoras de planos de saúde, utilizando os Dados Abertos da ANS.

## 1.1. Acesso à API de Dados Abertos
O script acessa o repositório oficial da ANS e identifica automaticamente os últimos 3 trimestres disponíveis para download.
- **Resiliência**: O código foi desenvolvido para ser resiliente a variações de estrutura de diretórios e nomes de arquivos, navegando recursivamente quando necessário para encontrar os arquivos de demonstrações contábeis.

## 1.2. Processamento de Arquivos
O processamento envolve a extração de arquivos ZIP e a filtragem específica de "Despesas com Eventos/Sinistros".

### Identificação Automática de Estrutura
- O script identifica automaticamente se os arquivos estão em formato CSV, TXT ou XLSX, normalizando os nomes das colunas e os delimitadores para garantir que os dados sejam consolidados de forma uniforme, independente da variação técnica do arquivo original.

### Trade-off Técnico: Processamento em Memória vs Incremental
- **Escolha**: Processamento Incremental (Arquivo por Arquivo).
- **Justificativa**: Cada arquivo trimestral da ANS pode conter centenas de milhares de linhas. Processar todos de uma vez em memória poderia exceder o limite de RAM em máquinas com recursos limitados. A abordagem incremental processa um arquivo por vez, filtra os dados necessários e os anexa ao consolidado, garantindo baixo consumo de memória e estabilidade.

## 1.3. Consolidação e Análise de Inconsistências
Os dados dos 3 trimestres são unificados em um único CSV com as colunas: `CNPJ`, `RazaoSocial`, `Trimestre`, `Ano` e `ValorDespesas`.

### Tratamento de Inconsistências:
- **CNPJs duplicados com razões sociais diferentes**:
    - **Abordagem**: Foi priorizada a Razão Social mais recente identificada no cadastro oficial da ANS.
    - **Justificativa**: Operadoras podem mudar de nome ou passar por fusões. O cadastro oficial é a âncora de confiança.
- **Valores zerados ou negativos**:
    - **Abordagem**: Mantidos no arquivo final.
    - **Justificativa**: Na contabilidade regulatória, valores negativos podem representar estornos ou ajustes de provisões técnicos. Removê-los distorceria o balanço final da operadora.
- **Formatos de data inconsistentes**:
    - **Abordagem**: Padronização sistemática para o formato `YYYY/QQ`.
    - **Justificativa**: Garante a integridade temporal nas análises comparativas.

## ⚙️ Padronização de Encoding (Resolução de Acentos)
Os arquivos originais da ANS frequentemente utilizam codificações legadas (como Latin-1). Para garantir que nomes de operadoras com acentos (ex: "SAÚDE", "CONCEIÇÃO") sejam preservados corretamente em todos os sistemas (Windows, Linux, Bancos de Dados):
- **Solução**: Todos os arquivos de saída agora são salvos utilizando o encoding `utf-8-sig`.
- **Por que `utf-8-sig`?**: Esta variante adiciona um "Byte Order Mark" (BOM) que força aplicativos como Excel e editores de texto no Windows a reconhecerem imediatamente o arquivo como UTF-8, evitando caracteres corrompidos (`mojibake`).

---

## Entrega Final
- **Arquivo**: `output/consolidado_despesas.zip`
- **Conteúdo**: CSV consolidado dos últimos 3 trimestres.

## Como Executar
1. Instale as dependências: `pip install pandas requests beautifulsoup4`
2. Navegue até a pasta: `cd desafio_01_api_ans`
3. Execute: `python src/main.py`