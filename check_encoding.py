import pandas as pd
import os

files = [
    r'desafio_01_api_ans/output/consolidado_despesas.csv',
    r'desafio_02_transformacao_validacao/output/despesas_agregadas.csv'
]

with open('encoding_check.txt', 'w', encoding='utf-8') as f:
    for file in files:
        f.write(f"--- Checking {file} ---\n")
        try:
            df = pd.read_csv(file, encoding='utf-8-sig', nrows=20)
            f.write(df['RazaoSocial'].to_string())
            f.write("\n\n")
        except Exception as e:
            f.write(f"Error reading {file}: {e}\n\n")

print("Check finished. Check encoding_check.txt")
