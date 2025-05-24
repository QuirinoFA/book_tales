import json
import os
import datetime


caminho = os.path.join(*["C:\\", "Users", "felip", "OneDrive", "Documentos", "Tabela_Relacional.json"])

class Universo:
    def __init__(self):
        self.nome = None
        self.resumo = None
        self.criado = None
        self.alterado = None
        self.repositorio = RepositorioUniverso()

    def para_dict(self) ->dict:
        dic_universo = {
            'Nome': self.nome,
            'Resumo': self.resumo,
            'Criado': self.criado,
            'Alterado': self.alterado
        }
        return dic_universo

    def criar(self, c_nome:str, c_resumo:str) ->None:
        if self.repositorio.existe_universo(c_nome):
            raise UniversoJaExiste(caminho)
        else:
            self.nome = c_nome
            self.resumo = c_resumo
            self.criado = str(datetime.datetime.now())
            self.alterado = None
            novo_universo = self.para_dict()
            self.repositorio.salvar_universo(novo_universo)

    def ler(self, l_nome:str) ->None:
        l_universo = self.repositorio.ler_universo(l_nome)
        self.nome = l_universo['Nome']
        self.resumo = l_universo['Resumo']
        self.criado = l_universo['Criado']
        self.alterado = l_universo['Alterado']

    def atualizar(self, a_nome:str, a_resumo:str) ->None:
        v_universo = self.repositorio.ler_universo(self.nome)
        v_nome = self.nome
        self.nome = a_nome
        self.resumo = a_resumo
        self.criado = v_universo['Criado']
        self.alterado = str(datetime.datetime.now())
        a_universo = self.para_dict()
        self.repositorio.atualizar_universo(v_nome, a_universo)

    def deletar(self) ->None:
        self.repositorio.deletar_universo(self.nome)
        self.nome = None
        self.resumo = None
        self.criado = None
        self.alterado = None


class ErroArquivo(Exception):
    pass

class ArquivoNaoEncontrado(ErroArquivo):
    def __init__(self, a_n_e_caminho):
        self.caminho = a_n_e_caminho
        super().__init__(f"Arquivo não encontrado. Caminho: {self.caminho}")

class ArquivoCorrompido(ErroArquivo):
    def __init__(self, a_c_caminho):
        self.caminho = a_c_caminho
        super().__init__(f"Arquivo corrompido. Caminho: {self.caminho}")

class ErroUniverso(Exception):
    pass

class UniversoJaExiste(ErroUniverso):
    def __init__(self, u_j_e_caminho):
        self.caminho = u_j_e_caminho
        super().__init__(f"Universo já existe. Caminho {self.caminho}")

class UniversoNaoEncontrado(ErroUniverso):
    def __init__(self,  u_n_e_caminho):
        self.caminho = u_n_e_caminho
        super().__init__(f"Universo não encontrado. Caminho {self.caminho}")

class RepositorioUniverso:
    def __init__(self):
        self.caminho = caminho

    def ler_arquivo(self) -> list:
        try:
            with open(self.caminho, mode='r', encoding='utf-8') as j_l_a:
                tab_l_a = json.load(j_l_a)
            return tab_l_a
        except FileNotFoundError:
            raise ArquivoNaoEncontrado(self.caminho)
        except json.JSONDecodeError:
            raise ArquivoCorrompido(self.caminho)

    def salvar_arquivo(self, tab_s_a:list) -> bool:
        try:
            with open(self.caminho, mode='w', encoding='utf-8') as j_s_a:
                json.dump(tab_s_a, j_s_a, ensure_ascii=False, allow_nan=False, indent=4)
            return True
        except FileNotFoundError:
            raise ArquivoNaoEncontrado(self.caminho)
        except json.JSONDecodeError:
            raise ArquivoCorrompido(self.caminho)

    def existe_universo(self, e_u_nome:str) -> bool:
        tab_e_u = self.ler_arquivo()
        for e_universo in tab_e_u:
            if e_universo.get('Nome') == e_u_nome:
                return True
        return False

    def salvar_universo(self, s_u_novo:dict) ->bool:
        tab_s_u = self.ler_arquivo()
        tab_s_u.append(s_u_novo.copy())
        self.salvar_arquivo(tab_s_u)
        return True

    def ler_universo(self, l_u_nome:str) ->dict:
        tab_l_u = self.ler_arquivo()
        for l_universo in tab_l_u:
            if l_universo.get('Nome') == l_u_nome:
                return l_universo
        raise UniversoNaoEncontrado(self.caminho)

    def atualizar_universo(self, v_u_nome:str, a_u_universo:dict) ->bool:
        tab_a_u = self.ler_arquivo()
        for a_universo in tab_a_u:
            if a_universo['Nome'] == v_u_nome:
                a_universo['Nome'] = a_u_universo['Nome']
                a_universo['Resumo'] = a_u_universo['Resumo']
                a_universo['Criado'] = a_u_universo['Criado']
                a_universo['Alterado'] = a_u_universo['Alterado']
                self.salvar_arquivo(tab_a_u)
                return True
        raise UniversoNaoEncontrado(self.caminho)

    def deletar_universo(self, d_u_nome:str) ->bool:
        tab_d_u = self.ler_arquivo()
        for d_universo in tab_d_u:
            if d_universo['Nome'] == d_u_nome:
                tab_d_u.remove(d_universo)
                self.salvar_arquivo(tab_d_u)
                return True
        raise UniversoNaoEncontrado(self.caminho)

def nome_universo_valido():
    while True:
        n_v_nome = str(input('Nome: '))
        if n_v_nome:
            return n_v_nome
        else:
            print('ERRO! Digite um nome para o universo!')

def salvar_universo() ->None:
    su_nome = nome_universo_valido()
    su_resumo = str(input('Resumo: '))
    su_salva = Universo()
    su_salva.criar(su_nome, su_resumo)

def ler_universo() ->None:
    lu_nome = nome_universo_valido()
    lu_uni = Universo()
    lu_uni.ler(lu_nome)
    print(f'Nome: {lu_uni.nome}')
    print(f'Resumo: {lu_uni.resumo}')
    print(f'Criado: {lu_uni.criado}')
    print(f'Alterado: {lu_uni.alterado}')

def atualizar_universo() -> None:
    print('Velho Universo ', end='')
    vu_nome = nome_universo_valido()
    au_universo = Universo()
    au_universo.ler(vu_nome)
    print('Novo Universo ', end='')
    au_nome = nome_universo_valido()
    au_resumo = str(input('Resumo: '))
    au_universo.atualizar(au_nome, au_resumo)

def deletar_universo() ->None:
    du_nome = nome_universo_valido()
    du_universo = Universo()
    du_universo.ler(du_nome)
    du_universo.deletar()
