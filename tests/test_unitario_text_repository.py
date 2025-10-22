import pytest
from sqlalchemy.orm import Session
from unittest.mock import Mock
from texts import Texto, RepositorioTexto
from universes import Universo
from erros import TextoNaoEncontrado


@pytest.fixture(scope='function')
def texto_um() -> Texto:
    texto = Texto(
        id=1,
        titulo='Texto 1',
        texto='Primeiro texto salvo.',
        criado='01/01/2000',
        alterado='01/01/2000',
        uni_id=1
    )
    return texto

@pytest.fixture(scope='function')
def texto_dois() -> dict:
    dict_texto = {
        'titulo': 'Texto 2',
        'texto': 'Segundo texto salvo.'
    }
    return dict_texto

def test_existe_texto(texto_um):
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = texto_um
    repositorio = RepositorioTexto(mock_session)
    existe_texto = repositorio.existe_texto('Texto 1')
    assert existe_texto == True
    mock_session.query.assert_called_with(Texto)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_nao_existe_texto():
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = None
    repositorio = RepositorioTexto(mock_session)
    existe_texto = repositorio.existe_texto('Texto 1')
    assert existe_texto == False
    mock_session.query.assert_called_with(Texto)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_salvar_texto(texto_um):
    salvar_texto = texto_um
    mock_session = Mock(spec=Session)
    mock_session.add.return_value = True
    mock_session.commit.return_value = True
    repositorio = RepositorioTexto(mock_session)
    new_texto = repositorio.salvar_texto(salvar_texto)
    assert new_texto.id == salvar_texto.id
    assert new_texto.titulo == salvar_texto.titulo
    assert new_texto.texto == salvar_texto.texto
    assert new_texto.criado == salvar_texto.criado
    assert new_texto.alterado == salvar_texto.alterado
    assert new_texto.uni_id == salvar_texto.uni_id
    mock_session.add.assert_called_once_with(salvar_texto)
    mock_session.commit.assert_called_once()

def test_ler_texto(texto_um):
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = texto_um
    repositorio = RepositorioTexto(mock_session)
    ler_texto = repositorio.ler_texto('Texto 1')
    assert ler_texto.id == texto_um.id
    assert ler_texto.titulo == texto_um.titulo
    assert ler_texto.texto == texto_um.texto
    assert ler_texto.criado == texto_um.criado
    assert ler_texto.alterado == texto_um.alterado
    assert ler_texto.uni_id == texto_um.uni_id
    mock_session.query.assert_called_once_with(Texto)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_nao_lido_texto():
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = None
    repositorio = RepositorioTexto(mock_session)
    ler_texto = repositorio.ler_texto('Texto 1')
    assert ler_texto is None
    mock_session.query.assert_called_once_with(Texto)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_atualizar_texto(texto_um, texto_dois):
    vel_texto = 'Texto 1'
    dict_texto = texto_dois
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = texto_um
    mock_session.commit.return_value = True
    repositorio = RepositorioTexto(mock_session)
    atua_texto = repositorio.atualizar_texto(vel_texto, dict_texto)
    assert atua_texto.id == texto_um.id
    assert atua_texto.titulo == dict_texto['titulo']
    assert atua_texto.texto == dict_texto['texto']
    assert atua_texto.criado == texto_um.criado
    assert atua_texto.alterado == texto_um.alterado
    assert atua_texto.uni_id == texto_um.uni_id
    mock_session.query.assert_called_once_with(Texto)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()
    mock_session.commit.assert_called_once()

def test_nao_atualizar_texto(texto_dois):
    vel_texto = 'Texto 1'
    dict_texto = texto_dois
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = None
    repositorio = RepositorioTexto(mock_session)
    with pytest.raises(TextoNaoEncontrado):
        repositorio.atualizar_texto(vel_texto, dict_texto)
    mock_session.query.assert_called_once_with(Texto)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()

def test_deletar_texto(texto_um):
    del_titulo = texto_um.titulo
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = texto_um
    mock_session.delete.return_value = True
    mock_session.commit.return_value = True
    repositorio = RepositorioTexto(mock_session)
    assert repositorio.deletar_texto(del_titulo) is None
    mock_session.query.assert_called_once_with(Texto)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()
    mock_session.delete.assert_called_once_with(texto_um)
    mock_session.commit.assert_called_once()

def test_nao_deletar_texto():
    del_texto = 'Texto 1'
    mock_session = Mock(spec=Session)
    mock_session.query.return_value.filter.return_value.first.return_value = None
    repositorio = RepositorioTexto(mock_session)
    with pytest.raises(TextoNaoEncontrado):
        repositorio.deletar_texto(del_texto)
    mock_session.query.assert_called_once_with(Texto)
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.first.assert_called_once()
