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
import logging



def menu_texto() ->None:
    logging.info(f'Acesso ao Menu de Texto.')
    while True:
        x = input('Deseja salvar um texto ou ler um texto? [S salvar | L ler | N parar]: ').strip().upper()
        if x == 'S':
            salvar_texto()
        elif x == 'L':
            ler_texto()
        elif x == 'N':
            logging.info('Saida do Menu de Texto.')
            break
        else:
            logging.warning(f'Informação {x} recebida inválida.')

def menu_universo() ->None:
    logging.info(f'Acesso ao Menu de Universo.')
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
                logging.info(f'Saída do Menu de Universo.')
                break
            else:
                logging.warning(f'Informação {x} recebida inválida.')
        except ArquivoCorrompido as e:
            print(e)
        except ArquivoNaoEncontrado as e:
            print(e)
        except UniversoNaoEncontrado as e:
            print(e)
        except UniversoJaExiste as e:
            print(e)

def main ():
    format_logs = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format = format_logs,
                        filename = 'logs.log',
                        filemode='a')
    logging.info('Programa iniciado com sucesso.')
    while True:
        y = input('Deseja ver Universos ou Textos [U | T | N]? ')
        if y.upper() =='T':
            menu_texto()
        elif y.upper() == 'U':
            menu_universo()
        elif y.upper() == 'N':
            logging.info('Programa encerrado.')
            break
        else:
            logging.warning(f'Informação inesperada: {y}.')


if __name__ == "__main__":
    main()
