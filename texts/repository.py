import logging
from ..database import Session
from .model import Texto
from ..erros import TextoNaoEncontrado


logger = logging.getLogger(__name__)

class RepositorioTexto:
    def __init__(self, session: Session):
        self.session = session
        logger.info('Objeto RepositorioTexto inicializado com sucesso.')

    def existe_texto(self, titulo_text:str) -> bool:
        logger.info(f'Pesquisando pelo texto {titulo_text} no banco de dados.')
        exi_text = self.session.query(Texto).filter(Texto.titulo == titulo_text).first()
        if exi_text:
            logger.info(f'Texto {titulo_text} existe.')
            return True
        else:
            logger.info(f'Texto {titulo_text} não existe.')
            return False

    def salvar_texto(self, novo_texto:Texto) -> Texto:
        logger.info(f'Tentando salvar texto {novo_texto.titulo}.')
        self.session.add(novo_texto)
        self.session.commit()
        logger.info(f'Novo texto {novo_texto.titulo} salvo com sucesso.')
        return novo_texto

    def ler_texto(self, titulo_texto:str) -> Texto | None:
        ler_texto = self.session.query(Texto).filter(Texto.titulo == titulo_texto).first()
        if ler_texto:
            logger.info(f'Leitura do texto {titulo_texto} retornada com sucesso.')
            return ler_texto
        else:
            logger.warning(f'Leitura interrompida. Texto {titulo_texto} não encontrado.')
            return None

    def atualizar_texto(self, titulo_texto:str, atua_texto:dict) -> Texto:
        logger.info(f'Atualizando texto {titulo_texto} no banco de dados.')
        real_texto = self.session.query(Texto).filter(Texto.titulo == titulo_texto).first()
        if real_texto:
            for k, v in atua_texto.items():
                setattr(real_texto, k, v)
            self.session.commit()
            logger.info(f'Texto {titulo_texto} atualizado com sucesso.')
            return real_texto
        else:
            logger.error(f'Texto {titulo_texto} não encontrado. Procedimento cancelado.')
            raise TextoNaoEncontrado()

    def deletar_texto(self, titulo_texto:str) -> None:
        logger.info(f'Apagando texto {titulo_texto} do banco de dados.')
        del_texto = self.session.query(Texto).filter(Texto.titulo == titulo_texto).first()
        if del_texto:
            self.session.delete(del_texto)
            logger.info(f'Texto {titulo_texto} apagado com sucesso.')
            self.session.commit()
            return None
        else:
            logger.error(f'Texto {titulo_texto} não encontrado. Procedimento cancelado.')
            raise TextoNaoEncontrado()