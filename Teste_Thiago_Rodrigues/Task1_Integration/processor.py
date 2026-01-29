import pandas as pd
import zipfile
import os
import glob
import re

def extract_zip(zip_path, extract_to):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to

def identify_and_load_csv(file_path):
    """
    Tries to load a file with different encodings and delimiters.
    """
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    delimiters = [';', ',', '\t']
    
    for encoding in encodings:
        for sep in delimiters:
            try:
                # Read just first few lines to check
                df = pd.read_csv(file_path, sep=sep, encoding=encoding, nrows=5)
                if len(df.columns) > 1:
                    # Successfully read with multiple columns
                    return pd.read_csv(file_path, sep=sep, encoding=encoding, low_memory=False)
            except Exception:
                continue
    return None

def process_quarter_data(folder_path, year, quarter):
    """
    Processes all files in a folder, looking for 'Despesas' data.
    """
    all_files = glob.glob(os.path.join(folder_path, "**/*"), recursive=True)
    relevant_dfs = []
    
    for file_path in all_files:
        if os.path.isdir(file_path):
            continue
            
        # Check filename for hints, though we should also check content
        # Common names: "Demonstrações Contábeis", "Despesas"
        filename = os.path.basename(file_path).lower()
        
        df = None
        if filename.endswith('.csv') or filename.endswith('.txt'):
            df = identify_and_load_csv(file_path)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            try:
                df = pd.read_excel(file_path)
            except Exception:
                continue
        
        if df is not None:
            # Normalize columns to lowercase and remove spaces
            df.columns = [str(c).strip().lower() for c in df.columns]
            
            # Look for columns related to "Despesas com Eventos" or "Sinistros"
            # In ANS files, this usually falls under specific account codes or descriptions
            # Accounts starting with 4 (Despesas) are often what we need.
            # However, the task says "arquivos que contenham dados de Despesas com Eventos/Sinistros"
            # Often these are specific CSVs in the ZIP.
            
            # Let's check if the dataframe has typical columns like 'cnpj', 'valor', 'descricao'
            required_keywords = ['cnpj', 'raz', 'valor', 'termo', 'sinistro', 'evento', 'despesa']
            match_count = sum(1 for col in df.columns if any(key in col for key in required_keywords))
            
            if match_count >= 2:
                # Further filter rows if needed, or if the file IS the expense file.
                # Usually there's a column 'DESCRICAO' or 'CONTA' 
                # Account codes for expenses are 4xxxx
                
                # Check for Account Code column
                code_cols = [c for c in df.columns if 'cd_conta' in c or 'conta' in c or 'codigo' in c]
                if code_cols:
                    # Filter for account codes related to expenses (starting with 4)
                    # and specifically "Eventos Indenizáveis" or "Sinistros" (often 411)
                    # For this test, we'll try to keep it general but robust.
                    df[code_cols[0]] = df[code_cols[0]].astype(str)
                    # 411 is common for "Eventos Indenizáveis"
                    mask = df[code_cols[0]].str.startswith('4') 
                    relevant_df = df[mask].copy()
                else:
                    relevant_df = df.copy()
                
                if not relevant_df.empty:
                    # Map to standard names
                    col_map = {}
                    for col in relevant_df.columns:
                        if 'cnpj' in col: col_map[col] = 'CNPJ'
                        elif 'raz' in col: col_map[col] = 'RazaoSocial'
                        elif 'vl_' in col or 'valor' in col: col_map[col] = 'ValorDespesas'
                    
                    relevant_df = relevant_df.rename(columns=col_map)
                    
                    # Ensure necessary columns exist
                    for col in ['CNPJ', 'RazaoSocial', 'ValorDespesas']:
                        if col not in relevant_df.columns:
                            relevant_df[col] = None
                    
                    relevant_df['Trimestre'] = quarter
                    relevant_df['Ano'] = year
                    
                    relevant_dfs.append(relevant_df[['CNPJ', 'RazaoSocial', 'Trimestre', 'Ano', 'ValorDespesas']])
                    
    if not relevant_dfs:
        return pd.DataFrame(columns=['CNPJ', 'RazaoSocial', 'Trimestre', 'Ano', 'ValorDespesas'])
        
    return pd.concat(relevant_dfs, ignore_index=True)

def consolidate_data(dfs):
    combined = pd.concat(dfs, ignore_index=True)
    # Basic cleaning before saving
    combined['CNPJ'] = combined['CNPJ'].astype(str).str.replace(r'\D', '', regex=True).str.zfill(14)
    # Handle ValorDespesas conversion
    combined['ValorDespesas'] = pd.to_numeric(combined['ValorDespesas'].astype(str).str.replace(',', '.'), errors='coerce')
    return combined
