-- 3.3. Queries de Importação e Tratamento de Dados

-- Nota: Os caminhos dos arquivos devem ser ajustados para o ambiente real.
-- É assumido o uso de MySQL 8.0.

-- 1. Importação dos Dados Cadastrais (Operadoras)
-- Estratégia: Carregar em tabela temporária para limpeza antes de inserir na oficial.
CREATE TEMPORARY TABLE temp_operadoras (
    reg_ans VARCHAR(50),
    cnpj VARCHAR(50),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(255),
    logradouro VARCHAR(255),
    numero VARCHAR(50),
    complemento VARCHAR(255),
    bairro VARCHAR(255),
    cidade VARCHAR(255),
    uf CHAR(2),
    cep VARCHAR(20),
    ddd VARCHAR(10),
    telefone VARCHAR(50),
    fax VARCHAR(50),
    email VARCHAR(255),
    representante VARCHAR(255),
    cargo VARCHAR(255),
    regiao VARCHAR(100),
    data_registro VARCHAR(50)
);

LOAD DATA INFILE '/caminho/para/Relatorio_cadop.csv' 
INTO TABLE temp_operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- Limpeza e Inserção:
-- Tratamento: Remover caracteres não numéricos do CNPJ e garantir 14 dígitos.
-- Caso o CNPJ seja nulo ou inválido, o registro é ignorado (chave primária obrigatória).
INSERT INTO operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, uf)
SELECT 
    reg_ans,
    LPAD(REGEXP_REPLACE(cnpj, '[^0-9]', ''), 14, '0'),
    COALESCE(razao_social, 'NAO IDENTIFICADO'),
    nome_fantasia,
    modalidade,
    uf
FROM temp_operadoras
WHERE cnpj IS NOT NULL
ON DUPLICATE KEY UPDATE razao_social = VALUES(razao_social);

-- 2. Importação das Despesas Consolidadas
CREATE TEMPORARY TABLE temp_despesas (
    cnpj VARCHAR(255),
    razao_social VARCHAR(255),
    trimestre VARCHAR(10),
    ano VARCHAR(10),
    valor VARCHAR(255)
);

LOAD DATA INFILE '/caminho/para/consolidado_despesas.csv' 
INTO TABLE temp_despesas
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- Limpeza e Inserção:
-- Tratamento: Converter "1T" para o mês inicial do trimestre para o tipo DATE.
-- Tratamento: Substituir strings ou campos vazios no valor por 0.00.
INSERT INTO despesas_consolidadas (cnpj, data_referencia, ano, trimestre, valor_despesa)
SELECT 
    LPAD(REGEXP_REPLACE(cnpj, '[^0-9]', ''), 14, '0'),
    STR_TO_DATE(CONCAT(ano, '-', 
        CASE 
            WHEN trimestre LIKE '%1%' THEN '01'
            WHEN trimestre LIKE '%2%' THEN '04'
            WHEN trimestre LIKE '%3%' THEN '07'
            WHEN trimestre LIKE '%4%' THEN '10'
            ELSE '01'
        END, '-01'), '%Y-%m-%d'),
    CAST(ano AS UNSIGNED),
    CAST(REGEXP_REPLACE(trimestre, '[^0-9]', '') AS UNSIGNED),
    CAST(REPLACE(COALESCE(NULLIF(valor, ''), '0'), ',', '.') AS DECIMAL(18,2))
FROM temp_despesas;
