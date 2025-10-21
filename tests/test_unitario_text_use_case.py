import pytest
from ..use_cases import (titulo_valido, dicionario_valido, texto_valido, salvar_texto, ler_texto,
                         atualizar_texto, deletar_texto)
from ..erros import TextoTituloEmBranco, TextoTituloGrande, TextoTextoEmBranco, TextoJaExiste
from unittest.mock import Mock
from ..texts import RepositorioTexto, Texto


@pytest.fixture(scope='function')
def test_dicionario_texto()->dict:
    dict_texto = {
        'id':1,
        'titulo':'Texto 1',
        'texto':'Primeiro texto salvo.',
        'criado':'01/01/2000',
        'alterado':'01/01/2000',
        'uni_id':1
    }
    return dict_texto

@pytest.fixture(scope='function')
def test_texto(test_dicionario_texto)->Texto:
    texto = Texto()
    for k, v in test_dicionario_texto.items():
        setattr(texto, k, v)
    return texto

def test_titulo_em_branco():
    titulo = ''
    with pytest.raises(TextoTituloEmBranco):
        titulo_valido(titulo)

def test_titulo_grande():
    titulo = ('Lorem ipsum dolor sit amet, consectetuer '
              'adipiscing elit. Aenean commodo ligula eget dolor. '
              'Aenean massa. Cum sociis natoque penatibus et '
              'magnis dis parturient montes, nascetur ridiculus mus. '
              'Donec quam felis, ultricies nec, pellentesque eu, '
              'pretium quis,.')
    with pytest.raises(TextoTituloGrande):
        titulo_valido(titulo)

def test_titulo_valido(test_dicionario_texto):
    titulo = test_dicionario_texto['titulo']
    assert titulo_valido(titulo) is None

def test_dicionario_texto_em_branco(test_dicionario_texto):
    dict_texto = test_dicionario_texto
    dict_texto['texto'] = ''
    with pytest.raises(TextoTextoEmBranco):
        dicionario_valido(dict_texto)

def test_dicionario_valido(test_dicionario_texto):
    dict_texto = test_dicionario_texto
    assert dicionario_valido(dict_texto) is None

def test_texto_ja_existe(test_dicionario_texto):
    texto = test_dicionario_texto['titulo']
    mock_repositorio = Mock(spec=RepositorioTexto)
    mock_repositorio.existe_texto.return_value = True
    with pytest.raises(TextoJaExiste):
        texto_valido(mock_repositorio, texto)
    mock_repositorio.existe_texto.assert_called_with(texto)

def test_texto_valido(test_dicionario_texto):
    texto = test_dicionario_texto['titulo']
    mock_repositorio = Mock(spec=RepositorioTexto)
    mock_repositorio.existe_texto.return_value = None
    assert texto_valido(mock_repositorio, texto) is None
    mock_repositorio.existe_texto.assert_called_with(texto)

def test_salvar_texto(test_texto, test_dicionario_texto):
    mock_repositorio = Mock(spec=RepositorioTexto)
    mock_repositorio.salvar_texto.return_value = test_texto
    mock_repositorio.existe_texto.return_value = False
    texto_salvo = salvar_texto(mock_repositorio, test_dicionario_texto)
    assert texto_salvo == test_texto
    salvar_cha = mock_repositorio.salvar_texto.call_args[0][0]
    assert salvar_cha.id == test_dicionario_texto['id']
    assert salvar_cha.titulo == test_dicionario_texto['titulo']
    assert salvar_cha.texto == test_dicionario_texto['texto']
    assert salvar_cha.criado == test_dicionario_texto['criado']
    assert salvar_cha.alterado == test_dicionario_texto['alterado']
    assert salvar_cha.uni_id == test_dicionario_texto['uni_id']
    mock_repositorio.existe_texto.assert_called_once_with(test_dicionario_texto['titulo'])
    mock_repositorio.salvar_texto.assert_called_once()

def test_salvar_titulo_em_branco(test_dicionario_texto):
    dicionario_texto = test_dicionario_texto
    dicionario_texto['texto'] = ''
    mock_repositorio = Mock(spec=RepositorioTexto)
    with pytest.raises(TextoTextoEmBranco):
        salvar_texto(mock_repositorio, dicionario_texto)
    assert mock_repositorio.existe_texto.call_count == 0
    assert mock_repositorio.salvar_texto.call_count == 0

def test_salvar_titulo_grande(test_dicionario_texto):
    dicionario_texto = test_dicionario_texto
    dicionario_texto['titulo'] = 'Lorem ipsum dolor sit amet, consectetuer '\
             'adipiscing elit. Aenean commodo ligula eget dolor. '\
             'Aenean massa. Cum sociis natoque penatibus et '\
             'magnis dis parturient montes, nascetur ridiculus mus. '\
             'Donec quam felis, ultricies nec, pellentesque eu, '\
             'pretium quis,.'
    mock_repositorio = Mock(spec=RepositorioTexto)
    with pytest.raises(TextoTituloGrande):
        salvar_texto(mock_repositorio, dicionario_texto)
    assert mock_repositorio.existe_texto.call_count == 0
    assert mock_repositorio.salvar_texto.call_count == 0

def test_salvar_texto_em_branco(test_dicionario_texto):
    dicionario_texto = test_dicionario_texto
    dicionario_texto['texto'] = ''
    mock_repositorio = Mock(spec=RepositorioTexto)
    with pytest.raises(TextoTextoEmBranco):
        salvar_texto(mock_repositorio, dicionario_texto)
    assert mock_repositorio.existe_texto.call_count == 0
    assert mock_repositorio.salvar_texto.call_count == 0

