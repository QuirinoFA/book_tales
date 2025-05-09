from reader import salvar_texto
from reader import ler_texto


def main ():
    while True:
        x = input('Deseja salvar um texto ou ler um texto? [S salva|L lê|N para]:  ')
        if x.upper() == 'S':
            salvar_texto()
        elif x.upper() == 'L':
            ler_texto()
        elif x.upper() == 'N':
            break


if __name__ == "__main__":
    main()
