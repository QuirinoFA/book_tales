from reader import salvar_texto
from reader import ler_texto
from reader import salvar_universo
from reader import ler_universo
from reader import atualizar_universo
from reader import deletar_universo
from reader import ArquivoCorrompido
from reader import ArquivoNaoEncontrado
from reader import UniversoNaoEncontrado
from reader import UniversoJaExiste


def menu_texto() ->None:
    while True:
        x = input('Deseja salvar um texto ou ler um texto? [S salvar | L ler | N parar]: ').strip().upper()
        if x == 'S':
            salvar_texto()
        elif x == 'L':
            ler_texto()
        elif x == 'N':
            break

def menu_universo() ->None:
    while True:
        x = input('Deseja salvar ou ler um universo [S salvar | L ler | A atualizar | D deletar | N parar]? ').strip().upper()
        try:
            if x == 'S':
                salvar_universo()
            elif x == 'L':
                ler_universo()
            elif x == 'A':
                atualizar_universo()
            elif x == 'D':
                deletar_universo()
            elif x.upper() == 'N':
                break
        except ArquivoCorrompido as e:
            print(e)
        except ArquivoNaoEncontrado as e:
            print(e)
        except UniversoNaoEncontrado as e:
            print(e)
        except UniversoJaExiste as e:
            print(e)

def main ():
    while True:
        y = input('Deseja ver Universos ou Textos [U | T | N]? ')
        if y.upper() =='T':
            menu_texto()
        elif y.upper() == 'U':
            menu_universo()
        elif y.upper() == 'N':
            break


if __name__ == "__main__":
    main()
