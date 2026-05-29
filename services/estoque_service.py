import os
from datetime import datetime
import pandas as pd

ARQUIVO = "estoque.xlsx"


# ==========================================
# 1. ESTRUTURA DO BANCO DE DADOS (EXCEL)
# ==========================================
def criar_estrutura():
    """Verifica se o estoque.xlsx está vazio ou sem as abas corretas.

    Se estiver, cria a estrutura inicial para o sistema não quebrar.
    """
    precisa_criar = False

    # Se o arquivo não existir ou se existir mas estiver com 0 bytes (totalmente vazio)
    if not os.path.exists(ARQUIVO) or os.path.getsize(ARQUIVO) == 0:
        precisa_criar = True
    else:
        # Se o arquivo existe, checa se as abas obrigatórias estão lá dentro
        try:
            with pd.ExcelFile(ARQUIVO) as xls:
                if (
                        "produtos" not in xls.sheet_names
                        or "entradas" not in xls.sheet_names
                        or "saidas" not in xls.sheet_names
                ):
                    precisa_criar = True
        except Exception:
            precisa_criar = True

    if precisa_criar:
        print(
            f"🔄 O arquivo '{ARQUIVO}' estava vazio ou incompleto. Inicializando abas obrigatórias..."
        )
        produtos = pd.DataFrame(
            columns=["produto", "categoria", "quantidade", "local"]
        )
        entradas = pd.DataFrame(
            columns=["produto", "categoria", "quantidade", "local", "data"]
        )
        saidas = pd.DataFrame(
            columns=[
                "produto",
                "quantidade",
                "responsavel",
                "telefone",
                "data",
            ]
        )

        with pd.ExcelWriter(ARQUIVO, engine="openpyxl") as writer:
            produtos.to_excel(writer, sheet_name="produtos", index=False)
            entradas.to_excel(writer, sheet_name="entradas", index=False)
            saidas.to_excel(writer, sheet_name="saidas", index=False)
        print(f"✅ Estrutura do banco de dados gerada com sucesso no '{ARQUIVO}'!")
    else:
        print(f"💻 Banco de dados '{ARQUIVO}' pronto para uso.")


def salvar_todas_as_abas(df_produtos, df_entradas, df_saidas):
    """Função utilitária segura para salvar todas as abas de uma vez só,

    evitando que o Excel apague dados de abas não editadas.
    """
    with pd.ExcelWriter(ARQUIVO, engine="openpyxl") as writer:
        df_produtos.to_excel(writer, sheet_name="produtos", index=False)
        df_entradas.to_excel(writer, sheet_name="entradas", index=False)
        df_saidas.to_excel(writer, sheet_name="saidas", index=False)


# ==========================================
# 2. FUNÇÕES DE MOVIMENTAÇÃO (ENTRADAS E SAÍDAS)
# ==========================================
def registrar_entrada(
        produto, categoria, quantidade, local, data_customizada=None
):
    # Forçar padronização do nome do produto (Tudo em maiúsculo e sem espaços sobrando)
    produto_limpo = str(produto).strip().upper()
    categoria_limpa = str(categoria).strip().upper()

    # Garante que as abas existam antes de tentar ler
    criar_estrutura()

    # Ler todas as abas atuais
    produtos = pd.read_excel(ARQUIVO, sheet_name="produtos")
    entradas = pd.read_excel(ARQUIVO, sheet_name="entradas")
    saidas = pd.read_excel(ARQUIVO, sheet_name="saidas")

    data_registro = data_customizada or datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Registrar na aba Entradas
    nova_entrada = pd.DataFrame(
        {
            "produto": [produto_limpo],
            "categoria": [categoria_limpa],
            "quantidade": [quantidade],
            "local": [local],
            "data": [data_registro],
        }
    )
    entradas = pd.concat([entradas, nova_entrada], ignore_index=True)

    # Atualizar a aba Produtos (Estoque)
    if (
            not produtos.empty
            and produto_limpo in produtos["produto"].astype(str).values
    ):
        produtos.loc[
            produtos["produto"].astype(str) == produto_limpo, "quantidade"
        ] += quantidade
    else:
        novo_produto = pd.DataFrame(
            {
                "produto": [produto_limpo],
                "categoria": [categoria_limpa],
                "quantidade": [quantidade],
                "local": [local],
            }
        )
        produtos = pd.concat([produtos, novo_produto], ignore_index=True)

    # Gravar as alterações de forma segura
    salvar_todas_as_abas(produtos, entradas, saidas)
    print(f"📦 Entrada de {quantidade}x {produto_limpo} registrada!")


