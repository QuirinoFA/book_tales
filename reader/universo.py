import json
import os
import datetime


class Universo:
    def __init__(self, nome:str):
        self.caminho = os.path.join(*["C:\\", "Users", "felip", "OneDrive", "Documentos", "Tabela_Relacional.json"])
        self.nome = nome
        if self.existe(nome):
            with open(self.caminho, mode='r', encoding='utf-8') as t:
                tabela = json.load(t)
                for i in tabela:
                    if i['Nome'] == self.nome:
                        self.id = i['ID']
                        self.resumo = i['Resumo']
                        self.texto = i['Texto']
                        self.criado = i['Criado']
                        self.alterado = i['Alterado']
        else:
            with open(self.caminho, mode='r', encoding='utf-8') as t:
                try:
                    tabela = json.load(t)
                    self.id = len(tabela)
                except json.JSONDecodeError:
                    self.id = 0
            self.resumo = None
            self.texto = None
            self.criado = None
            self.alterado = None

    def existe(self, exi_uni:str) ->bool:
        if os.path.exists(self.caminho):
            with open(self.caminho, mode='r', encoding='utf-8') as j_exi:
                try:
                    tab_exi = json.load(j_exi)
                    for tab_item in tab_exi:
                        if tab_item['Nome'] == exi_uni:
                            return True
                    return False
                except json.JSONDecodeError:
                    return False
        else:
            lis_exi_uni = []
            with open(self.caminho, mode='w', encoding='utf-8') as l_e_u:
                json.dump(lis_exi_uni, l_e_u, ensure_ascii=False, allow_nan=False, indent=4)
            return False

    def criar(self, c_res:str=None, c_tex:str=None) ->None:
        if self.existe(self.nome):
            print('ERRO! Universo já existe!')
            return
        else:
            self.resumo = c_res
            self.texto = c_tex
            self.criado = str(datetime.datetime.now())
            novo_uni = {
                'ID': self.id,
                'Nome': self.nome,
                'Resumo': self.resumo,
                'Texto': self.texto,
                'Criado': self.criado,
                'Alterado': self.alterado
            }
            with open(self.caminho, mode='w', encoding='utf-8') as j_cri:
                try:
                    tab_cri = json.load(j_cri)
                    tab_cri.append(novo_uni)
                    json.dump(tab_cri, j_cri, ensure_ascii=False, allow_nan=False, indent=4)
                except:
                    novo_list_uni = [novo_uni]
                    json.dump(novo_list_uni, j_cri, ensure_ascii=False, allow_nan=False, indent=4)
            return

    def alterar(self, a_nom:str, a_res:str=None, a_tex:str=None) ->None:
        if self.existe(self.nome):
            with open(self.caminho, mode='w', encoding='utf-8') as j_alt:
                tab_alt = json.load(j_alt)
                for a_item in tab_alt:
                    if a_item['Nome'] == self.nome:
                        a_item['Nome'] = a_nom
                        a_item['Resumo'] = a_res
                        a_item['Texto'] = a_tex
                        a_item['Alterado'] = str(datetime.datetime.now())
                json.dump(tab_alt, j_alt, ensure_ascii=False, allow_nan=False, indent=4)
            return
        else:
            print('ERRO! Universo não existe!')
            return

    def ler(self) ->None:
        if self.existe(self.nome):
            with open(self.caminho, mode='r', encoding='utf-8') as j_ler:
                tab_ler = json.load(j_ler)
                for l_item in tab_ler:
                    if l_item['Nome'] == self.nome:
                        for i, j in l_item.items():
                            print(f'{i}: {j}')
            return
        else:
            print('ERRO! Universo não existe!')
            return

def salvar_universo() ->None:
    while True:
        su_nome = str(input('Nome: '))
        if su_nome:
            break
        else:
            print('ERRO! Digite um nome para o universo!')
    su_resumo = str(input('Resumo: '))
    su_linhas = []
    su_aux = 0
    while True:
        su_l = str(input('Texto [ENTER 2 vzs para sair]:'))
        if su_l == '':
            su_aux += 1
            if su_aux > 1:
                break
        else:
            su_aux = 0
        su_linhas.append(su_l)
    su_texto = '\n'.join(su_linhas)
    su_salva = Universo(su_nome)
    su_salva.criar(su_resumo, su_texto)

def ler_universo() ->None:
    while True:
        lu_nome = str(input('Nome: '))
        if lu_nome:
            break
        else:
            print('ERRO! Digite um nome!')
    lu_uni = Universo(lu_nome)
    lu_uni.ler()
