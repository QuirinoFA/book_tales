import os
import datetime
import logging
from .repositorio import RepositorioUniverso
from .erros import UniversoJaExiste


logger = logging.getLogger(__name__)

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
        logger.info(f'Universo {self.nome} comprimido para dicionário.')
        return dic_universo

    def criar(self, c_nome:str, c_resumo:str) ->None:
        logger.info(f'Tentando criar o Universo {c_nome}.')
        if self.repositorio.existe_universo(c_nome):
            logger.warning(f'Erro ao criar Universo {c_nome}. Universo já existe.')
            raise UniversoJaExiste(caminho)
        else:
            self.nome = c_nome
            self.resumo = c_resumo
            self.criado = str(datetime.datetime.now())
            self.alterado = None
            novo_universo = self.para_dict()
            self.repositorio.salvar_universo(novo_universo)

    def ler(self, l_nome:str) ->None:
        logger.info(f'Tentando ler o Universo {l_nome}.')
        l_universo = self.repositorio.ler_universo(l_nome)
        self.nome = l_universo['Nome']
        self.resumo = l_universo['Resumo']
        self.criado = l_universo['Criado']
        self.alterado = l_universo['Alterado']

    def atualizar(self, a_nome:str, a_resumo:str) ->None:
        logger.info(f'Tentando atualizar o Universo {a_nome}.')
        v_universo = self.repositorio.ler_universo(self.nome)
        v_nome = self.nome
        self.nome = a_nome
        self.resumo = a_resumo
        self.criado = v_universo['Criado']
        self.alterado = str(datetime.datetime.now())
        a_universo = self.para_dict()
        self.repositorio.atualizar_universo(v_nome, a_universo)

    def deletar(self) ->None:
        logger.info(f'Tentando deletar o Universo {self.nome}.')
        self.repositorio.deletar_universo(self.nome)
        self.nome = None
        self.resumo = None
        self.criado = None
        self.alterado = None
