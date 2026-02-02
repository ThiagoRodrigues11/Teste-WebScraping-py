-- 3.2. Queries DDL para estruturar as tabelas

-- Tabela para dados cadastrais das operadoras
-- Chave primária no CNPJ para integridade e busca rápida.
CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(20),
    cnpj VARCHAR(14) PRIMARY KEY,
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    uf CHAR(2),
    INDEX idx_modalidade (modalidade),
    INDEX idx_uf (uf)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela para dados consolidados de despesas
-- Uso de DECIMAL(18,2) para precisão financeira absoluta.
-- Data como DATE para permitir filtros temporais e ordenação eficiente.
CREATE TABLE IF NOT EXISTS despesas_consolidadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cnpj VARCHAR(14),
    data_referencia DATE, -- Representa o início do trimestre
    ano INT,
    trimestre INT,
    valor_despesa DECIMAL(18,2),
    FOREIGN KEY (cnpj) REFERENCES operadoras(cnpj),
    INDEX idx_data (data_referencia),
    INDEX idx_cnpj_data (cnpj, data_referencia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela para dados agregados
-- Armazena o resultado processado para consultas rápidas em dashboards.
CREATE TABLE IF NOT EXISTS despesas_agregadas (
    cnpj VARCHAR(14) PRIMARY KEY,
    razao_social VARCHAR(255),
    uf CHAR(2),
    total_despesas DECIMAL(18,2),
    media_trimestral DECIMAL(18,2),
    desvio_padrao DECIMAL(18,2),
    FOREIGN KEY (cnpj) REFERENCES operadoras(cnpj)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
