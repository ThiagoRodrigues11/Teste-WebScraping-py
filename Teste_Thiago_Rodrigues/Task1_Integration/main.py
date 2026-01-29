from ans_api import get_latest_quarters, download_file
from processor import extract_zip, process_quarter_data, consolidate_data
import os
import zipfile
import pandas as pd

def run_task1():
    print("Starting Task 1: API Integration and Data Processing...")
    
    # 1. Identify quarters
    latest_quarters = get_latest_quarters(limit=3)
    print(f"Identified quarters: {[(y, q) for y, q, u in latest_quarters]}")
    
    all_quarter_dfs = []
    data_dir = os.path.join(os.getcwd(), "..", "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    for year, q, url in latest_quarters:
        # 2. Download
        zip_path = download_file(url, data_dir)
        
        # 3. Extract
        extract_folder = os.path.join(data_dir, f"{year}T{q}")
        extract_zip(zip_path, extract_folder)
        
        # 4. Process
        print(f"Processing data for {year} Q{q}...")
        df = process_quarter_data(extract_folder, year, q)
        print(f"Found {len(df)} records for {year} Q{q}")
        all_quarter_dfs.append(df)
    
    # 5. Consolidate
    if all_quarter_dfs:
        consolidated_df = consolidate_data(all_quarter_dfs)
        output_csv = os.path.join(data_dir, "consolidado_despesas.csv")
        consolidated_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        print(f"Consolidated data saved to {output_csv}")
        
        # 6. Archive
        zip_output = os.path.join(data_dir, "consolidado_despesas.zip")
        with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(output_csv, arcname=os.path.basename(output_csv))
        print(f"Final ZIP created: {zip_output}")
    else:
        print("No data found to consolidate.")

if __name__ == "__main__":
    run_task1()
