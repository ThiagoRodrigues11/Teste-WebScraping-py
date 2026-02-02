import os
import zipfile
import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = BASE_DIR / "output"

RAW_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# 1️⃣ Cadastro de operadoras (CNPJ + Razão Social)
# ==================================================

def baixar_cadastro_operadoras():
    url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude/Relatorio_cadop.csv"
    destino = RAW_DIR / "cadastro_operadoras.csv"

    if destino.exists():
        print("✅ Cadastro de operadoras já existe.")
        return destino

    print("📥 Baixando cadastro de operadoras da ANS...")
    r = requests.get(url)
    r.raise_for_status()
    destino.write_bytes(r.content)
    print("✅ Cadastro salvo.")
    return destino


def carregar_cadastro_operadoras():
    path = baixar_cadastro_operadoras()

    df = pd.read_csv(path, sep=";", encoding="utf-8-sig", dtype=str)

    print("\n🔎 COLUNAS DO CADASTRO:")
    print(df.columns.tolist())

    # 🔥 PADRONIZAÇÃO CORRETA
    df = df.rename(columns={
        "REGISTRO_OPERADORA": "REG_ANS",
        "Razao_Social": "RazaoSocial"
    })

    df["REG_ANS"] = df["REG_ANS"].str.strip()

    print("\n🔎 PREVIEW CADASTRO (CHAVE CORRETA):")
    print(df[["REG_ANS", "CNPJ", "RazaoSocial"]].head())

    return df[["REG_ANS", "CNPJ", "RazaoSocial"]]


# ==================================================
# 2️⃣ Consolidação das despesas
# ==================================================

def consolidar_despesas():
    cadastro = carregar_cadastro_operadoras()
    dfs = []

    for pasta in RAW_DIR.iterdir():
        if not pasta.is_dir():
            continue
        if "2025" not in pasta.name:
            continue

        for arquivo in pasta.glob("*.csv"):
            print(f"\n📄 Lendo {arquivo}...")
            df = pd.read_csv(arquivo, sep=";", encoding="utf-8-sig", dtype=str)

            print("🔎 COLUNAS DESPESAS:")
            print(df.columns.tolist())

            # Renomeia coluna correta de valor
            df = df.rename(columns={
                "VL_SALDO_FINAL": "ValorDespesas"
            })

            ano = pasta.name.split("_")[0]
            trimestre = pasta.name.split("_")[1]

            df["Ano"] = ano
            df["Trimestre"] = trimestre
            df["REG_ANS"] = df["REG_ANS"].str.strip()

            df = df[["REG_ANS", "Ano", "Trimestre", "ValorDespesas"]]

            print("\n🔎 PREVIEW DESPESAS:")
            print(df.head())

            dfs.append(df)

    despesas = pd.concat(dfs, ignore_index=True)

    despesas["ValorDespesas"] = (
        despesas["ValorDespesas"]
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # ==================================================
    # 3️⃣ MERGE CORRETO
    # ==================================================

    final = despesas.merge(
        cadastro,
        on="REG_ANS",
        how="left",
        validate="many_to_one"
    )

    print("\n🔎 PREVIEW APÓS MERGE:")
    print(final.head())

    # ==================================================
    # 4️⃣ Tratamento de inconsistências
    # ==================================================

    final["CNPJ"] = final["CNPJ"].fillna("DESCONHECIDO")
    final["RazaoSocial"] = final["RazaoSocial"].fillna("DESCONHECIDO")

    final = final[[
        "CNPJ",
        "RazaoSocial",
        "Trimestre",
        "Ano",
        "ValorDespesas"
    ]]

    print("\n🔎 COLUNAS FINAIS:")
    print(final.columns.tolist())

    print("\n🔎 PREVIEW FINAL:")
    print(final.head())

    # ==================================================
    # 5️⃣ Exportação CSV + ZIP
    # ==================================================

    csv_path = OUTPUT_DIR / "consolidado_despesas.csv"
    zip_path = OUTPUT_DIR / "consolidado_despesas.zip"

    final.to_csv(csv_path, index=False, encoding="utf-8-sig")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(csv_path, arcname="consolidado_despesas.csv")

    print("\n✅ CONSOLIDAÇÃO FINALIZADA COM SUCESSO")
    print(f"📦 {zip_path}")


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":
    consolidar_despesas()
