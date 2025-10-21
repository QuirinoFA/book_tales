from ..erros import UniversoNaoEncontrado
import logging
from ..database import Session
from .modelos import Universo


logger = logging.getLogger(__name__)

class RepositorioUniverso:
    def __init__(self, session: Session):
        self.session = session
        logger.info('Objeto RepositorioUniverso instanciado com sucesso.')

    def existe_universo(self, exi_uni : str) -> bool:
        logger.info(f'Pesquisando universo {exi_uni} no banco de dados.')
        check_uni = self.session.query(Universo).filter(Universo.nome == exi_uni).first()
        if check_uni:
            logger.info(f'Universo {exi_uni} existe.')
            return True
        else:
            logger.warning(f'Universo {exi_uni} não encontrado.')
        return False

    def salvar_universo(self, novo_uni : Universo) -> Universo:
        logger.info(f'Tentando salvar novo universo {novo_uni.nome}.')
        self.session.add(novo_uni)
        self.session.commit()
        logger.info(f'Novo universo {novo_uni.nome} salvo com sucesso.')
        return novo_uni

    def ler_universo(self, ler_uni : str) -> Universo | None:
        logger.info(f'Tentando ler universo {ler_uni} no banco de dados.')
        res_ler_uni = self.session.query(Universo).filter(Universo.nome == ler_uni).first()
        if res_ler_uni:
            logger.info(f'Leitura do universo {ler_uni} retornada com sucesso.')
            return res_ler_uni
        else:
            logger.warning(f'Leitura interrompida. Universo {ler_uni} não encontrado.')
            return None

    def atualizar_universo(self, vel_nome:str, atua_uni:dict) -> Universo:
        logger.info(f'Atualizando universo {vel_nome} no banco de dados.')
        vel_uni = self.session.query(Universo).filter(Universo.nome == vel_nome).first()
        if vel_uni:
            for k, v in atua_uni.items():
                setattr(vel_uni, k, v)
            self.session.commit()
            logger.info(f'Universo {vel_uni.nome} atualizado com sucesso.')
            return vel_uni
        else:
            logger.error(f'Universo {vel_nome} não encontrado. Procedimento cancelado.')
            raise UniversoNaoEncontrado()

    def deletar_universo(self, del_nome:str) -> None:
        logger.info(f'Apagando universo {del_nome} do banco de dados.')
        del_uni = self.session.query(Universo).filter(Universo.nome == del_nome).first()
        if del_uni:
            self.session.delete(del_uni)
            logger.info(f'universo {del_nome} apagado com sucesso.')
            self.session.commit()
            return None
        else:
            logger.error(f'Universo {del_nome} não encontrado. Procedimento cancelado.')
            raise UniversoNaoEncontrado()

    def id_universo(self, nome_uni:str) -> int:
        logger.info(f'Obtendo id do universo {nome_uni} do banco de dados.')
        id_uni = self.session.query(Universo.id).filter(Universo.nome == nome_uni).first()
        if id_uni:
            logger.info(f'ID {id_uni[0]} do universo {nome_uni} retornada com sucesso.')
            return id_uni[0]
        else:
            logger.warning('Universo não encontrado.')
            raise UniversoNaoEncontrado()
