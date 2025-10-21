import copy
import pytest
from ..database import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from ..texts import Texto, RepositorioTexto
from ..universes import Universo, RepositorioUniverso
from ..use_cases import texto_valido, salvar_texto, ler_texto, atualizar_texto, deletar_texto
from ..erros import TextoJaExiste, TextoNaoEncontrado


@pytest.fixture(scope='function')
def test_engine():
    engine = create_engine('mysql+pymysql://app_book_tales:1234@localhost/book_tales_test_db')
    return engine

@pytest.fixture(scope='function')
def test_session(test_engine):
    Base.metadata.create_all(test_engine)
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(test_engine)

@pytest.fixture(scope='function')
def test_dict_texto()->dict:
    dict_texto = {
        'id':1,
        'titulo': 'Texto 1',
        'texto': 'Primeiro texto salvo.',
        'criado':func.now(),
        'alterado':func.now(),
        'uni_id':1
    }
    return dict_texto

@pytest.fixture(scope='function')
def test_texto(test_dict_texto)->Texto:
    texto = Texto()
    for k, v in test_dict_texto.items():
        setattr(texto, k, v)
    return texto

@pytest.fixture(scope='function')
def test_universo()->Universo:
    universo = Universo(
        id=1,
        nome='Universo 1',
        resumo='Primeiro universo salvo.',
        criado=func.now(),
        alterado=func.now()
    )
    return universo

def test_texto_nao_valido(test_session,test_universo, test_texto):
    test_session.add(test_universo)
    test_session.add(test_texto)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    titulo_texto = test_texto.titulo
    with pytest.raises(TextoJaExiste):
        texto_valido(repositorio, titulo_texto)

def test_texto_valido(test_session,test_universo, test_texto):
    test_session.add(test_universo)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    titulo_texto = test_texto.titulo
    assert texto_valido(repositorio, titulo_texto) is None

def test_salvar_texto_ja_existe(test_session,test_universo, test_dict_texto, test_texto):
    test_session.add(test_universo)
    test_session.add(test_texto)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    dict_texto = test_dict_texto
    with pytest.raises(TextoJaExiste):
        salvar_texto(repositorio, dict_texto)

def test_salvar_texto(test_session,test_universo, test_texto, test_dict_texto):
    test_session.add(test_universo)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    texto_salvar = salvar_texto(repositorio, test_dict_texto)
    assert texto_salvar.id == test_texto.id
    assert texto_salvar.titulo == test_texto.titulo
    assert texto_salvar.criado is not None
    assert texto_salvar.alterado is not None
    assert texto_salvar.uni_id == test_universo.id
    with pytest.raises(TextoJaExiste):
        texto_valido(repositorio, test_dict_texto['titulo'])

def test_ler_texto_nao_encontrado(test_session,test_universo, test_texto):
    test_session.add(test_universo)
    test_session.add(test_texto)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    titulo_texto = 'Texto 2'
    assert ler_texto(repositorio, titulo_texto) is None

def test_ler_texto(test_session, test_universo, test_texto):
    test_session.add(test_universo)
    test_session.add(test_texto)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    titulo_texto = test_texto.titulo
    texto_ler = ler_texto(repositorio, titulo_texto)
    assert texto_ler == test_texto

def test_alterado_texto_nao_encontrado(test_session,test_universo, test_texto, test_dict_texto):
    test_session.add(test_universo)
    dict_texto = test_dict_texto
    dict_texto['titulo'] = 'Texto 2'
    test_session.add(test_texto)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    vel_texto = 'Texto 2'
    with pytest.raises(TextoNaoEncontrado):
        atualizar_texto(repositorio, vel_texto, test_dict_texto)

def test_alterado_novo_titulo_ja_existe(test_session,test_universo, test_dict_texto, test_texto):
    test_session.add(test_universo)
    test_session.add(test_texto)
    texto_dois = copy.deepcopy(test_texto)
    texto_dois.titulo = 'Texto 2'
    texto_dois.id = 2
    test_session.add(texto_dois)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    vel_texto = test_texto.titulo
    dict_texto = test_dict_texto
    dict_texto['titulo'] = 'Texto 2'
    with pytest.raises(TextoJaExiste):
        atualizar_texto(repositorio, vel_texto, dict_texto)

def test_alterar_texto_titulo_diferente(test_session,test_universo, test_texto, test_dict_texto):
    test_session.add(test_universo)
    test_session.add(test_texto)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    vel_texto = 'Texto 1'
    dict_texto = test_dict_texto
    dict_texto['titulo'] = 'Texto 2'
    dict_texto['texto'] = 'Primeiro texto alterado.'
    atua_texto = atualizar_texto(repositorio, vel_texto, dict_texto)
    assert atua_texto.id == dict_texto['id']
    assert atua_texto.titulo == dict_texto['titulo']
    assert atua_texto.texto == dict_texto['texto']
    assert atua_texto.alterado != dict_texto['alterado']
    assert atua_texto.uni_id == dict_texto['uni_id']
    texto_lido = ler_texto(repositorio, dict_texto['titulo'])
    assert texto_lido == atua_texto

def test_alterar_texto_titulo_igual(test_session,test_universo, test_texto, test_dict_texto):
    test_session.add(test_universo)
    test_session.add(test_texto)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    vel_texto = 'Texto 1'
    dict_texto = test_dict_texto
    dict_texto['texto'] = 'Primeiro texto alterado.'
    atua_texto = atualizar_texto(repositorio, vel_texto, dict_texto)
    assert atua_texto.id == dict_texto['id']
    assert atua_texto.titulo == dict_texto['titulo']
    assert atua_texto.texto == dict_texto['texto']
    assert atua_texto.alterado != dict_texto['alterado']
    assert atua_texto.uni_id == dict_texto['uni_id']
    texto_lido = ler_texto(repositorio, dict_texto['titulo'])
    assert texto_lido == atua_texto

def test_deletar_nao_encontrado(test_session,test_universo, test_texto):
    test_session.add(test_universo)
    test_session.add(test_texto)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    titulo_texto = 'Texto 2'
    with pytest.raises(TextoNaoEncontrado):
        deletar_texto(repositorio, titulo_texto)

def test_deletar_texto(test_session,test_universo, test_texto):
    test_session.add(test_universo)
    test_session.add(test_texto)
    test_session.commit()
    repositorio = RepositorioTexto(test_session)
    del_texto = test_texto.titulo
    assert deletar_texto(repositorio, del_texto) is None
    assert texto_valido(repositorio, del_texto) is None
