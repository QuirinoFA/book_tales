import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from universes import RepositorioUniverso, Universo
from texts import Texto
from erros import UniversoNaoEncontrado


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
def test_repositorio(test_session) -> RepositorioUniverso:
    repositorio = RepositorioUniverso(test_session)
    novo_uni = Universo(
        nome='Universo 1',
        resumo='Primeiro universo criado'
    )
    repositorio.session.add(novo_uni)
    repositorio.session.commit()
    return repositorio

def test_existe_universo(test_repositorio):
    existe = 'Universo 1'
    resposta = test_repositorio.existe_universo(existe)
    assert resposta == True

def test_nao_existe_universo(test_repositorio):
    existe = 'Universo 2'
    resposta = test_repositorio.existe_universo(existe)
    assert resposta == False

def test_salvar_universo(test_repositorio):
    uni_envio= Universo(
        nome='Universo 2',
        resumo='Segundo universo criado.'
    )
    novo_uni = test_repositorio.salvar_universo(uni_envio)
    uni_db = (test_repositorio.session.query(Universo)
              .filter(Universo.nome == uni_envio.nome).first())
    assert uni_db.id is not None and uni_db.id == novo_uni.id
    assert uni_db.nome  == novo_uni.nome
    assert uni_db.resumo == novo_uni.resumo
    assert uni_db.criado is not None and uni_db.criado == novo_uni.criado

def test_lido_universo(test_repositorio):
    ler_nome = 'Universo 1'
    ler_uni = test_repositorio.ler_universo(ler_nome)
    uni_db = (test_repositorio.session.query(Universo)
              .filter(Universo.nome == ler_uni.nome).first())
    assert ler_uni.id is not None and ler_uni.id == uni_db.id
    assert ler_uni.nome == uni_db.nome
    assert ler_uni.resumo == uni_db.resumo
    assert ler_uni.criado is not None and ler_uni.criado == uni_db.criado
    assert ler_uni.alterado == uni_db.alterado

def test_nao_lido_universo(test_repositorio):
    ler_nome = 'Universo 2'
    ler_uni = test_repositorio.ler_universo(ler_nome)
    assert ler_uni is None

def test_atualizado_universo(test_repositorio):
    vel_nome = 'Universo 1'
    dict_uni ={
        'nome': 'Universo 2',
        'resumo': 'Antigo Universo 1 e novo Universo 2'
    }
    atua_uni = test_repositorio.atualizar_universo(vel_nome, dict_uni)
    uni_db = (test_repositorio.session.query(Universo)
              .filter(Universo.nome == dict_uni['nome']).first())
    assert atua_uni.nome is not None and atua_uni.nome == uni_db.nome
    assert atua_uni.resumo is not None and atua_uni.resumo == uni_db.resumo
    assert atua_uni.criado is not None and atua_uni.criado == uni_db.criado
    assert atua_uni.alterado is not None and atua_uni.alterado == uni_db.alterado

def test_nao_atualizado_universo(test_repositorio):
    vel_nome = 'Universo 2'
    dict_uni = {
        'nome': 'Universo 1',
        'resumo': 'Universo 2 voltando a ser Universo 1.'
    }
    with pytest.raises(UniversoNaoEncontrado):
        test_repositorio.atualizar_universo(vel_nome, dict_uni)

def test_deletado_universo(test_repositorio):
    del_nome = 'Universo 1'
    test_repositorio.deletar_universo(del_nome)
    assert (test_repositorio.session.query(Universo).
            filter(Universo.nome == del_nome).first() is None)
def test_nao_deletado_universo(test_repositorio):
    del_nome = 'Universo 2'
    with pytest.raises(UniversoNaoEncontrado):
        test_repositorio.deletar_universo(del_nome)

def test_id_universo(test_repositorio):
    nome_uni = 'Universo 1'
    id_uni = test_repositorio.id_universo(nome_uni)
    uni_db = (test_repositorio.session.query(Universo)
              .filter(Universo.nome == nome_uni).first())
    assert id_uni is not None and id_uni == uni_db.id

def test_nao_id_universo(test_repositorio):
    nome_uni = 'Universo 2'
    with pytest.raises(UniversoNaoEncontrado):
        test_repositorio.id_universo(nome_uni)
