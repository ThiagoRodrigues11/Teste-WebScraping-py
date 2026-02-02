-- 3.4. Queries Analíticas (VERSÃO FINAL CORRIGIDA)

-- QUERY 1: Top 5 operadoras com maior crescimento percentual entre o primeiro e o último trimestre
WITH primeiro_trimestre AS (
    SELECT cnpj, SUM(valor_despesa) as valor_inicial
    FROM despesas_consolidadas
    WHERE data_referencia = (SELECT MIN(data_referencia) FROM despesas_consolidadas)
    GROUP BY cnpj
),
ultimo_trimestre AS (
    SELECT cnpj, SUM(valor_despesa) as valor_final
    FROM despesas_consolidadas
    WHERE data_referencia = (SELECT MAX(data_referencia) FROM despesas_consolidadas)
    GROUP BY cnpj
)
SELECT 
    o.razao_social,
    p.valor_inicial,
    u.valor_final,
    ((u.valor_final - p.valor_inicial) / NULLIF(p.valor_inicial, 0)) * 100 AS crescimento_percentual
FROM primeiro_trimestre p
JOIN ultimo_trimestre u ON p.cnpj = u.cnpj
JOIN operadoras o ON p.cnpj = o.cnpj
WHERE p.valor_inicial > 0
ORDER BY crescimento_percentual DESC
LIMIT 5;


-- QUERY 2: Distribuição de despesas por UF e média REAL por operadora
-- Agrupa por estado e divide a soma total pela quantidade de CNPJs únicos naquele estado.
SELECT 
    o.uf,
    SUM(d.valor_despesa) AS total_despesas_uf,
    SUM(d.valor_despesa) / COUNT(DISTINCT o.cnpj) AS media_por_operadora_uf,
    COUNT(DISTINCT o.cnpj) AS qtd_operadoras
FROM despesas_consolidadas d
JOIN operadoras o ON d.cnpj = o.cnpj
GROUP BY o.uf
ORDER BY total_despesas_uf DESC
LIMIT 5;


-- QUERY 3: Operadoras com despesas acima da média geral em pelo menos 2 dos 3 trimestres
-- Lógica:
-- 1. Soma total por operadora/trimestre
-- 2. Média global dos totais trimestrais
-- 3. Compara operadora vs média global e conta trimestres (máx 3)
WITH total_operadora_trimestre AS (
    SELECT cnpj, data_referencia, SUM(valor_despesa) as total_op
    FROM despesas_consolidadas
    GROUP BY cnpj, data_referencia
),
media_global_trimestral AS (
    SELECT data_referencia, AVG(total_op) as media_global
    FROM total_operadora_trimestre
    GROUP BY data_referencia
)
SELECT 
    o.razao_social,
    COUNT(*) as trimestres_acima_da_media
FROM total_operadora_trimestre t
JOIN media_global_trimestral m ON t.data_referencia = m.data_referencia
JOIN operadoras o ON t.cnpj = o.cnpj
WHERE t.total_op > m.media_global
GROUP BY t.cnpj, o.razao_social
HAVING count(*) >= 2;