def test_salvar_titulo_ja_existe(test_dicionario_texto, test_texto):
    dicionario_texto = test_dicionario_texto
    mock_repositorio = Mock(spec=RepositorioTexto)
    mock_repositorio.existe_texto.return_value = test_texto
    with pytest.raises(TextoJaExiste):
        salvar_texto(mock_repositorio, dicionario_texto)
    mock_repositorio.existe_texto.assert_called_once_with(test_dicionario_texto['titulo'])
    assert mock_repositorio.salvar_texto.call_count == 0

def test_ler_texto(test_texto):
    titulo = test_texto.titulo
    mock_repositorio = Mock(spec=RepositorioTexto)
    mock_repositorio.ler_texto.return_value = test_texto
    texto_lido = ler_texto(mock_repositorio, titulo)
    assert texto_lido == test_texto
    ler_cha = mock_repositorio.ler_texto.call_args[0][0]
    assert ler_cha == titulo
    mock_repositorio.ler_texto.assert_called_once()

def test_ler_titulo_em_branco():
    titulo =''
    mock_repositorio = Mock(spec=RepositorioTexto)
    with pytest.raises(TextoTituloEmBranco):
        ler_texto(mock_repositorio, titulo)
    assert mock_repositorio.ler_texto.call_count == 0

def test_ler_titulo_grande():
    titulo = 'Lorem ipsum dolor sit amet, consectetuer '\
             'adipiscing elit. Aenean commodo ligula eget dolor. '\
             'Aenean massa. Cum sociis natoque penatibus et '\
             'magnis dis parturient montes, nascetur ridiculus mus. '\
             'Donec quam felis, ultricies nec, pellentesque eu, '\
             'pretium quis,.'
    mock_repositorio = Mock(spec=RepositorioTexto)
    with pytest.raises(TextoTituloGrande):
        ler_texto(mock_repositorio, titulo)
    assert mock_repositorio.ler_texto.call_count == 0

def test_atualizar_texto(test_texto, test_dicionario_texto):
    titulo = 'Texto 2'
    dict_texto = test_dicionario_texto
    mock_repositorio = Mock(spec=RepositorioTexto)
    mock_repositorio.atualizar_texto.return_value = test_texto
    texto_atua = atualizar_texto(mock_repositorio, titulo, dict_texto)
    assert texto_atua == test_texto
    titulo_cha = mock_repositorio.atualizar_texto.call_args[0][0]
    dict_cha = mock_repositorio.atualizar_texto.call_args[0][1]
    assert titulo_cha == titulo
    assert dict_cha == dict_texto
    mock_repositorio.atualizar_texto.assert_called_once()

def test_atualizar_titulo_em_branco(test_dicionario_texto):
    titulo = ''
    mock_repositorio = Mock(spec=RepositorioTexto)
    with pytest.raises(TextoTituloEmBranco):
        atualizar_texto(mock_repositorio, titulo, test_dicionario_texto)
    assert mock_repositorio.atualizar_texto.call_count == 0

def test_atualizar_titulo_grande(test_dicionario_texto):
    titulo = 'Lorem ipsum dolor sit amet, consectetuer '\
             'adipiscing elit. Aenean commodo ligula eget dolor. '\
             'Aenean massa. Cum sociis natoque penatibus et '\
             'magnis dis parturient montes, nascetur ridiculus mus. '\
             'Donec quam felis, ultricies nec, pellentesque eu, '\
             'pretium quis,.'
    mock_repositorio = Mock(spec=RepositorioTexto)
    with pytest.raises(TextoTituloGrande):
        atualizar_texto(mock_repositorio, titulo, test_dicionario_texto)
    assert mock_repositorio.atualizar_texto.call_count == 0

def test_atualizar_texto_em_branco(test_dicionario_texto, test_texto):
    titulo = test_dicionario_texto['titulo']
    dict_texto = test_dicionario_texto
    dict_texto['texto'] = ''
    mock_repositorio = Mock(spec=RepositorioTexto)
    with pytest.raises(TextoTextoEmBranco):
        atualizar_texto(mock_repositorio, titulo, dict_texto)
    assert mock_repositorio.atualizar_texto.call_count == 0

def test_deletar_texto():
    titulo = 'Texto 1'
    mock_repositorio = Mock(spec=RepositorioTexto)
    mock_repositorio.deletar_texto.return_value = None
    assert deletar_texto(mock_repositorio, titulo) is None
    mock_repositorio.deletar_texto.assert_called_once_with(titulo)

def test_deletar_titulo_em_branco():
    titulo = ''
    mock_repositorio = Mock(spec=RepositorioTexto)
    with pytest.raises(TextoTituloEmBranco):
        deletar_texto(mock_repositorio, titulo)
    assert mock_repositorio.deletar_texto.call_count == 0

def test_deletar_titulo_grande():
    titulo = 'Lorem ipsum dolor sit amet, consectetuer '\
             'adipiscing elit. Aenean commodo ligula eget dolor. '\
             'Aenean massa. Cum sociis natoque penatibus et '\
             'magnis dis parturient montes, nascetur ridiculus mus. '\
             'Donec quam felis, ultricies nec, pellentesque eu, '\
             'pretium quis,.'
    mock_repositorio = Mock(spec=RepositorioTexto)
    with pytest.raises(TextoTituloGrande):
        deletar_texto(mock_repositorio, titulo)
    assert mock_repositorio.deletar_texto.call_count == 0
