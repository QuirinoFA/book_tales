import copy

import pytest
from use_cases import (nome_valido, dicionario_valido_universo, universo_valido, salvar_universo,
                         ler_universo, atualizar_universo, deletar_universo, id_universo)
from erros import (UniversoNomeEmBranco, UniversoNomeGrande, UniversoResumoEmBranco,
                     UniversoJaExiste)
from universes import Universo, RepositorioUniverso
from unittest.mock import Mock


@pytest.fixture(scope='function')
def dicionario_universo()->dict:
    universo = {
        'id':1,
        'nome':'Universo 1',
        'resumo':'Primeiro universo salvo.',
        'criado':'01/01/2000',
        'alterado':'01/01/2000'
    }
    return universo

@pytest.fixture(scope='function')
def universo_test(dicionario_universo)->Universo:
    universo = Universo()
    for k, v in dicionario_universo.items():
        setattr(universo, k, v)
    return universo

@pytest.fixture(scope='function')
def nome_grande()->str:
    nome = ('Lorem ipsum dolor sit amet, consectetuer '
              'adipiscing elit. Aenean commodo ligula eget dolor. '
              'Aenean massa. Cum sociis natoque penatibus et '
              'magnis dis parturient montes, nascetur ridiculus mus. '
              'Donec quam felis, ultricies nec, pellentesque eu, '
              'pretium quis,.')
    return nome

def test_nome_valido_em_branco():
    nome = ''
    with pytest.raises(UniversoNomeEmBranco):
        nome_valido(nome)

def test_nome_grande(nome_grande):
    nome = nome_grande
    with pytest.raises(UniversoNomeGrande):
        nome_valido(nome)

def test_nome_valido():
    nome = 'Universo 1'
    assert nome_valido(nome) is None

def test_dicionario_nome_em_branco(dicionario_universo):
    dict_uni = dicionario_universo
    dict_uni['nome'] = ''
    with pytest.raises(UniversoNomeEmBranco):
        dicionario_valido_universo(dict_uni)

def test_dicionario_nome_grande(dicionario_universo, nome_grande):
    dict_uni = dicionario_universo
    dict_uni['nome'] = nome_grande
    with pytest.raises(UniversoNomeGrande):
        dicionario_valido_universo(dict_uni)

def test_dicionario_resumo_em_branco(dicionario_universo):
    dict_uni = dicionario_universo
    dict_uni['resumo'] = ''
    with pytest.raises(UniversoResumoEmBranco):
        dicionario_valido_universo(dict_uni)

def test_resumo_valido(dicionario_universo):
    dict_uni = dicionario_universo
    assert dicionario_valido_universo(dict_uni) is None

def test_universo_nao_valido(universo_test):
    mock_repositorio = Mock(spec=RepositorioUniverso)
    mock_repositorio.existe_universo.return_value = universo_test
    with pytest.raises(UniversoJaExiste):
        universo_valido(mock_repositorio, universo_test)
    mock_repositorio.existe_universo.assert_called_with(universo_test.nome)

def test_universo_valido(universo_test):
    mock_repositorio = Mock(spec=RepositorioUniverso)
    mock_repositorio.existe_universo.return_value = None
    assert universo_valido(mock_repositorio, universo_test) is None
    mock_repositorio.existe_universo.assert_called_with(universo_test.nome)

def test_salvar_nome_em_branco(dicionario_universo):
    dict_uni = dicionario_universo
    dict_uni['nome'] = ''
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeEmBranco):
        salvar_universo(mock_repositorio, dict_uni)
    assert mock_repositorio.existe_universo.call_count == 0
    assert mock_repositorio.salvar_universo.call_count == 0

def test_salvar_nome_grande(dicionario_universo, nome_grande):
    dict_uni = dicionario_universo
    dict_uni['nome'] = nome_grande
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeGrande):
        salvar_universo(mock_repositorio, dict_uni)
    assert mock_repositorio.existe_universo.call_count == 0
    assert mock_repositorio.salvar_universo.call_count == 0

def test_salvar_resumo_em_branco(dicionario_universo):
    dict_uni = dicionario_universo
    dict_uni['resumo'] = ''
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoResumoEmBranco):
        salvar_universo(mock_repositorio, dict_uni)
    assert mock_repositorio.existe_universo.call_count == 0
    assert mock_repositorio.salvar_universo.call_count == 0

