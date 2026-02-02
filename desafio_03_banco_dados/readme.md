# Desafio 3 - Banco de Dados e Análise

Este diretório contém a solução completa para o Desafio 3, focando na estruturação, importação e análise de dados de operadoras de saúde e suas despesas assistenciais.

## Estrutura do Projeto
- `sql/schema.sql`: Definições DDL (Criação de tabelas, chaves e índices).
- `sql/import.sql`: Scripts para importação e tratamento de dados dos CSVs.
- `sql/analise.sql`: Queries analíticas para responder às perguntas de negócio.
- `src/sqlite_test.py`: Script de validação que simula o banco de dados e executa as queries sobre os dados reais.

---

## 3.2. Estrutura e Trade-offs Técnicos

### Normalização: Opção B (Tabelas Normalizadas)
**Escolha**: Tabelas separadas para cadastro (`operadoras`), fatos de despesas (`despesas_consolidadas`) e resumo (`despesas_agregadas`).
- **Volume de Dados**: Com mais de 2 milhões de registros, a desnormalização causaria redundância massiva de strings (Razão Social, UF, Modalidade), ocupando gigabytes extras.
- **Frequência de Atualização**: Operadoras podem mudar de nome ou UF. Em uma estrutura normalizada, atualizamos apenas uma linha na tabela de cadastro.
- **Complexidade**: Embora exija `JOINs`, o uso de Chaves Primárias (`CNPJ`) indexadas torna as consultas extremamente performáticas.

### Tipos de Dados
- **Valores Monetários (`DECIMAL(18,2)`)**: Essencial para precisão financeira. Tipos como `FLOAT` ou `DOUBLE` possuem imprecisões de ponto flutuante que acumulariam erros em somas de milhões de linhas.
- **Datas (`DATE`)**: Armazenamos o início do trimestre como uma data real (AAAA-MM-DD). Isso permite o uso de funções temporais nativas do SQL, ordenação cronológica e ocupa menos espaço que strings.

---

## 3.3. Importação e Trata-fomento de Inconsistências

Durante a carga dos dados, implementamos as seguintes lógicas de resiliência:
- **Encoding (Resolução Definitiva)**: Para solucionar o bug de caracteres "zoados" (ex: `SAÃšDE` em vez de `SAÚDE`), todos os scripts de leitura e escrita foram padronizados para o encoding `utf-8-sig`. No script de teste (`sqlite_test.py`), implementamos uma camada de limpeza adicional que garante que os relatórios analíticos sejam 100% legíveis no Windows.
- **Valores NULL/Vazios**: Campos de valor obrigatório são tratados com `COALESCE` e convertidos para `0.00` para não quebrar cálculos estatísticos.
- **Strings em Campos Numéricos**: Limpeza via Regex para garantir que CNPJs contenham apenas números e que símbolos monetários/milhares sejam removidos antes do cast numérico.
- **Formatos de Data**: Conversão do formato "AAAA-QT" (ex: 2024-1T) para o primeiro dia do respectivo trimestre para padronização.

---

## 3.4. Queries Analíticas e Desafios

### Query 1: Maior Crescimento Percentual
- **Desafio**: Operadoras que não possuem dados em todos os períodos.
- **Solução**: Utilizamos `INNER JOIN` entre o primeiro e o último trimestre disponível. Operadoras sem dados em ambas as pontas são excluídas do ranking de crescimento para garantir um cálculo estatisticamente válido.

### Query 2: Distribuição por UF
- **Destaque**: Além do total por estado, calculamos a **Média Real por Operadora**. No estado do Ceará, por exemplo, observamos que apenas 5 operadoras concentram a maior parte do gasto, gerando uma média por empresa muito superior a estados como Minas Gerais, que possui um mercado mais pulverizado.

### Query 3: Operadoras Acima da Média
- **Trade-off Técnico**: Escolhemos a abordagem de **CTEs (Common Table Expressions)**.
- **Justificativa**: Esta abordagem torna o código modular (passo-a-passo) e altamente legível. Primeiro calculamos os totais por empresa/trimestre, depois a média global e, por fim, filtramos. É muito mais fácil de manter do que subqueries aninhadas.

---

## Como Executar o Teste de Validação

Para validar as queries e os dados sem precisar configurar um servidor SQL completo, utilize o simulador SQLite incluído:

1. **Requisitos**: Python 3.x e biblioteca `pandas` instalada.
2. **Execução**:
   ```bash
   cd desafio_03_banco_dados
   python src/sqlite_test.py
   ```
3. **Verificação**: O script exibirá os resultados com acentuação corrigida no terminal e gerará um arquivo `test_results.txt` com o log completo.
