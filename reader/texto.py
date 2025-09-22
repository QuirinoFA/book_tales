import json
import os
import datetime
import logging


logger = logging.getLogger(__name__)

class Texto:
    def __init__(self, titulo, autor=None, texto=None):
        self.titulo = titulo
        self.autor = autor
        self.texto = texto
        self.date = str(datetime.datetime.now())
        self.caminho = os.path.join(*["C:\\", "Users", "felip", "OneDrive", "Documentos", titulo+".json"])
        logger.info(f'Objeto Texto {self.titulo} foi instanciado.')

    def salvar(self) ->None:
        novo = {
            'titulo': self.titulo,
            'autor': self.autor,
            'texto': self.texto,
            'data': self.date
        }
        with open(self.caminho, mode='w', encoding='utf-8') as s:
            json.dump(novo, s, ensure_ascii=False, allow_nan=False, indent=4)
        logger.info(f'Objeto Texto {self.titulo} foi salvo no arquivo {self.caminho}.')

    def ler(self) ->None:
        with open(self.caminho, mode='r', encoding='utf-8') as l:
            arq = json.load(l)
            print(f"Título: {arq['titulo'].capitalize()}")
            print(f"Autor: {arq['autor'].capitalize()}")
            print(f"Criado em: {arq['data']}")
            print('')
            print(f"{arq['texto']}")
        logger.info(f'Objeto Texto {self.titulo} foi lido pelo caminho {self.caminho} e exibido ao usuário.')

def salvar_texto() ->None:
    logger.info(f'Acesso para salvar Texto.')
    while True:
        s_titulo = str(input('Título: '))
        if s_titulo:
            break
        else:
            logger.warning(f'Título {s_titulo} inválido.')
            print('ERRO! Texto precisa ter um título!')
    teste = Texto(s_titulo)
    if os.path.exists(teste.caminho):
        logger.info(f'Tentativa de sobrescrever Texto existente: {teste.caminho}.')
        alerta = str(input('Arquivo já existe! Deseja continuar [S/N]? '))
        if alerta.upper().strip() != 'S':
            logger.warning(f'Operação de sobrescrever {teste.caminho} cancelada.')
            print('Operação cancelada!')
            return
    while True:
        s_autor = str(input('Autor: '))
        if s_autor:
            break
        else:
            logger.warning(f'Autor {s_autor} inválido.')
            print('ERRO! Texto precisa ter autor!')
    linhas = []
    aux = 0
    while True:
        linha = str(input('Texto: '))
        if linha == '':
            aux += 1
            if aux > 1:
                break
        else:
            aux = 0
        linhas.append(linha)
    s_texto = '\n'.join(linhas)
    salva = Texto(s_titulo, s_autor, s_texto)
    logger.info(f'Salvando Objeto Texto {s_titulo} do autor {s_autor}.')
    salva.salvar()
    logger.info(f'Objeto Texto {s_titulo} do autor {s_autor} salvo com sucesso.')

def ler_texto() ->None:
    logger.info(f'Acesso para ler Texto.')
    while True:
        l_titulo = str(input('Título: '))
        if l_titulo:
            break
        else:
            logger.warning(f'Título {l_titulo} inválido.')
            print('ERRO! Digite um título!')
    le = Texto(l_titulo)
    try:
        le.ler()
    except FileNotFoundError as e:
        logger.error(f'Arquivo não encontrado: {e}.')
        print(f'Nenhum arquivo com nome {l_titulo} encontrado!')
