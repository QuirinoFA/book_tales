from use_cases import salvar_texto, ler_texto, atualizar_texto, deletar_texto
from use_cases import salvar_universo, ler_universo, atualizar_universo, deletar_universo
from erros import (TextoTituloEmBranco, TextoTituloGrande, TextoTextoEmBranco,  TextoJaExiste,
                   TextoNaoEncontrado, UniversoNomeEmBranco, UniversoNomeGrande,
                   UniversoResumoEmBranco, UniversoNaoEncontrado, UniversoJaExiste)
import logging
from database import Base, engine
from sqlalchemy.orm import sessionmaker
from texts import RepositorioTexto
from universes import RepositorioUniverso

Base.metadata.create_all(engine)

def dicionario_texto(uni_id) -> dict:
    dict_texto = {
        'titulo': str(input('Digite o título do texto: ')).strip(),
        'texto': str(input('Digite seu texto: ')).strip(),
        'uni_id': uni_id
    }
    return dict_texto

def dicionario_universo() -> dict:
    dict_uni = {
        'nome': str(input('Digite o nome do universo: ')).strip(),
        'resumo': str(input('Digite o resumo do universo: ')).strip()
    }
    return dict_uni

def menu_texto(repositorio:RepositorioTexto, uni_id:int) ->None:
    logging.info(f'Acesso ao Menu de Texto.')
    while True:
        try:
            x = input('Deseja salvar um texto ou ler um texto? [S salvar | L ler | A Atualizar '
                      '| D Deletar | N parar]: ').strip().upper()
            if x == 'S':
                logging.info('Acesso para salvar textos.')
                dict_texto = dicionario_texto(uni_id)
                novo_texto = salvar_texto(repositorio, dict_texto)
                print(f'Texto {novo_texto.titulo} salvo com sucesso!')
                logging.info(f'Texto {novo_texto.titulo} salvo com sucesso.')
            elif x == 'L':
                logging.info('Acesso para ler textos.')
                titulo_texto = str(input('Digite o título do texto que deseja ler: ')).strip()
                lido_texto = ler_texto(repositorio, titulo_texto)
                if lido_texto:
                    print(f'Título: {lido_texto.titulo}')
                    print(f'Texto: {lido_texto.texto}')
                    logging.info(f'Texto {lido_texto.titulo} lido e apresentado com sucesso.')
                else:
                    print(f'Erro: Texto {titulo_texto} não encontrado.')
                    logging.warning(f'Texto {titulo_texto} não encontrado.')
            elif x == 'A':
                logging.info('Acesso para atualizar textos.')
                vel_texto = str(input('Digite o titulo do texto que deseja atualizar: ')).strip()
                dict_texto = dicionario_texto(uni_id)
                atua_texto = atualizar_texto(repositorio, vel_texto, dict_texto)
                print(f'Texto {atua_texto.titulo} atualizado com sucesso!')
                logging.info(f'Texto {atua_texto.titulo} atualizado com sucesso.')
            elif x == 'D':
                logging.info('Acesso para deletar textos.')
                del_texto = str(input('Digite o titulo do texto que deseja deletar: ')).strip()
                deletar_texto(repositorio, del_texto)
                print(f'Texto {del_texto} deletado com sucesso!')
                logging.info(f'Texto {del_texto} deletado com sucesso.')
            elif x == 'N':
                logging.info('Saida do Menu de Texto.')
                break
            else:
                logging.warning(f'Informação {x} recebida inválida.')
        except TextoTituloEmBranco as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de texto: {e}')
        except TextoTituloGrande as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de texto: {e}')
        except TextoTextoEmBranco as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de texto: {e}')
        except TextoJaExiste as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de texto: {e}')
        except TextoNaoEncontrado as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de texto: {e}')

