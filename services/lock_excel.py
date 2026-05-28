from filelock import FileLock
import pandas as pd

ARQUIVO_EXCEL = "estoque.xlsx"
LOCK_FILE = "estoque.xlsx.lock"

lock = FileLock(LOCK_FILE)

def adicionar_item(nome, quantidade):
    with lock:
        df = pd.read_excel(ARQUIVO_EXCEL)

        novo_item = {
            "nome": nome,
            "quantidade": quantidade
        }

        df = pd.concat([df, pd.DataFrame([novo_item])], ignore_index=True)

        df.to_excel(ARQUIVO_EXCEL, index=False)