# Desafio 2 - Transformação e Validação de Dados

Este projeto realiza a validação, enriquecimento e agregação dos dados financeiros de operadoras de saúde consolidado no Desafio 1, cruzando-os com dados cadastrais oficiais da ANS.

## 2.1. Validação de Dados
Foram implementadas as seguintes validações:
- **Razão Social**: Verificação de campos não nulos e não vazios.
- **Valores Numéricos**: Garantia de que as despesas são valores positivos (>= 0).
- **CNPJ**: Validação rigorosa utilizando Regex para formato e o algoritmo de Dígitos Verificadores (cálculo matemático oficial).

### Trade-off Técnico: CNPJs Inválidos
- **Abordagem Escolhida**: Filtragem e remoção (Drop).
- **Prós**: Garante a integridade absoluta do relatório final. Como o objetivo é agrupar por UF e Modalidade, registros com CNPJ inválido não teriam correspondência confiável no cadastro, gerando dados "órfãos" ou classificados erroneamente.
- **Contras**: Redução do volume total processado (perda de registros que poderiam ter valores financeiros reais, mas com erro de digitação no identificador).
- **Justificativa**: Em conformidade com as boas práticas de Engenharia de Dados, a "fonte da verdade" para identificação é o CNPJ. Dados inconsistentes nesta chave primária inviabilizam análises geográficas/cadastrais precisas.

## 2.2. Enriquecimento de Dados
O script realiza o download automático do arquivo `Relatorio_cadop.csv` do portal de Dados Abertos da ANS e realiza o enriquecimento (Join) para adicionar as colunas: `RegistroANS`, `Modalidade` e `UF`.

### Análise Crítica e Tratamento de Falhas
- **Registros sem match no cadastro**: Foi utilizado um **Left Join**. Registros financeiros sem correspondência no cadastro ativo são mantidos para preservar o valor total, mas identificados com "N/A" nas colunas cadastrais.
- **CNPJs Duplicados no Cadastro**: Aplicada a estratégia de de-duplicação no arquivo cadastral (`drop_duplicates`) mantendo o primeiro registro. Isso evita a explosão da base de dados financeira.
- **Trade-off de Processamento (Join)**:
    - **Estratégia**: Processamento em memória utilizando a biblioteca Pandas.
    - **Justificativa**: Com um volume de aproximadamente 2,1 milhões de linhas (~175MB), o processamento em memória é extremamente eficiente em termos de tempo e complexidade de código. Estratégias incrementais ou armazenamento em banco de dados seriam desnecessariamente complexas para este volume de dados, que consome menos de 1GB de RAM durante a execução.

## 2.3. Agregação com Múltiplas Estratégias
Os dados foram agrupados por `RazaoSocial`, `UF`, `CNPJ`, `RegistroANS` e `Modalidade`.

### Métricas Calculadas:
- **Total de Despesas**: Soma acumulada de todos os registros do período.
- **Média de despesas por trimestre**: Calculada em duas etapas para maior precisão (soma dos valores por trimestre e posterior média dessas somas por operadora).
- **Desvio Padrão**: Calculado para identificar a volatilidade das despesas de cada operadora.

### Trade-off de Ordenação:
- **Estratégia**: Ordenação via Pandas `sort_values` (QuickSort interno).
- **Justificativa**: O resultado final agregado possui cerca de 800-1000 linhas (número total de operadoras ativas). A ordenação em memória é virtualmente instantânea e permite priorizar a visualização das operadoras com maior impacto financeiro no setor.

---

## Entrega Final
- **Arquivo de Saída**: `output/despesas_agregadas.csv`
- **Ordenação**: Ordenado por valor total (maior para menor).
- **Compactação**: Arquivo de saída compactado em `Teste_Thiago_Rodrigues.zip` localizado na raiz do projeto.

## Como Executar
1. Certifique-se de que o arquivo `desafio_01_api_ans/output/consolidado_despesas.csv` existe.
2. Navegue até a pasta: `cd desafio_02_transformacao_validacao`
3. Execute: `python src/main.py`