def registrar_saida(produto, quantidade, responsavel, telefone):
    produto_limpo = str(produto).strip().upper()

    # Garante que as abas existam antes de tentar ler
    criar_estrutura()

    produtos = pd.read_excel(ARQUIVO, sheet_name="produtos")
    entradas = pd.read_excel(ARQUIVO, sheet_name="entradas")
    saidas = pd.read_excel(ARQUIVO, sheet_name="saidas")

    # Verificar se o produto existe e tem quantidade suficiente
    if (
            produtos.empty
            or produto_limpo not in produtos["produto"].astype(str).values
    ):
        print(f"❌ Erro: O produto '{produto_limpo}' não existe no estoque.")
        return

    qtd_atual = produtos.loc[
        produtos["produto"].astype(str) == produto_limpo, "quantidade"
    ].values[0]
    if qtd_atual < quantidade:
        print(
            f"❌ Erro: Estoque insuficiente para '{produto_limpo}'. Disponível: {qtd_atual}"
        )
        return

    # Registrar na aba Saídas
    nova_saida = pd.DataFrame(
        {
            "produto": [produto_limpo],
            "quantidade": [quantidade],
            "responsavel": [responsavel],
            "telefone": [telefone],
            "data": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        }
    )
    saidas = pd.concat([saidas, nova_saida], ignore_index=True)

    # Deduzir do estoque
    produtos.loc[
        produtos["produto"].astype(str) == produto_limpo, "quantidade"
    ] -= quantidade

    salvar_todas_as_abas(produtos, entradas, saidas)
    print(f"🤝 Saída de {quantidade}x {produto_limpo} registrada!")


# ==========================================
# 3. CARGA INICIAL DE DADOS (DATA INGESTION)
# ==========================================
def realizar_carga_inicial(caminho_planilha_velha):
    """Lê a planilha antiga fornecida pelo Lucas, limpa os dados bagunçados

    e joga no formato novo do sistema.
    """
    if not os.path.exists(caminho_planilha_velha):
        print(
            f"⚠️ Arquivo antigo '{caminho_planilha_velha}' não foi encontrado. Aguardando planilha do Lucas."
        )
        return

    print("🚀 Iniciando a carga inicial de dados...")

    # Lê a planilha antiga enviada
    df_velho = pd.read_excel(caminho_planilha_velha)
    df_velho = df_velho.dropna(how="all")

    for _, linha in df_velho.iterrows():
        # Captura as colunas (tenta nomes comuns, se não achar usa valor padrão)
        nome_item = linha.get("Item", linha.get("produto", None))
        categoria_item = linha.get("Tipo", linha.get("categoria", "DIVERSOS"))
        qtd_item = linha.get("Quantidade", linha.get("quantidade", 0))
        local_item = linha.get("Local", "Estoque Geral")

        if pd.isna(nome_item):
            continue

        produto_limpo = str(nome_item).strip().upper()
        categoria_limpa = str(categoria_item).strip().upper()

        try:
            quantidade_limpa = int(float(qtd_item))
        except (ValueError, TypeError):
            quantidade_limpa = 0

        if quantidade_limpa > 0 and produto_limpo != "NAN":
            # Usa a nossa função de entrada passando uma tag de histórico na data
            registrar_entrada(
                produto=produto_limpo,
                categoria=categoria_limpa,
                quantidade=quantidade_limpa,
                local=local_item,
                data_customizada="HISTORICO_ONG_"
                                 + datetime.now().strftime("%Y-%m-%d"),
            )

    print("🎯 Carga inicial concluída com sucesso!")


# ==========================================
# EXECUÇÃO DE TESTE
# ==========================================
if __name__ == "__main__":
    print("--- INICIANDO TESTE DO ESTOQUE SERVICE ---")

    # 1. Testando uma entrada manual (Isso vai criar as abas no seu Excel vazio automaticamente!)
    registrar_entrada("Arroz 5kg", "Alimento", 50, "Prateleira A")

    # 2. Testando uma saída
    registrar_saida("Arroz 5kg", 10, "João da Silva", "11999999999")

    # 3. Carga inicial (Descomente e mude o nome do arquivo quando o Lucas te entregar a planilha)
    # realizar_carga_inicial("planilha_do_lucas_padilha.xlsx")