def test_salvar_universo_ja_existe(dicionario_universo, universo_test):
    dict_uni = dicionario_universo
    mock_repositorio = Mock(spec=RepositorioUniverso)
    mock_repositorio.existe_universo.return_value = universo_test
    with pytest.raises(UniversoJaExiste):
        salvar_universo(mock_repositorio, dict_uni)
    mock_repositorio.existe_universo.assert_called_with(dict_uni['nome'])
    assert mock_repositorio.salvar_universo.call_count == 0

def test_salvar_universo(dicionario_universo, universo_test):
    dict_uni = dicionario_universo
    mock_repositorio = Mock(spec=RepositorioUniverso)
    mock_repositorio.existe_universo.return_value = None
    mock_repositorio.salvar_universo.return_value = universo_test
    salvar_uni = salvar_universo(mock_repositorio, dict_uni)
    assert salvar_uni == universo_test
    salvar_cha = mock_repositorio.salvar_universo.call_args[0][0]
    assert salvar_cha.id == dict_uni['id']
    assert salvar_cha.nome == dict_uni['nome']
    assert salvar_cha.resumo == dict_uni['resumo']
    assert salvar_cha.criado == dict_uni['criado']
    assert salvar_cha.alterado == dict_uni['alterado']
    mock_repositorio.existe_universo.assert_called_with(dict_uni['nome'])

def test_ler_nome_em_branco():
    nome_uni = ''
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeEmBranco):
        ler_universo(mock_repositorio, nome_uni)
    assert mock_repositorio.ler_universo.call_count == 0

def test_ler_nome_grande(nome_grande):
    nome_uni = nome_grande
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeGrande):
        ler_universo(mock_repositorio, nome_uni)
    assert mock_repositorio.ler_universo.call_count == 0

def test_ler_universo(universo_test):
    nome_uni = 'Universo 1'
    mock_repositorio = Mock(spec=RepositorioUniverso)
    mock_repositorio.ler_universo.return_value = universo_test
    ler_uni = ler_universo(mock_repositorio, nome_uni)
    assert ler_uni == universo_test
    ler_cha = mock_repositorio.ler_universo.call_args[0][0]
    assert ler_cha == nome_uni
    mock_repositorio.ler_universo.assert_called_once()

def test_atualizar_vel_nome_em_branco(dicionario_universo):
    vel_uni = ''
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeEmBranco):
        atualizar_universo(mock_repositorio, vel_uni, dicionario_universo)
    assert mock_repositorio.existe_universo.call_count == 0
    assert mock_repositorio.atualizar_universo.call_count == 0

def test_atualizar_vel_nome_grande(nome_grande, dicionario_universo):
    vel_uni = nome_grande
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeGrande):
        atualizar_universo(mock_repositorio, vel_uni, dicionario_universo)
    assert mock_repositorio.existe_universo.call_count == 0
    assert mock_repositorio.atualizar_universo.call_count == 0

def test_atualizar_novo_nome_em_branco(dicionario_universo):
    vel_uni = 'Universo 1'
    atua_uni = dicionario_universo
    atua_uni['nome'] = ''
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeEmBranco):
        atualizar_universo(mock_repositorio, vel_uni, atua_uni)
    assert mock_repositorio.existe_universo.call_count == 0
    assert mock_repositorio.atualizar_universo.call_count == 0

def test_atualizar_novo_nome_grande(dicionario_universo, nome_grande):
    vel_uni = 'Universo 1'
    atua_uni = dicionario_universo
    atua_uni['nome'] = nome_grande
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeGrande):
        atualizar_universo(mock_repositorio, vel_uni, atua_uni)
    assert mock_repositorio.existe_universo.call_count == 0
    assert mock_repositorio.atualizar_universo.call_count == 0

def test_atualizar_resumo_em_branco(dicionario_universo):
    vel_uni = 'Universo 2'
    dict_uni = dicionario_universo
    dict_uni['resumo'] = ''
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoResumoEmBranco):
        atualizar_universo(mock_repositorio, vel_uni, dict_uni)
    assert mock_repositorio.existe_universo.call_count == 0
    assert mock_repositorio.atualizar_universo.call_count == 0

