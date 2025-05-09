import json
import os

class Texto:
    def __init__(self, titulo, autor=None, texto=None):
        self.titulo = titulo
        self.autor = autor
        self.texto = texto
        self.caminho = os.path.join(*['C', 'Users', 'felip', 'OneDrive', 'Documentos'])

    def salvar(self) ->None:
        novo = {
            'titulo': self.titulo,
            'autor': self.autor,
            'texto': self.texto
        }
        with open(os.path.join(self.caminho, self.titulo+'.json'), mode='w', encoding='utf-8') as s:
            json.dump(novo, s, ensure_ascii=False, allow_nan=False, indent=4)

    def ler(self) ->None:
        with open(os.path.join(self.caminho, self.titulo+'.json'), mode='r', encoding='utf-8') as l:
            arq = json.load(l)
            print(f"Título: {arq['titulo'].capitalize()}")
            print(f"Autor: {arq['autor'].capitalize()}")
            print('')
            print(f"{arq['texto']}")

def salvar_texto() ->None:
    s_titulo = str(input('Título: '))
    teste = Texto(s_titulo)
    arquivo = os.path.join(teste.caminho, teste.titulo + '.json')
    if os.path.exists(arquivo):
        alerta = str(input('Arquivo já existe! Deseja continuar [S/N]? '))
        if alerta.upper().strip() != 'S':
            print('Operação cancelada!')
            return
    s_autor = str(input('Autor: '))
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
    l_titulo = str(input('Título: '))
    le = Texto(l_titulo)
    try:
        le.ler()
    except FileNotFoundError:
        print(f'Nenhum arquivo com nome {l_titulo} encontrado!')
