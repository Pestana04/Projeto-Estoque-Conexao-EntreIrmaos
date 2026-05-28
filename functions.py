import pandas as pd
import os

class GerenciadorEstoque:
    # O método __init__ é executado automaticamente quando criamos o gerenciador
    def __init__(self, caminho_arquivo):
        self.caminho = caminho_arquivo
        self.df = pd.read_csv(self.caminho)
        
    def registrar_entrada(self, nome, categoria, quantidade, local, validade=None):
        filtro = (
            (self.df['nome'] == nome) & 
            (self.df['categoria'] == categoria) & 
            (self.df['local'] == local)
        )
        
        if self.df[filtro].empty:
            novo_item = pd.DataFrame([{
                'nome': nome, 
                'categoria': categoria, 
                'quantidade': quantidade, 
                'local': local,
                'validade': validade
            }])
            self.df = pd.concat([self.df, novo_item], ignore_index=True)
            print(f'Novo item cadastrado: {nome}.')
            
        else:
            indice = self.df[filtro].index[0]
            self.df.at[indice, 'quantidade'] += quantidade
            print(f'Quantidade atualizada para o item: {nome}.')

    def registrar_saida(self,nome,categoria,local,quantidade_retirar,nome_pessoa,telefone):
        filtro = (
            (self.df['nome'] == nome) &
            (self.df['categoria'] == categoria) &
            (self.df['local'] == local)
        )

        if self.df[filtro].empty:
            print(f'Erro: O produto "{nome}" não foi encontrado em {local}.')
            return False
        
        indice = self.df[filtro].index[0]
        quantidade_atual = self.df.at[indice, 'quantidade']

        if quantidade_retirar > quantidade_atual:
            print(f'Erro: não é possível retirar {quantidade_retirar}, pois temos um estoque de {quantidade_atual}.')
            return False
        
        self.df.at[indice, 'quantidade'] -= quantidade_retirar

        print(f'Saída autorizada: {quantidade_retirar}x "{nome}".')
        print(f'Estoque atualizado: "{nome}": {self.df.at[indice, 'quantidade']} restantes')

    def salvar_planilha(self):
        self.df.to_csv(self.caminho, index=False)
        print('Planilha salva com sucesso!')


