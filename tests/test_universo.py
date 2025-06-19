import pytest
import json
from reader import Universo, caminho
from reader import RepositorioUniverso
from unittest.mock import patch, MagicMock
from reader import UniversoJaExiste

def universo_dict() ->dict:
    u_d = {
        "Nome": "Forgotten Realms",
        "Resumo": "Forgotten Realms é um universo de Dungeons and Dragons.",
        "Criado": "07-1987",
        "Alterado": "25-05-2025"
    }
    return u_d

def universo_alterar_dict() ->dict:
    u_a_d = {
        "Nome": "Grayhalk",
        "Resumo": "Grayhawk é um cenário de RGP criado por Gary Gygax para o jogo Dungeons and Dragons.",
        "Criado": "07-1987",
        "Alterado": "19-06-2025"
    }
    return u_a_d

@patch('reader.universo.RepositorioUniverso')
def test_universo_inicializar(mock_universo_inicializar):
    # Teste: inicializar correta dos valores mocando o repositório
    mock_universo_instancia = MagicMock()
    mock_universo_inicializar.return_value = mock_universo_instancia
    universo_inicializar = Universo()

    assert universo_inicializar.nome is None
    assert universo_inicializar.resumo is None
    assert universo_inicializar.criado is None
    assert universo_inicializar.alterado is None
    assert universo_inicializar.repositorio == mock_universo_instancia

    mock_universo_inicializar.assert_called_once_with(caminho)

@patch('reader.universo.RepositorioUniverso')
def test_universo_dicionario(mock_universo_dicionario):
    # Teste: criação correta de dicionario com parâmetros
    mock_universo_dicionario.return_value = MagicMock()
    universo_dicionario = Universo()

    u_d_d = universo_dict()
    for chave_u_d_d, item_u_d_d in u_d_d.items():
        setattr(universo_dicionario, chave_u_d_d.lower(), item_u_d_d)

    assert universo_dicionario.para_dict() == universo_dict()
    mock_universo_dicionario.assert_called_once_with(caminho)

@patch('reader.universo.RepositorioUniverso')
def test_universo_criar(mock_universo_criar):
    # Teste: criar um novo universo
    mock_universo_instancia_certo = MagicMock()
    mock_universo_criar.return_value = mock_universo_instancia_certo
    mock_universo_instancia_certo.existe_universo.return_value = False

    universo_criar_certo = Universo()
    u_c_d = universo_dict()
    universo_criar_certo.criar(u_c_d['Nome'], u_c_d['Resumo'])

    assert universo_criar_certo.nome == u_c_d['Nome']
    assert universo_criar_certo.resumo == u_c_d['Resumo']
    assert universo_criar_certo.criado is not None
    assert universo_criar_certo.alterado is None
    mock_universo_instancia_certo.salvar_universo.assert_called_once_with(universo_criar_certo.para_dict())

@patch('reader.universo.RepositorioUniverso')
def test_universo_criar_erro(mock_universo_criar_erro):
    # Teste ERRO:universo já existe
    mock_universo_instancia_erro = MagicMock()
    mock_universo_criar_erro.return_value = mock_universo_instancia_erro
    mock_universo_instancia_erro.existe_universo.return_value = True

    universo_criar_erro = Universo()
    u_c_d_e = universo_dict()
    with pytest.raises(UniversoJaExiste):
        universo_criar_erro.criar(u_c_d_e['Nome'], u_c_d_e['Resumo'])
    mock_universo_criar_erro.assert_called_once_with(caminho)

@patch('reader.universo.RepositorioUniverso')
def test_universo_ler(mock_universo_ler):
    # Teste: universo lido com sucesso
    mock_universo_ler_instancia = MagicMock()
    mock_universo_ler.return_value = mock_universo_ler_instancia
    u_l_m = universo_dict()
    mock_universo_ler_instancia.ler_universo.return_value = u_l_m

    universo_ler = Universo()
    universo_ler.ler(u_l_m['Nome'])
    assert universo_ler.nome == u_l_m['Nome']
    assert universo_ler.resumo == u_l_m['Resumo']
    assert universo_ler.criado == u_l_m['Criado']
    assert universo_ler.alterado == u_l_m['Alterado']
    mock_universo_ler.assert_called_once_with(caminho)
    mock_universo_ler_instancia.ler_universo.assert_called_once_with(u_l_m['Nome'])

@patch('reader.universo.RepositorioUniverso')
def test_universo_alterar(mock_universo_alterar):
    # Teste: alterar universo com sucesso
    mock_universo_alterar_instancia = MagicMock()
    mock_universo_alterar.return_value = mock_universo_alterar_instancia
    u_a_a = universo_dict()
    mock_universo_alterar_instancia.ler_universo.return_value = u_a_a
    u_d_a = universo_alterar_dict()

    universo_alterar = Universo()
    for chave_alterar, valor_alterar in u_a_a.items():
        setattr(universo_alterar, chave_alterar.lower(), valor_alterar)
    universo_alterar.atualizar(u_d_a['Nome'], u_d_a['Resumo'])

    assert universo_alterar.nome == u_d_a['Nome']
    assert universo_alterar.resumo == u_d_a['Resumo']
    assert universo_alterar.criado == u_a_a['Criado']
    assert universo_alterar.alterado != u_a_a['Alterado']
    mock_universo_alterar_instancia.ler_universo.assert_called_once_with(u_a_a['Nome'])
    mock_universo_alterar_instancia.atualizar_universo.assert_called_once_with(u_a_a['Nome'], universo_alterar.para_dict())

@patch('reader.universo.RepositorioUniverso')
def test_universo_deletar(mock_universo_deletar):
    # Teste: deletar arquivo com sucesso
    mock_universo_deletar_instancia = MagicMock()
    mock_universo_deletar.return_value = mock_universo_deletar_instancia
    u_d = universo_dict()

    universo_deletar = Universo()
    for chave_deletar, valor_deletar in u_d.items():
        setattr(universo_deletar, chave_deletar.lower(), valor_deletar)
    universo_deletar.deletar()

    assert universo_deletar.nome is None
    assert universo_deletar.resumo is None
    assert universo_deletar.criado is None
    assert universo_deletar.alterado is None
    mock_universo_deletar_instancia.deletar_universo.assert_called_once_with(u_d['Nome'])
