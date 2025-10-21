import logging
from ..texts import RepositorioTexto, Texto
from ..erros import TextoTituloEmBranco, TextoTituloGrande, TextoTextoEmBranco, TextoJaExiste


logger = logging.getLogger(__name__)

def titulo_valido(titulo_texto:str) -> None:
    if not titulo_texto:
        logger.warning('Título em branco. Título inválido.')
        raise TextoTituloEmBranco()
    elif len(titulo_texto) > 255:
        logger.warning(f'Título {titulo_texto} maior do que 255 caracteres. Título Inválido.')
        raise TextoTituloGrande()
    return None

def dicionario_valido(dict_texto:dict) -> None:
    titulo_valido(dict_texto.get('titulo'))
    if not dict_texto.get('texto'):
        logger.warning(f'Texto {dict_texto.get('titulo')} com texto em branco. Texto inválido.')
        raise TextoTextoEmBranco()
    return None

def texto_valido(repositorio:RepositorioTexto, titulo_texto:str) -> None:
    if repositorio.existe_texto(titulo_texto):
        logger.warning(f'Nome do texto {titulo_texto} já existe.')
        raise TextoJaExiste()
    return None

def salvar_texto(repositorio:RepositorioTexto, dict_texto:dict) -> Texto:
    logger.info('Iniciando a validação para o salvamento de texto.')
    dicionario_valido(dict_texto)
    texto_valido(repositorio, dict_texto.get('titulo'))
    novo_texto = Texto()
    for k, v in dict_texto.items():
        setattr(novo_texto, k, v)
    novo_texto = repositorio.salvar_texto(novo_texto)
    return novo_texto

def ler_texto(repositorio:RepositorioTexto, titulo_texto:str) -> Texto | None:
    logger.info('Inciando a validação para a leitura de texto.')
    titulo_valido(titulo_texto)
    lido_texto = repositorio.ler_texto(titulo_texto)
    return lido_texto

def atualizar_texto(repositorio:RepositorioTexto, vel_texto:str, dict_texto:dict) -> Texto:
    logger.info('Iniciando a validação para a atualização do texto.')
    titulo_valido(vel_texto)
    dicionario_valido(dict_texto)
    if dict_texto.get('titulo') == vel_texto:
        atua_texto = repositorio.atualizar_texto(vel_texto, dict_texto)
        return atua_texto
    else:
        texto_valido(repositorio, dict_texto.get('titulo'))
        atua_texto = repositorio.atualizar_texto(vel_texto, dict_texto)
        return atua_texto

def deletar_texto(repositorio:RepositorioTexto, titulo_texto:str) -> None:
    logger.info('Inciando a validação para deletar o texto.')
    titulo_valido(titulo_texto)
    repositorio.deletar_texto(titulo_texto)
    return None
