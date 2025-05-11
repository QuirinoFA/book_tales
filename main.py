from reader import salvar_texto
from reader import ler_texto
from reader import salvar_universo
from reader import ler_universo


def main ():
    while True:
        y = input('Deseja ver Universos ou Textos [U | T | N]? ')
        if y.upper() =='T':
            while True:
                x = input('Deseja salvar um texto ou ler um texto? [S salvar | L ler | N parar]: ')
                if x.upper() == 'S':
                    salvar_texto()
                elif x.upper() == 'L':
                    ler_texto()
                elif x.upper() == 'N':
                    break
        elif y.upper() == 'U':
            while True:
                x = input('Deseja salvar ou ler um universo [S salvar | L ler | N parar]? ')
                if x.upper() == 'S':
                    salvar_universo()
                elif x.upper() == 'L':
                    ler_universo()
                elif x.upper() == 'N':
                    break
        elif y.upper() == 'N':
            break


if __name__ == "__main__":
    main()