def test_atualizar_novo_nome_ja_existe(dicionario_universo):
    vel_uni = 'Universo 2'
    dict_uni = dicionario_universo
    mock_repositorio = Mock(spec=RepositorioUniverso)
    mock_repositorio.existe_universo.return_value = True
    with pytest.raises(UniversoJaExiste):
        atualizar_universo(mock_repositorio, vel_uni, dict_uni)
    mock_repositorio.existe_universo.assert_called_with(dicionario_universo['nome'])

def test_atualizar_universo_nome_diferente(dicionario_universo, universo_test):
    vel_uni = 'Universo 1'
    mock_repositorio = Mock(spec=RepositorioUniverso)
    mock_repositorio.atualizar_universo.return_value = universo_test
    dict_uni = copy.deepcopy(dicionario_universo)
    dict_uni['nome'] = 'Universo 2'
    atualizar_uni = atualizar_universo(mock_repositorio, vel_uni, dicionario_universo)
    assert atualizar_uni == universo_test
    vel_cha = mock_repositorio.atualizar_universo.call_args[0][0]
    assert vel_cha == vel_uni
    atualizar_cha = mock_repositorio.atualizar_universo.call_args[0][1]
    assert atualizar_cha['id'] == dicionario_universo['id']
    assert atualizar_cha['nome'] == dicionario_universo['nome']
    assert atualizar_cha['resumo'] == dicionario_universo['resumo']
    assert atualizar_cha['criado'] == dicionario_universo['criado']
    assert atualizar_cha['alterado'] == dicionario_universo['alterado']
    mock_repositorio.atualizar_universo.assert_called_once()

def test_atualizar_universo_nome_igual(dicionario_universo, universo_test):
    vel_uni = dicionario_universo['nome']
    mock_repositorio = Mock(spec=RepositorioUniverso)
    mock_repositorio.atualizar_universo.return_value = universo_test
    atualizar_uni = atualizar_universo(mock_repositorio, vel_uni, dicionario_universo)
    assert atualizar_uni == universo_test
    vel_cha = mock_repositorio.atualizar_universo.call_args[0][0]
    assert vel_cha == vel_uni
    atualizar_cha = mock_repositorio.atualizar_universo.call_args[0][1]
    assert atualizar_cha['id'] == dicionario_universo['id']
    assert atualizar_cha['nome'] == dicionario_universo['nome']
    assert atualizar_cha['resumo'] == dicionario_universo['resumo']
    assert atualizar_cha['criado'] == dicionario_universo['criado']
    assert atualizar_cha['alterado'] == dicionario_universo['alterado']
    mock_repositorio.atualizar_universo.assert_called_once()
    assert mock_repositorio.existe_universo.call_count == 0

def test_deletar_nome_em_branco():
    nome_uni = ''
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeEmBranco):
        deletar_universo(mock_repositorio, nome_uni)
    assert mock_repositorio.deletar_universo.call_count == 0

def test_deletar_nome_grande(nome_grande):
    nome_uni = nome_grande
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeGrande):
        deletar_universo(mock_repositorio, nome_uni)
    assert mock_repositorio.deletar_universo.call_count == 0

def test_deletar_universo():
    nome_uni = 'Universo 1'
    mock_repositorio = Mock(spec=RepositorioUniverso)
    mock_repositorio.deletar_universo.return_value = None
    assert deletar_universo(mock_repositorio, nome_uni) is None
    deletar_cha = mock_repositorio.deletar_universo.call_args[0][0]
    assert deletar_cha == nome_uni
    mock_repositorio.deletar_universo.assert_called_once()

def test_id_nome_em_branco():
    nome_uni = ''
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeEmBranco):
        id_universo(mock_repositorio, nome_uni)
    assert mock_repositorio.id_universo.call_count == 0

def test_id_nome_grande(nome_grande):
    nome_uni = nome_grande
    mock_repositorio = Mock(spec=RepositorioUniverso)
    with pytest.raises(UniversoNomeGrande):
        id_universo(mock_repositorio, nome_uni)
    assert mock_repositorio.id_universo.call_count == 0

def test_id_universo():
    nome_uni = 'Universo 1'
    mock_repositorio = Mock(spec=RepositorioUniverso)
    mock_repositorio.id_universo.return_value = 1
    id_uni = id_universo(mock_repositorio, nome_uni)
    assert id_uni == 1
    mock_repositorio.id_universo.assert_called_once_with(nome_uni)
