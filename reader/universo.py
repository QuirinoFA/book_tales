import os
import datetime
from .repositorio import RepositorioUniverso
from .erros import UniversoJaExiste


caminho = os.path.join(*["C:\\", "Users", "felip", "OneDrive", "Documentos", "Tabela_Relacional.json"])

class Universo:
    def __init__(self):
        self.nome = None
        self.resumo = None
        self.criado = None
        self.alterado = None
        self.repositorio = RepositorioUniverso(caminho)

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
