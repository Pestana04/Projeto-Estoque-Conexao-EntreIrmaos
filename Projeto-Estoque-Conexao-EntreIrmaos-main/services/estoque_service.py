import pandas as pd
import os
from datetime import datetime

import os

ARQUIVO = "estoque.xlsx"

# criar o banco 
def criar_estrutura():
    print("FUNÇÃO EXECUTOU")

def criar_estrutura():
    print("FUNÇÃO EXECUTOU")

    produtos = pd.DataFrame(columns=["produto", "categoria", "quantidade", "local"])
    entradas = pd.DataFrame(columns=["produto", "categoria", "quantidade", "local", "data"])
    saidas = pd.DataFrame(columns=["produto", "quantidade", "responsavel", "telefone", "data"])

    with pd.ExcelWriter(ARQUIVO, engine="openpyxl") as writer:
        produtos.to_excel(writer, sheet_name="produtos", index=False)
        entradas.to_excel(writer, sheet_name="entradas", index=False)
        saidas.to_excel(writer, sheet_name="saidas", index=False)

# registro da entrada  
def registrar_entrada(produto, categoria, quantidade, local):

    entradas = pd.read_excel(
        ARQUIVO,
        sheet_name="entradas"
    )

    nova_entrada = pd.DataFrame({
        "produto": [produto],
        "categoria": [categoria],
        "quantidade": [quantidade],
        "local": [local],
        "data": [datetime.now()]
    })

    entradas = pd.concat(
        [entradas, nova_entrada],
        ignore_index=True
    )

    with pd.ExcelWriter(
        ARQUIVO,
        mode="a",
        if_sheet_exists="replace",
        engine="openpyxl"
    ) as writer:

        entradas.to_excel(
            writer,
            sheet_name="entradas",
            index=False
        )

    atualizar_estoque(
        produto,
        categoria,
        quantidade,
        local
    )

# atualizar o estoque
def atualizar_estoque(produto, categoria, quantidade, local):

    produtos = pd.read_excel(
        ARQUIVO,
        sheet_name="produtos"
    )

    if produto in produtos["produto"].values:

        produtos.loc[
            produtos["produto"] == produto,
            "quantidade"
        ] += quantidade

    else:

        novo = pd.DataFrame({
            "produto": [produto],
            "categoria": [categoria],
            "quantidade": [quantidade],
            "local": [local]
        })

        produtos = pd.concat(
            [produtos, novo],
            ignore_index=True
        )

    with pd.ExcelWriter(
        ARQUIVO,
        mode="a",
        if_sheet_exists="replace",
        engine="openpyxl"
    ) as writer:

        produtos.to_excel(
            writer,
            sheet_name="produtos",
            index=False
        )

# saida
def registrar_saida(produto, quantidade, responsavel, telefone):

    saidas = pd.read_excel(
        ARQUIVO,
        sheet_name="saidas"
    )

    nova_saida = pd.DataFrame({
        "produto": [produto],
        "quantidade": [quantidade],
        "responsavel": [responsavel],
        "telefone": [telefone],
        "data": [datetime.now()]
    })

    saidas = pd.concat(
        [saidas, nova_saida],
        ignore_index=True
    )

    with pd.ExcelWriter(
        ARQUIVO,
        mode="a",
        if_sheet_exists="replace",
        engine="openpyxl"
    ) as writer:

        saidas.to_excel(
            writer,
            sheet_name="saidas",
            index=False
        )

    produtos = pd.read_excel(
        ARQUIVO,
        sheet_name="produtos"
    )

    produtos.loc[
        produtos["produto"] == produto,
        "quantidade"
    ] -= quantidade

    with pd.ExcelWriter(
        ARQUIVO,
        mode="a",
        if_sheet_exists="replace",
        engine="openpyxl"
    ) as writer:

        produtos.to_excel(
            writer,
            sheet_name="produtos",
            index=False
        )
        
criar_estrutura()

# registrar_entrada(
#     "Arroz",
#     "Alimento",
#     10,
#     "Instituto"
# )