import json
import os
import datetime

class Texto:
    def __init__(self, titulo, autor=None, texto=None):
        self.titulo = titulo
        self.autor = autor
        self.texto = texto
        self.date = str(datetime.datetime.now())
        self.caminho = os.path.join(*["C:\\", "Users", "felip", "OneDrive", "Documentos", titulo+".json"])

    def salvar(self) ->None:
        novo = {
            'titulo': self.titulo,
            'autor': self.autor,
            'texto': self.texto,
            'data': self.date
        }
        with open(self.caminho, mode='w', encoding='utf-8') as s:
            json.dump(novo, s, ensure_ascii=False, allow_nan=False, indent=4)

    def ler(self) ->None:
        with open(self.caminho, mode='r', encoding='utf-8') as l:
            arq = json.load(l)
            print(f"Título: {arq['titulo'].capitalize()}")
            print(f"Autor: {arq['autor'].capitalize()}")
            print(f"Criado em: {arq['data']}")
            print('')
            print(f"{arq['texto']}")

def salvar_texto() ->None:
    while True:
        s_titulo = str(input('Título: '))
        if s_titulo:
            break
        else:
            print('ERRO! Texto precisa ter um título!')
    teste = Texto(s_titulo)
    if os.path.exists(teste.caminho):
        alerta = str(input('Arquivo já existe! Deseja continuar [S/N]? '))
        if alerta.upper().strip() != 'S':
            print('Operação cancelada!')
            return
    while True:
        s_autor = str(input('Autor: '))
        if s_autor:
            break
        else:
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
    salva.salvar()

def ler_texto() ->None:
    while True:
        l_titulo = str(input('Título: '))
        if l_titulo:
            break
        else:
            print('ERRO! Digite um título!')
    le = Texto(l_titulo)
    try:
        le.ler()
    except FileNotFoundError:
        print(f'Nenhum arquivo com nome {l_titulo} encontrado!')
