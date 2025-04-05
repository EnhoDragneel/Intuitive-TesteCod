import requests
from bs4 import BeautifulSoup
import os
import pdfplumber
import pandas as pd
import zipfile
import chardet
from sqlalchemy import text
from datetime import datetime, timedelta
from bd import criar_banco_se_nao_existir, conectar_engine


URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
PASTA_PDFS = "pdfs"
PASTA_CSV = "csvs"
PASTA_ZIP_ANOS = "zip_anos"
PASTA_CSV_OPERADORAS = "csv_operadoras"

# -------------------- TESTES 1 E 2 --------------------

def baixar_pdfs(url):
    os.makedirs(PASTA_PDFS, exist_ok=True)

    response = requests.get(url)
    if response.status_code != 200:
        print("Erro ao acessar a página:", response.status_code)
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = [
        a["href"] for a in soup.find_all("a", href=True)
        if ".pdf" in a["href"].lower() and "anexo" in a["href"].lower()
    ]

    arquivos_baixados = []
    for link in pdf_links:
        if not link.startswith("http"):
            link = "https://www.gov.br" + link

        nome_arquivo = os.path.join(PASTA_PDFS, link.split("/")[-1])
        pdf_response = requests.get(link)

        if pdf_response.status_code == 200:
            with open(nome_arquivo, "wb") as f:
                f.write(pdf_response.content)
            print(f"Download concluído: {nome_arquivo}")
            arquivos_baixados.append(nome_arquivo)
        else:
            print(f"Erro ao baixar {link}")

    return arquivos_baixados

def compactar_pdfs():
    zip_filename = "pdfs_compactados.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for pdf in os.listdir(PASTA_PDFS):
            zipf.write(os.path.join(PASTA_PDFS, pdf), pdf)
    print(f"PDFs compactados em {zip_filename}")
    return zip_filename

def encontrar_anexo(nome):
    arquivos = [pdf for pdf in os.listdir(PASTA_PDFS) if nome in pdf.lower()]
    return os.path.join(PASTA_PDFS, arquivos[0]) if arquivos else None

def extrair_tabelas_do_pdf(arquivo_pdf):
    dados_tabela = []
    with pdfplumber.open(arquivo_pdf) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                dados_tabela.extend(table)

    df = pd.DataFrame(dados_tabela).dropna(how='all')
    return df

def processar_dataframe(df):
    if df.iloc[0].str.contains("PROCEDIMENTO", case=False, na=False).any():
        df = df.iloc[1:]

    nomes_colunas = [
        "PROCEDIMENTO", "RN(alteração)", "VIGÊNCIA", "OD", "AMB",
        "HCO", "HSO", "REF", "PAC", "DUT", "SUBGRUPO", "GRUPO", "CAPÍTULO"
    ]
    
    df.columns = nomes_colunas[:len(df.columns)]
    
    df = df.rename(columns={"AMB": "Seg. Ambulatorial", "OD": "Seg. Odontológica"})
    return df

def salvar_csv(df, nome_base):
    os.makedirs(PASTA_CSV, exist_ok=True)
    csv_file = os.path.join(PASTA_CSV, f"{nome_base}.csv")
    df.to_csv(csv_file, index=False, sep=";")
    print(f"Dados salvos em {csv_file}")
    return csv_file

def compactar_csv():
    zip_filename = "csvs_compactados.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for csv in os.listdir(PASTA_CSV):
            zipf.write(os.path.join(PASTA_CSV, csv), csv)
    print(f"CSVs compactados em {zip_filename}")
    return zip_filename

def importar_csv_para_postgres(csv_path, nome_tabela, append=False):
    engine = conectar_engine()
    encoding = detectar_encoding_csv(csv_path)
    df = pd.read_csv(csv_path, encoding=encoding, sep=";")

   
    if 'DATA' in df.columns:
        try:
            df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True, errors='coerce')  
        except Exception as e:
            print(f"Erro ao converter a coluna 'DATA': {e}")

    if_exists_mode = "append" if append else "replace"
    df.to_sql(nome_tabela, engine, if_exists=if_exists_mode, index=False)
    print(f"Tabela '{nome_tabela}' atualizada com sucesso!")


def importar_csv_com_pk(csv_path, nome_tabela):
    engine = conectar_engine()
    encoding = detectar_encoding_csv(csv_path)
    df = pd.read_csv(csv_path, encoding=encoding, sep=";")

    if 'DATA' in df.columns:
        try:
            df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True, errors='coerce')
        except Exception as e:
            print(f"Erro ao converter a coluna 'DATA': {e}")


    df.to_sql(nome_tabela, engine, if_exists="replace", index=False)
    print(f"Tabela '{nome_tabela}' criada com sucesso!")


    if "Registro_ANS" in df.columns:
        with engine.connect() as conn:
            try:
                conn.execute(text(f"""
                    ALTER TABLE "{nome_tabela}"
                    ADD PRIMARY KEY ("Registro_ANS");
                """))
                print(f"Chave primária definida na tabela '{nome_tabela}' (coluna 'Registro_ANS').")
            except Exception as e:
                print(f"Erro ao definir chave primária: {e}")
    else:
        print(f"A coluna 'Registro_ANS' não foi encontrada na tabela '{nome_tabela}'.")



