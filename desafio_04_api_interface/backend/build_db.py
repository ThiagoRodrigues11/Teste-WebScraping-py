import sqlite3
import pandas as pd
import os
import re

def build_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "backend", "ans.db")
    despesas_csv = os.path.join(base_dir, "..", "desafio_01_api_ans", "output", "consolidado_despesas.csv")
    cadop_csv = os.path.join(base_dir, "..", "desafio_02_transformacao_validacao", "data", "Relatorio_cadop.csv")
    
    conn = sqlite3.connect(db_path)
    
    # 1. Operadoras
    print("Populado tabela de operadoras...")
    df_cadop = pd.read_csv(cadop_csv, sep=';', encoding='latin-1')
    df_cadop = df_cadop.rename(columns={
        'REGISTRO_OPERADORA': 'registro_ans',
        'CNPJ': 'cnpj',
        'Razao_Social': 'razao_social',
        'Modalidade': 'modalidade',
        'UF': 'uf'
    })
    
    def fix_encoding(text):
        if not isinstance(text, str): return text
        try: return text.encode('latin-1').decode('utf-8')
        except: return text

    # Aplicar correção de acentos em todas as colunas de texto
    text_cols = ['razao_social', 'modalidade', 'uf']
    for col in text_cols:
        df_cadop[col] = df_cadop[col].apply(fix_encoding)

    df_cadop['cnpj'] = df_cadop['cnpj'].astype(str).str.replace(r'\D', '', regex=True).str.zfill(14)
    df_cadop = df_cadop[['registro_ans', 'cnpj', 'razao_social', 'modalidade', 'uf']].drop_duplicates(subset=['cnpj'])
    df_cadop.to_sql('operadoras', conn, if_exists='replace', index=False)
    
    # 2. Despesas
    print("Populado tabela de despesas (isso pode demorar um pouco)...")
    df_despesas = pd.read_csv(despesas_csv, encoding='utf-8-sig')
    df_despesas['cnpj'] = df_despesas['CNPJ'].astype(str).str.replace(r'\D', '', regex=True).str.zfill(14)
    
    # Padronizar data para facilitar queries
    df_despesas['data_referencia'] = df_despesas['Ano'].astype(str) + "-" + \
                                   df_despesas['Trimestre'].apply(lambda x: '01' if '1' in str(x) else ('04' if '2' in str(x) else '07' if '3' in str(x) else '10')) + "-01"
    
    df_despesas_clean = df_despesas[['cnpj', 'data_referencia', 'Ano', 'Trimestre', 'ValorDespesas']]
    df_despesas_clean.to_sql('despesas', conn, if_exists='replace', index=False)
    
    # Criar índices
    conn.execute("CREATE INDEX idx_cnpj ON despesas(cnpj)")
    conn.execute("CREATE INDEX idx_cnpj_cad ON operadoras(cnpj)")
    
    print(f"Banco de dados criado em: {db_path}")
    conn.close()

if __name__ == "__main__":
    build_db()
