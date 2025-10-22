import logging
from universes import RepositorioUniverso, Universo
from erros import UniversoNomeEmBranco, UniversoNomeGrande, UniversoJaExiste, UniversoResumoEmBranco

logger = logging.getLogger(__name__)

def nome_valido(nome_uni:str) -> None:
    if not nome_uni:
        logger.warning(f'Nome em branco. Universo inválido.')
        raise UniversoNomeEmBranco()
    elif len(nome_uni) > 255:
        logger.warning(f'Nome {nome_uni} acima dos caracteres permitidos. Universo inválido.')
        raise UniversoNomeGrande()
    return None

def dicionario_valido_universo(dict_uni:dict) -> None:
    nome_valido(dict_uni.get('nome'))
    if not dict_uni.get('resumo'):
        logger.warning(f'Universo {dict_uni.get('nome')} com resumo em branco. Universo inválido.')
        raise UniversoResumoEmBranco()
    return None

def universo_valido(repositorio:RepositorioUniverso, nome_universo:Universo) -> None:
    if repositorio.existe_universo(nome_universo.nome):
        logger.warning(f'Nome de universo {nome_universo} já existe.')
        raise UniversoJaExiste()
    return None

def salvar_universo(repositorio:RepositorioUniverso, dict_uni:dict) -> Universo:
    logger.info('Iniciando validação de salvamento de novo universo.')
    dicionario_valido_universo(dict_uni)
    novo_uni = Universo()
    for k, v in dict_uni.items():
        setattr(novo_uni, k, v)
    universo_valido(repositorio, novo_uni)
    novo_uni = repositorio.salvar_universo(novo_uni)
    return novo_uni

def ler_universo(repositorio:RepositorioUniverso, nome_uni:str) -> Universo | None:
    logger.info('Iniciando validação de leitura de universo.')
    nome_valido(nome_uni)
    ler_uni = repositorio.ler_universo(nome_uni)
    return ler_uni

def atualizar_universo(repositorio:RepositorioUniverso, vel_uni:str, atua_dict:dict) -> Universo:
    logger.info('Inicializando a validação da atualização de universo.')
    nome_valido(vel_uni)
    dicionario_valido_universo(atua_dict)
    if vel_uni != atua_dict['nome']:
        exi_uni = Universo()
        for k, v in atua_dict.items():
            setattr(exi_uni, k, v)
        universo_valido(repositorio, exi_uni)
        atua_uni = repositorio.atualizar_universo(vel_uni, atua_dict)
        return atua_uni
    else:
        atua_uni = repositorio.atualizar_universo(vel_uni, atua_dict)
        return atua_uni

def deletar_universo(repositorio:RepositorioUniverso, del_uni:str) -> None:
    logger.info('Inicializando a validação de deletar universo.')
    nome_valido(del_uni)
    repositorio.deletar_universo(del_uni)
    return None

def id_universo(repositorio:RepositorioUniverso, nome_uni:str) -> int:
    logger.info('Iniciando a validação de id universo.')
    nome_valido(nome_uni)
    id_uni = repositorio.id_universo(nome_uni)
    return id_uni
