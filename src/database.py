import os
from dotenv import load_dotenv
from mssql_python import connect

# Carrega as variáveis do arquivo .env
load_dotenv()

def conectar_banco():
    string_conexao = os.getenv("SQL_CONNECTION_STRING")

    if not string_conexao:
        raise RuntimeError(
            "SQL_CONNECTION_STRING não encontrada. "
            "Verifique o arquivo .env."
        )
    return connect(string_conexao)