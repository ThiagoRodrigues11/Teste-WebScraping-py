import sqlite3
import pandas as pd
import os

def run_test():
    # Caminhos
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    despesas_path = os.path.join(base_dir, "desafio_01_api_ans", "output", "consolidado_despesas.csv")
    cadop_path = os.path.join(base_dir, "desafio_02_transformacao_validacao", "data", "Relatorio_cadop.csv")
    
    # Criar Banco em memória
    conn = sqlite3.connect(':memory:')
    
    print("--- Simulação de Banco de Dados (SQLite) ---")
    
    # Função para limpar textos de acentuação zoada
    def clean_text(df, column):
        if column in df.columns:
            # Tenta corrigir o erro clássico de ler UTF-8 como Latin-1
            def fix(text):
                if not isinstance(text, str): return text
                try:
                    return text.encode('latin-1').decode('utf-8')
                except:
                    return text
            df[column] = df[column].apply(fix)
        return df

    # 1. Carregar Operadoras
    print("Carregando dados cadastrais...")
    try:
        # Relatorio_cadop agora é processado como utf-8-sig
        df_cadop = pd.read_csv(cadop_path, sep=';', encoding='utf-8-sig')
        df_cadop = df_cadop[['CNPJ', 'REGISTRO_OPERADORA', 'Modalidade', 'UF', 'Razao_Social']].drop_duplicates(subset=['CNPJ'])
        df_cadop.to_sql('operadoras', conn, index=False)
    except Exception as e:
        # Fallback para latin-1 caso o download original ainda esteja lá
        df_cadop = pd.read_csv(cadop_path, sep=';', encoding='latin-1')
        df_cadop = df_cadop[['CNPJ', 'REGISTRO_OPERADORA', 'Modalidade', 'UF', 'Razao_Social']].drop_duplicates(subset=['CNPJ'])
        df_cadop.to_sql('operadoras', conn, index=False)

    # 2. Carregar Despesas
    print("Carregando despesas (Base completa)...")
    try:
        # Nosso consolidado agora é salvo em utf-8-sig
        df_despesas = pd.read_csv(despesas_path, low_memory=False, encoding='utf-8-sig')
        
        df_despesas['data_referencia'] = df_despesas['Ano'].astype(str) + "-" + \
                                       df_despesas['Trimestre'].apply(lambda x: '01' if '1' in str(x) else ('04' if '2' in str(x) else '07' if '3' in str(x) else '10')) + "-01"
        df_despesas.to_sql('despesas_consolidadas', conn, index=False)
    except Exception as e:
        print(f"Erro ao carregar despesas: {e}")
        return

    # Execução das Queries
    print("\n" + "="*50)
    print("QUERY 1: TOP 5 CRESCIMENTO PERCENTUAL")
    query1 = """
    WITH primeiro_ponto AS (
        SELECT CNPJ, RazaoSocial, SUM(ValorDespesas) as inicial
        FROM despesas_consolidadas
        WHERE data_referencia = (SELECT MIN(data_referencia) FROM despesas_consolidadas)
        GROUP BY CNPJ
    ),
    ultimo_ponto AS (
        SELECT CNPJ, SUM(ValorDespesas) as final
        FROM despesas_consolidadas
        WHERE data_referencia = (SELECT MAX(data_referencia) FROM despesas_consolidadas)
        GROUP BY CNPJ
    )
    SELECT 
        p.RazaoSocial,
        ROUND(p.inicial, 2) as Gasto_Inicial,
        ROUND(u.final, 2) as Gasto_Final,
        ROUND(((u.final - p.inicial) / NULLIF(p.inicial, 0)) * 100, 2) as Crescimento_Perc
    FROM primeiro_ponto p
    JOIN ultimo_ponto u ON p.CNPJ = u.CNPJ
    WHERE p.inicial > 0
    ORDER BY Crescimento_Perc DESC
    LIMIT 5
    """
    print(pd.read_sql(query1, conn).to_string(index=False))

    print("\n" + "="*50)
    print("QUERY 2: DISTRIBUIÇÃO POR UF (ORDEM DE GASTO)")
    query2 = """
    SELECT 
        o.UF,
        ROUND(SUM(d.ValorDespesas), 2) as Total_UF,
        ROUND(SUM(d.ValorDespesas) / COUNT(DISTINCT o.CNPJ), 2) as Media_Por_Operadora
    FROM despesas_consolidadas d
    JOIN operadoras o ON d.CNPJ = o.CNPJ
    GROUP BY o.UF
    ORDER BY Total_UF DESC
    LIMIT 5
    """
    print(pd.read_sql(query2, conn).to_string(index=False))

    print("\n" + "="*50)
    print("QUERY 3: ACIMA DA MÉDIA EM 2+ TRIMESTRES")
    query3 = """
    WITH total_operadora_trimestre AS (
        SELECT CNPJ, RazaoSocial, data_referencia, SUM(ValorDespesas) as total_op
        FROM despesas_consolidadas
        GROUP BY CNPJ, data_referencia
    ),
    media_global_trimestre AS (
        SELECT data_referencia, AVG(total_op) as media_global
        FROM total_operadora_trimestre
        GROUP BY data_referencia
    )
    SELECT 
        t.RazaoSocial,
        COUNT(*) as Trimestres_Acima_Media
    FROM total_operadora_trimestre t
    JOIN media_global_trimestre m ON t.data_referencia = m.data_referencia
    WHERE t.total_op > m.media_global
    GROUP BY t.CNPJ
    HAVING Trimestres_Acima_Media >= 2
    LIMIT 5
    """
    print(pd.read_sql(query3, conn).to_string(index=False))
    
    # Salvar resultados em um log para conferência
    with open("test_results.txt", "w", encoding="utf-8") as f:
        f.write("--- RESULTADOS DO TESTE ---\n\n")
        
        f.write("QUERY 1:\n")
        f.write(pd.read_sql(query1, conn).to_string(index=False))
        f.write("\n\nQUERY 2:\n")
        f.write(pd.read_sql(query2, conn).to_string(index=False))
        f.write("\n\nQUERY 3:\n")
        f.write(pd.read_sql(query3, conn).to_string(index=False))

    print("\n" + "="*50)
    print("Teste concluído com sucesso! Verifique 'test_results.txt' para os dados limpos.")

if __name__ == "__main__":
    run_test()