def detectar_encoding_csv(caminho):
    with open(caminho, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


# -------------------- TESTE 3 --------------------

def baixar_arquivos_zip_ultimos_anos():
    """
    Acessa o repositório público e baixa os arquivos ZIP dos últimos dois anos (2023 e 2024).
    """
    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    anos = ["2023", "2024"]

    os.makedirs(PASTA_ZIP_ANOS, exist_ok=True)

    for ano in anos:
        url_ano = f"{base_url}{ano}/"
        response = requests.get(url_ano)

        if response.status_code != 200:
            print(f"Erro ao acessar {url_ano}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        zip_links = [
            a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".zip")
        ]

        for zip_file in zip_links:
            zip_url = f"{url_ano}{zip_file}"
            zip_path = os.path.join(PASTA_ZIP_ANOS, zip_file)

            if os.path.exists(zip_path):
                print(f"Arquivo {zip_file} já baixado.")
                continue

            print(f"Baixando {zip_url}...")
            zip_response = requests.get(zip_url)
            if zip_response.status_code == 200:
                with open(zip_path, "wb") as f:
                    f.write(zip_response.content)
                print(f"Download concluído: {zip_path}")
            else:
                print(f"Erro ao baixar {zip_url}")

def baixar_dados_operadoras():
    """
    Baixa os dados cadastrais das operadoras ativas em formato CSV.
    """
    url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
    os.makedirs(PASTA_CSV_OPERADORAS, exist_ok=True)

    caminho_csv = os.path.join(PASTA_CSV_OPERADORAS, "operadoras_ativas.csv")

    response = requests.get(url)
    if response.status_code == 200:
        with open(caminho_csv, "wb") as f:
            f.write(response.content)
        print(f"Download concluído: {caminho_csv}")
        importar_csv_com_pk(caminho_csv, "operadoras_ativas")
    else:
        print(f"Erro ao baixar {url}")

def extrair_zips_para_pasta(zip_dir=PASTA_ZIP_ANOS, destino="demonstracoes_contabeis_csv"):
    os.makedirs(destino, exist_ok=True)
    
    for nome_arquivo in os.listdir(zip_dir):
        if nome_arquivo.endswith(".zip"):
            caminho_zip = os.path.join(zip_dir, nome_arquivo)
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall(destino)
                print(f"Extraído: {caminho_zip} → {destino}")
'''          
    for nome_csv in os.listdir(destino):
        if nome_csv.endswith(".csv"):
            caminho_csv = os.path.join(destino, nome_csv)
            try:
                importar_csv_para_postgres(caminho_csv, "demonstracoes_contabeis", append=True)
            except Exception as e:
                print(f"Erro ao importar {caminho_csv}: {e}")
'''   

from sqlalchemy.sql import text
import pandas as pd

def consultar_maiores_despesas():
    engine = conectar_engine() 

    with engine.connect() as conn:
        print("\nTop 10 - Último Trimestre (dados disponíveis):")
        trimestre_query = """
        SELECT
            o."Razao_Social",
            SUM(REPLACE(NULLIF(d."VL_SALDO_FINAL", ''), ',', '.')::numeric) AS total_despesas
        FROM demonstracoes_contabeis d
        JOIN operadoras_ativas o ON d."REG_ANS" = o."Registro_ANS"
        WHERE d."DESCRICAO" ILIKE '%EVENTOS%'
          AND d."DESCRICAO" ILIKE '%CONHECIDOS%'
          AND d."DESCRICAO" ILIKE '%MEDICO%'
          AND d."DESCRICAO" ILIKE '%HOSPITALAR%'
        GROUP BY o."Razao_Social"
        ORDER BY total_despesas DESC
        LIMIT 10;
        """
        trimestre_df = pd.read_sql_query(text(trimestre_query), conn)
        print(trimestre_df)

        print("\nTop 10 - Último Ano (todos os dados disponíveis):")
        ano_query = """
        SELECT
            o."Razao_Social",
            SUM(REPLACE(NULLIF(d."VL_SALDO_FINAL", ''), ',', '.')::numeric) AS total_despesas
        FROM demonstracoes_contabeis d
        JOIN operadoras_ativas o ON d."REG_ANS" = o."Registro_ANS"
        WHERE d."DESCRICAO" ILIKE '%EVENTOS%'
          AND d."DESCRICAO" ILIKE '%CONHECIDOS%'
          AND d."DESCRICAO" ILIKE '%MEDICO%'
          AND d."DESCRICAO" ILIKE '%HOSPITALAR%'
        GROUP BY o."Razao_Social"
        ORDER BY total_despesas DESC
        LIMIT 10;
        """
        ano_df = pd.read_sql_query(text(ano_query), conn)
        print(ano_df)


# ------------------ EXECUÇÃO COMPLETA ------------------

criar_banco_se_nao_existir()
baixar_arquivos_zip_ultimos_anos()
extrair_zips_para_pasta()
baixar_dados_operadoras()
consultar_maiores_despesas()


arquivos_baixados = baixar_pdfs(URL)
if arquivos_baixados:
    compactar_pdfs()
    anexo_i = encontrar_anexo("anexo_i_rol")
    
    if anexo_i:
        df_i = extrair_tabelas_do_pdf(anexo_i)
        df_i = processar_dataframe(df_i)
        caminho_csv_i = salvar_csv(df_i, "Anexo_I")
        importar_csv_para_postgres(caminho_csv_i, "procedimentos_rol")
    
    
    compactar_csv()
else:
    print("Nenhum PDF baixado.")
