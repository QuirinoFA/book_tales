import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from texts import RepositorioTexto, Texto
from universes import Universo, RepositorioUniverso
from erros import TextoNaoEncontrado

@pytest.fixture(scope='function')
def test_engine():
    engine_teste = create_engine('mysql+pymysql://app_book_tales:1234@localhost/book_tales_test_db')
    return engine_teste

@pytest.fixture(scope='function')
def test_session(test_engine):
    Base.metadata.create_all(test_engine)
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(test_engine)

@pytest.fixture(scope='function')
def test_repositorio_universo(test_session):
    repositorio_universo = RepositorioUniverso(test_session)
    novo_universo = Universo(
        nome='Universo 1',
        resumo='Primeiro universo criado.'
    )
    repositorio_universo.session.add(novo_universo)
    repositorio_universo.session.commit()
    return repositorio_universo

@pytest.fixture(scope='function')
def test_repositorio(test_session, test_repositorio_universo):
    repositorio_test = RepositorioTexto(test_session)
    novo_texto = Texto(
        titulo='Texto 1',
        texto='Esse é o primeiro texto.',
        uni_id=1
    )
    repositorio_test.session.add(novo_texto)
    repositorio_test.session.commit()
    return repositorio_test

def test_existe_texto(test_repositorio):
    titulo_texto = 'Texto 1'
    exi_texto = test_repositorio.existe_texto(titulo_texto)
    assert exi_texto is True

def test_nao_existe_texto(test_repositorio):
    titulo_texto = 'Texto 2'
    exi_texto = test_repositorio.existe_texto(titulo_texto)
    assert exi_texto is False

def test_salvar_texto(test_repositorio):
    texto_envio = Texto(
        titulo='Texto 2',
        texto='Esse é o segundo texto.',
        uni_id=1
    )
    novo_texto = test_repositorio.salvar_texto(texto_envio)
    texto_db = (test_repositorio.session.query(Texto)
                .filter(Texto.titulo == texto_envio.titulo).first())
    assert novo_texto.id is not None and novo_texto.id == texto_db.id
    assert novo_texto.titulo == texto_db.titulo
    assert novo_texto.texto == texto_db.texto
    assert novo_texto.uni_id == texto_db.uni_id
    assert novo_texto.criado is not None and novo_texto.criado == texto_db.criado

def test_lido_texto(test_repositorio):
    texto_titulo = 'Texto 1'
    ler_texto = test_repositorio.ler_texto(texto_titulo)
    texto_db = (test_repositorio.session.query(Texto)
                .filter(Texto.titulo == texto_titulo).first())
    assert ler_texto.id is not None and ler_texto.id == texto_db.id
    assert ler_texto.titulo == texto_db.titulo
    assert ler_texto.texto == texto_db.texto
    assert ler_texto.uni_id == texto_db.uni_id
    assert ler_texto.criado is not None and ler_texto.criado == texto_db.criado
    assert ler_texto.alterado == texto_db.alterado

def test_nao_lido_texto(test_repositorio):
    texto_titulo = 'Texto 2'
    ler_texto = test_repositorio.ler_texto(texto_titulo)
    assert ler_texto is None

def test_alterado_texto(test_repositorio):
    vel_texto = 'Texto 1'
    dict_texto = {
        'titulo': 'Texto 2',
        'texto': 'Antigo Texto 1 e novo Texto 2.',
        'uni_id': 1
    }
    alt_texto = test_repositorio.atualizar_texto(vel_texto, dict_texto)
    texto_db = (test_repositorio.session.query(Texto)
                .filter(Texto.titulo == dict_texto['titulo']).first())
    assert alt_texto.id is not None and alt_texto.id == texto_db.id
    assert alt_texto.titulo == texto_db.titulo
    assert alt_texto.texto == texto_db.texto
    assert alt_texto.uni_id == texto_db.uni_id
    assert alt_texto.criado is not None and alt_texto.criado == texto_db.criado
    assert alt_texto.alterado is not None and alt_texto.alterado == texto_db.alterado

def test_nao_alterado_texto(test_repositorio):
    vel_texto = 'Texto 2'
    dict_texto = {
        'titulo': 'Texto 1',
        'texto': 'Texto 2 voltando a ser Texto 1.',
        'uni_id': 1
    }
    with pytest.raises(TextoNaoEncontrado):
        test_repositorio.atualizar_texto(vel_texto, dict_texto)

def test_deletado_texto(test_repositorio):
    titulo_texto = 'Texto 1'
    test_repositorio.deletar_texto(titulo_texto)
    assert (test_repositorio.session.query(Texto)
            .filter(Texto.titulo == titulo_texto).first() is None)

def test_nao_deletado_texto(test_repositorio):
    titulo_texto = 'Texto 2'
    with pytest.raises(TextoNaoEncontrado):
        test_repositorio.deletar_texto(titulo_texto)
