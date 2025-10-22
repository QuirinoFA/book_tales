import pytest
from sqlalchemy.orm import Session
from universes import RepositorioUniverso, Universo
from texts import Texto
from unittest.mock import Mock
from erros import UniversoNaoEncontrado


@pytest.fixture(scope='function')
def universo_um() -> Universo:
    universo = Universo(
        id=1,
        nome='Universo 1',
        resumo='Primeiro universo criado.',
        criado='01/01/2000',
        alterado='01/01/2000'
    )
    return universo

@pytest.fixture(scope='function')
def universo_dois() -> dict:
    universo = {
        'nome':'Universo 2',
        'resumo':'Segundo universo criado.'
    }
    return universo

def test_existe_universo(universo_um):
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = universo_um
    repositorio = RepositorioUniverso(mock_session)
    resposta = repositorio.existe_universo('Universo 1')
    assert resposta == True
    mock_session.query.assert_called_once_with(Universo)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_nao_existe_universo():
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = None
    repositorio = RepositorioUniverso(mock_session)
    resposta = repositorio.existe_universo('Universo 1')
    assert resposta == False
    mock_session.query.assert_called_once_with(Universo)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_salvar_universo(universo_um):
    salvar_uni = universo_um
    mock_session = Mock(spec=Session)
    mock_session.add.return_value = True
    mock_session.commit.return_value = True
    repositorio = RepositorioUniverso(mock_session)
    new_uni = repositorio.salvar_universo(salvar_uni)
    assert new_uni.id == salvar_uni.id
    assert new_uni.nome == salvar_uni.nome
    assert new_uni.resumo == salvar_uni.resumo
    assert new_uni.criado == salvar_uni.criado
    assert new_uni.alterado == salvar_uni.alterado
    mock_session.add.assert_called_once_with(salvar_uni)
    mock_session.commit.assert_called_once()

def test_ler_univero(universo_um):
    ler_uni = universo_um
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = ler_uni
    repositorio = RepositorioUniverso(mock_session)
    resposta = repositorio.ler_universo('Universo 1')
    assert resposta.id == ler_uni.id
    assert resposta.nome == ler_uni.nome
    assert resposta.resumo == ler_uni.resumo
    assert resposta.criado == ler_uni.criado
    assert resposta.alterado == ler_uni.alterado
    mock_session.query.assert_called_once_with(Universo)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_nao_ler_universo():
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = None
    repositorio = RepositorioUniverso(mock_session)
    ler_uni = repositorio.ler_universo('Universo 1')
    assert ler_uni is None
    mock_session.query.assert_called_once_with(Universo)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_atualizar_universo(universo_um, universo_dois):
    vel_uni = 'Universo 1'
    dict_uni = universo_dois
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = universo_um
    mock_session.commit.return_value = True
    repositorio = RepositorioUniverso(mock_session)
    atua_uni = repositorio.atualizar_universo(vel_uni, dict_uni)
    assert atua_uni.id == universo_um.id
    assert atua_uni.nome == dict_uni['nome']
    assert atua_uni.resumo == dict_uni['resumo']
    assert atua_uni.criado == universo_um.criado
    assert atua_uni.alterado == universo_um.alterado
    mock_session.query.assert_called_once_with(Universo)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()
    mock_session.commit.assert_called_once()

def test_nao_atualizar_universo(universo_um, universo_dois):
    vel_uni = 'Universo 1'
    dict_uni = universo_dois
    mock_session = Mock(spect=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = None
    repositorio = RepositorioUniverso(mock_session)
    with pytest.raises(UniversoNaoEncontrado):
        repositorio.atualizar_universo(vel_uni, dict_uni)
    mock_session.query.assert_called_once_with(Universo)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_deletar_universo(universo_um):
    del_uni = 'Universo 1'
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = universo_um
    mock_session.delete.return_value = True
    mock_session.commit.return_value = True
    repositorio = RepositorioUniverso(mock_session)
    assert repositorio.deletar_universo(del_uni) is None
    mock_session.query.assert_called_once_with(Universo)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()
    mock_session.delete.assert_called_once_with(universo_um)
    mock_session.commit.assert_called_once()

def test_nao_deletar_universo():
    del_uni = 'Universo 1'
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = None
    repositorio = RepositorioUniverso(mock_session)
    with pytest.raises(UniversoNaoEncontrado):
        repositorio.deletar_universo(del_uni)
    mock_session.query.assert_called_once_with(Universo)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_id_universo():
    nome_uni = 'Universo 1'
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = (1,)
    repositorio = RepositorioUniverso(mock_session)
    id_uni = repositorio.id_universo(nome_uni)
    assert id_uni == 1
    mock_session.query.assert_called_once_with(Universo.id)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_nao_id_universo():
    nome_uni = 'Universo 1'
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = None
    repositorio = RepositorioUniverso(mock_session)
    with pytest.raises(UniversoNaoEncontrado):
        repositorio.id_universo(nome_uni)
    mock_session.query.assert_called_once_with(Universo.id)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()