def menu_universo(repositorio:RepositorioUniverso) ->None:
    logging.info(f'Acesso ao Menu de Universo.')
    while True:
        try:
            x = input('Deseja salvar ou ler um universo [S salvar | L ler | A atualizar '
                      '| D deletar | N parar]? ').strip().upper()
            if x == 'S':
                logging.info('Acesso para salvar universos.')
                dict_uni = dicionario_universo()
                novo_uni = salvar_universo(repositorio, dict_uni)
                print(f'Universo salvo com sucesso.')
                logging.info(f'Universo {novo_uni.nome} salvo com sucesso.')
            elif x == 'L':
                logging.info('Acesso para ler universos.')
                nome_uni = str(input('Digite o nome do universo que deseja ler: ')).strip()
                ler_uni = ler_universo(repositorio, nome_uni)
                if ler_uni:
                    print(f'Nome: {ler_uni.nome}')
                    print(f'Resumo: {ler_uni.resumo}')
                    logging.info(f'Universo {ler_uni.nome} lido e apresentado com sucesso.')
                else:
                    print(f'Erro: Universo {nome_uni} não encontrado.')
                    logging.warning(f'Erro de universo: Universo {nome_uni} não encontrado.')
            elif x == 'A':
                logging.info('Acesso para alterar universos.')
                vel_uni = str(input('Digite o nome do universo que deseja alterar: '))
                dict_uni = dicionario_universo()
                atua_uni = atualizar_universo(repositorio, vel_uni, dict_uni)
                print(f' Universo {atua_uni.nome} atualizado com sucesso.')
                logging.info(f'Universo {atua_uni.nome} atualizado com sucesso.')
            elif x == 'D':
                logging.info('Acesso para deletar universos.')
                del_uni = str(input('Digite o nome do universo que deseja deletar: ')).strip()
                deletar_universo(repositorio, del_uni)
                print(f'Universo {del_uni} deletado com sucesso.')
                logging.info(f'Universo {del_uni} deletado com sucesso.')
            elif x.upper() == 'N':
                logging.info(f'Saída do Menu de Universo.')
                break
            else:
                logging.warning(f'Informação {x} recebida inválida.')
        except UniversoNomeEmBranco as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de universo: {e}')
        except UniversoNomeGrande as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de universo: {e}')
        except UniversoResumoEmBranco as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de universo: {e}')
        except UniversoJaExiste as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de universo: {e}')
        except UniversoNaoEncontrado as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de universo: {e}')

def main ():
    format_logs = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format = format_logs,
                        filename = 'logs.log',
                        filemode='a')
    logging.info('Programa iniciado com sucesso.')

    while True:
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            y = input('Deseja ver Universos ou Textos [U | T | N]? ')
            if y.upper() =='T':
                logging.info('Acessando menu de textos.')
                repositorio_universo = RepositorioUniverso(session)
                nome_uni = str(input('Digite o nome do universo que o texto pertence: ')).strip()
                logging.info(f'Validando universo {nome_uni} dos textos.')
                id_uni = repositorio_universo.id_universo(nome_uni)
                if id_uni is not None:
                    logging.info(f'Universo {nome_uni} com id {id_uni} encontrado com sucesso.')
                    repositorio_texto = RepositorioTexto(session)
                    menu_texto(repositorio_texto, id_uni)
                else:
                    logging.warning(f'Universo {nome_uni} não encontrado.')
                    raise UniversoNaoEncontrado
            elif y.upper() == 'U':
                logging.info('Acessando menu de universos.')
                repositorio_universo = RepositorioUniverso(session)
                menu_universo(repositorio_universo)
            elif y.upper() == 'N':
                logging.info('Programa encerrado.')
                break
            else:
                logging.warning(f'Informação inesperada: {y}.')
        except UniversoNomeEmBranco as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de universo: {e}')
        except UniversoNomeGrande as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de universo: {e}')
        except UniversoNaoEncontrado as e:
            print(f'Erro: {e}')
            logging.warning(f'Erro de universo: {e}')
        finally:
            if session is not None:
                session.close()

if __name__ == "__main__":
    main()
