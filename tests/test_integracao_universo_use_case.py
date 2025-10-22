import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from database import Base
from universes import Universo, RepositorioUniverso
from texts import Texto
import copy
from use_cases import (universo_valido, salvar_universo, ler_universo,
                         atualizar_universo, deletar_universo, id_universo)
from erros import UniversoJaExiste, UniversoNaoEncontrado


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
def dicionario_universo()->dict:
    universo={
        'id':1,
        'nome':'Universo 1',
        'resumo':'Primeiro universo salvo.',
        'criado':func.now(),
        'alterado':func.now()
    }
    return universo

@pytest.fixture(scope='function')
def universo(dicionario_universo)->Universo:
    universo = Universo()
    for k, v in dicionario_universo.items():
        setattr(universo, k, v)
    return universo

def test_dicionario_universo_ja_existe(test_session, universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    exi_uni = universo
    with pytest.raises(UniversoJaExiste):
        universo_valido(repositorio, exi_uni)

def test_dicionario_valido(test_session, universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    exi_uni = copy.deepcopy(universo)
    exi_uni.nome = 'Universo 2'
    assert universo_valido(repositorio, exi_uni) is None

def test_salvar_universo_ja_existe(test_session, universo, dicionario_universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    exi_uni = copy.deepcopy(dicionario_universo)
    with pytest.raises(UniversoJaExiste):
        salvar_universo(repositorio, exi_uni)

def test_salvar_universo(test_session, universo, dicionario_universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    exi_uni = copy.deepcopy(dicionario_universo)
    exi_uni['id'] = 2
    exi_uni['nome'] = 'Universo 2'
    salvar_uni = salvar_universo(repositorio, exi_uni)
    salvar_cha = test_session.query(Universo).filter(Universo.nome == exi_uni['nome']).first()
    assert salvar_uni == salvar_cha

def test_ler_universo_nao_encontrado(test_session, universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    ler_uni = 'Universo 2'
    assert ler_universo(repositorio, ler_uni) is None

def test_ler_universo(test_session, universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    nome_uni = copy.deepcopy(universo.nome)
    ler_uni = ler_universo(repositorio, nome_uni)
    ler_cha = test_session.query(Universo).filter(Universo.nome == nome_uni).first()
    assert ler_uni == ler_cha

def test_atualizar_universo_nao_encontrado(test_session, dicionario_universo, universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    vel_uni = 'Universo 2'
    dict_uni = copy.deepcopy(dicionario_universo)
    dict_uni['nome'] = 'Universo 2'
    with pytest.raises(UniversoNaoEncontrado):
        atualizar_universo(repositorio, vel_uni, dict_uni)

def test_atualizar_universo_ja_existe(test_session, universo, dicionario_universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    vel_uni = 'Universo 2'
    dict_uni = copy.deepcopy(dicionario_universo)
    with pytest.raises(UniversoJaExiste):
        atualizar_universo(repositorio, vel_uni, dict_uni)

def test_atualizar_universo_nome_diferente(test_session, universo, dicionario_universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    vel_uni = 'Universo 1'
    dict_uni = copy.deepcopy(dicionario_universo)
    dict_uni['nome'] = 'Universo 2'
    dict_uni['resumo'] = 'Primeiro Universo virando segundo.'
    atua_uni = atualizar_universo(repositorio, vel_uni, dict_uni)
    atua_cha = test_session.query(Universo).filter(Universo.nome == dict_uni['nome']).first()
    assert atua_uni == atua_cha

def test_atualizar_universo_nome_igual(test_session, universo, dicionario_universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    vel_uni = 'Universo 1'
    dict_uni = copy.deepcopy(dicionario_universo)
    dict_uni['resumo'] = 'Primeiro universo continua sendo o primeiro.'
    atua_uni = atualizar_universo(repositorio, vel_uni, dict_uni)
    atua_cha = test_session.query(Universo).filter(Universo.nome == dict_uni['nome']).first()
    assert atua_uni == atua_cha

def test_deletar_universo_nao_encontrado(test_session, universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    del_titulo = 'Universo 2'
    with pytest.raises(UniversoNaoEncontrado):
        deletar_universo(repositorio, del_titulo)

def test_deletar_universo(test_session, universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    del_titulo = 'Universo 1'
    assert deletar_universo(repositorio, del_titulo) is None
    assert test_session.query(Universo).filter(Universo.nome == del_titulo).first() is None

def test_universo_id_nao_encontrado(test_session, universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    nome_uni = 'Universo 2'
    with pytest.raises(UniversoNaoEncontrado):
        id_universo(repositorio, nome_uni)

def test_id_universo(test_session, universo):
    test_session.add(universo)
    test_session.commit()
    repositorio = RepositorioUniverso(test_session)
    nome_uni = copy.deepcopy(universo.nome)
    id_uni = id_universo(repositorio, nome_uni)
    id_cha = test_session.query(Universo.id).filter(Universo.nome == nome_uni).first()[0]
    assert id_uni == id_cha
