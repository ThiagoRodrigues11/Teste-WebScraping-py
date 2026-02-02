import pandas as pd
import os
import re

def validate_cnpj(cnpj):
    """
    Valida CNPJ usando regex e algoritmo de dígitos verificadores.
    """
    cnpj = re.sub(r'\D', '', str(cnpj))
    
    if len(cnpj) != 14:
        return False
    
    # CNPJs com todos os números iguais são inválidos
    if cnpj == cnpj[0] * 14:
        return False
    
    # Algoritmo de validação
    def calculate_digit(cnpj, weights):
        sum_val = sum(int(digit) * weight for digit, weight in zip(cnpj, weights))
        result = sum_val % 11
        return 0 if result < 2 else 11 - result

    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    digit1 = calculate_digit(cnpj[:12], weights1)
    digit2 = calculate_digit(cnpj[:13], weights2)
    
    return cnpj[-2:] == f"{digit1}{digit2}"

def main():
    # Caminhos
    # Pega o diretório raiz do projeto (subindo de src/ e desafio_02...)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_path = os.path.join(base_dir, "desafio_01_api_ans", "output", "consolidado_despesas.csv")
    output_dir = os.path.join(base_dir, "desafio_02_transformacao_validacao", "output")
    
    print(f"Lendo dados de: {input_path}")
    
    # 2.1. Validação de Dados
    # Vamos carregar o CSV consolidado do teste 1.3
    try:
        # Lendo com low_memory=False para evitar o aviso de Dtype
        df = pd.read_csv(input_path, low_memory=False, encoding='utf-8-sig')
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    print(f"Total de registros carregados: {len(df)}")

    # Implementando validações
    # 1. Razão Social não vazia
    df['razao_social_valida'] = df['RazaoSocial'].notna() & (df['RazaoSocial'].str.strip() != '')
    
    # 2. Valores numéricos positivos
    df['valor_positivo'] = df['ValorDespesas'] >= 0
    
    # 3. CNPJ válido
    print("Validando CNPJs (isso pode levar um tempo dependendo do volume)...")
    df['cnpj_valido'] = df['CNPJ'].apply(validate_cnpj)

    # Filtragem dos dados válidos
    df_clean = df[df['razao_social_valida'] & df['valor_positivo'] & df['cnpj_valido']].copy()
    print(f"Registros válidos: {len(df_clean)}")

    # 2.2. Enriquecimento de Dados
    cadop_url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
    cadop_path = os.path.join(base_dir, "desafio_02_transformacao_validacao", "data", "Relatorio_cadop.csv")
    
    if not os.path.exists(cadop_path):
        print(f"Baixando dados cadastrais de: {cadop_url}")
        import requests
        response = requests.get(cadop_url)
        with open(cadop_path, 'wb') as f:
            f.write(response.content)
    
    print("Lendo dados cadastrais...")
    # O arquivo da ANS costuma usar latin-1 ou cp1252 e separador ';'
    try:
        df_cadop = pd.read_csv(cadop_path, sep=';', encoding='utf-8-sig')
    except:
        df_cadop = pd.read_csv(cadop_path, sep=';', encoding='latin-1')

    # Limpeza básica do cadastro para o join
    # Garantir que CNPJ seja string e formatado uniformemente
    df_cadop['CNPJ'] = df_cadop['CNPJ'].astype(str).str.replace(r'\D', '', regex=True).str.zfill(14)
    df_clean['CNPJ'] = df_clean['CNPJ'].astype(str).str.replace(r'\D', '', regex=True).str.zfill(14)

    # Tratar CNPJs duplicados no cadastro (Estratégia: keep first)
    df_cadop = df_cadop.drop_duplicates(subset=['CNPJ'])

    print("Fazendo o Join das tabelas...")
    # Colunas desejadas: RegistroANS, Modalidade, UF
    # No CSV da ANS os nomes são: REGISTRO_OPERADORA, Modalidade, UF
    cols_to_keep = ['CNPJ', 'REGISTRO_OPERADORA', 'Modalidade', 'UF']
    
    df_enriched = pd.merge(df_clean, df_cadop[cols_to_keep], on='CNPJ', how='left')
    df_enriched = df_enriched.rename(columns={'REGISTRO_OPERADORA': 'RegistroANS'})

    # 2.3. Agregação
    print("Agrupando e calculando métricas...")
    # Preencher nulos para garantir que apareçam no agrupamento
    df_enriched['UF'] = df_enriched['UF'].fillna('N/A')
    df_enriched['Modalidade'] = df_enriched['Modalidade'].fillna('N/A')
    df_enriched['RegistroANS'] = df_enriched['RegistroANS'].fillna('N/A')

    # Cálculo correto da média por trimestre:
    # 1. Primeiro somamos as despesas por operadora/UF em cada trimestre individual
    df_quarterly = df_enriched.groupby(['CNPJ', 'RazaoSocial', 'RegistroANS', 'Modalidade', 'UF', 'Ano', 'Trimestre']).agg(
        Soma_Trimestre=('ValorDespesas', 'sum')
    ).reset_index()

    # 2. Agora calculamos o Total, a Média dos trimestres e o Desvio Padrão
    agregado = df_quarterly.groupby(['CNPJ', 'RazaoSocial', 'RegistroANS', 'Modalidade', 'UF']).agg(
        Total_Despesas=('Soma_Trimestre', 'sum'),
        Media_Trimestral=('Soma_Trimestre', 'mean'), 
        Desvio_Padrao_Despesas=('Soma_Trimestre', 'std')
    ).reset_index()

    # Ordenar por valor total (maior para menor)
    agregado = agregado.sort_values(by='Total_Despesas', ascending=False)

    # Salvar resultado
    output_file = os.path.join(output_dir, "despesas_agregadas.csv")
    agregado.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Resultado salvo em: {output_file}")

    # Compactar em ZIP
    import zipfile
    zip_path = os.path.join(base_dir, "Teste_Thiago_Rodrigues.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(output_file, arcname="despesas_agregadas.csv")
    
    print(f"Arquivo final compactado em: {zip_path}")

if __name__ == "__main__":
    main()
