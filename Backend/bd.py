import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "01563853"
DB_HOST = "localhost"
DB_PORT = "5432"

def criar_banco_se_nao_existir():
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Banco de dados '{DB_NAME}' criado com sucesso!")
    else:
        print(f"Banco de dados '{DB_NAME}' já existe.")

    cursor.close()
    conn.close()

def conectar_engine():
    """Retorna engine do SQLAlchemy."""
    return create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def conectar_banco_psycopg2():
    """Retorna conexão psycopg2 ao banco criado."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
