import pytest
import json
from reader import Universo
from reader import RepositorioUniverso
from reader import ArquivoCorrompido
from reader import ArquivoNaoEncontrado
from reader import UniversoNaoEncontrado
from unittest.mock import patch


def arquivo_certo_lista() ->list:
    arquivo_c_l = [
        {
            'Nome': 'Phamelosoph',
            'Resumo': 'Esse universo pertence ao Nathan.',
            'Criado': '01-01-2001',
            'Alterado': '25-05-2025'
        },
        {
            'Nome': 'Grandar',
            'Resumo': 'Esse universo pertence ao Felipe.',
            'Criado': '01-01-2020',
            'Alterado': '01-01-2024'
        }
    ]
    return arquivo_c_l

def arquivo_corrompido_lista() ->str:
    arquivo_c_l = """{'Nome': "Arquivo corrompido JSON"
        'Resumo': "OláMundo"
        'Criado': "Não faço ideia"
        'Alterado' : 000
        """
    return arquivo_c_l

def arquivo_sem_nome_lista() ->list:
    arquivo_arquivo_sem_nome_lista = [{
        'Resumo': 'Arquivo sem nome',
        'Criado': '01-01-2025',
        'Alterado': '01-05-2025'
    }]
    return arquivo_arquivo_sem_nome_lista

def universo_novo() ->dict:
    dicionario_universo_novo ={
        'Nome': 'Forgotten Realms',
        'Resumo': 'Forgotten Realms é um universo de Dungeons and Dragons.',
        'Criado': '07-1987',
        'Alterado': '25-05-2025'
    }
    return dicionario_universo_novo

def universo_leitura() ->dict:
    dicionario_universo_leitura = {
            'Nome': 'Phamelosoph',
            'Resumo': 'Esse universo pertence ao Nathan.',
            'Criado': '01-01-2001',
            'Alterado': '25-05-2025'
        }
    return dicionario_universo_leitura

def universo_atualizar() -> dict:
    dicionario_universo_atualizar = {
            'Nome': 'Phamelosoph',
            'Resumo': 'Esse universo pertence ao Nathan e ao Felipe.',
            'Criado': '01-01-2001',
            'Alterado': '17-06-2025'
        }
    return dicionario_universo_atualizar

def arquivo_certo_atualizar_lista() ->list:
    arquivo_c_a_l = [
        {
            'Nome': 'Phamelosoph',
            'Resumo': 'Esse universo pertence ao Nathan e ao Felipe.',
            'Criado': '01-01-2001',
            'Alterado': '17-06-2025'
        },
        {
            'Nome': 'Grandar',
            'Resumo': 'Esse universo pertence ao Felipe.',
            'Criado': '01-01-2020',
            'Alterado': '01-01-2024'
        }
    ]
    return arquivo_c_a_l

def arquivo_deletado_lista() ->list:
    arquivo_d_l = [
        {
            'Nome': 'Grandar',
            'Resumo': 'Esse universo pertence ao Felipe.',
            'Criado': '01-01-2020',
            'Alterado': '01-01-2024'
        }
    ]
    return arquivo_d_l

@pytest.fixture
def caminho_certo_json(tmp_path):
    caminho_certo_fixture = tmp_path / 'universo_certo.json'
    arquivo_mockado = arquivo_certo_lista()
    with open(caminho_certo_fixture,mode='w', encoding='utf-8') as j_m:
        json.dump(arquivo_mockado, j_m, ensure_ascii=False, allow_nan=False, indent=4)
    return caminho_certo_fixture

@pytest.fixture
def caminho_vazio_json(tmp_path):
    caminho_vazio_fixture = tmp_path / 'universo_vazio.json'
    arquivo_vazio = []
    with open(caminho_vazio_fixture, mode='w', encoding='utf-8') as j_c_v:
        json.dump(arquivo_vazio, j_c_v, ensure_ascii=False, allow_nan=False, indent=4)
    return caminho_vazio_fixture

@pytest.fixture
def caminho_corrompido_json(tmp_path):
    caminho_corrompido_fixture = tmp_path / 'universo_corrompido.json'
    tab_a_c_j = arquivo_corrompido_lista()
    with open(caminho_corrompido_fixture, mode='w', encoding='utf-8') as j_a_c:
        j_a_c.write(tab_a_c_j)
    return caminho_corrompido_fixture

@pytest.fixture
def caminho_sem_nome_json(tmp_path):
    caminho_sem_nome_fixture = tmp_path / 'universo_sem_nome.json'
    tab_a_s_n_j = arquivo_sem_nome_lista()
    with open(caminho_sem_nome_fixture, mode='w', encoding='utf-8') as j_a_s_n:
        json.dump(tab_a_s_n_j, j_a_s_n, ensure_ascii=False, allow_nan=False, indent=4)
    return caminho_sem_nome_fixture

def test_repositorio_ler_arquivo(caminho_certo_json, caminho_vazio_json, caminho_corrompido_json):
    # Teste: arquivo lido corretamente
    repositorio_certo_ler = RepositorioUniverso(caminho_certo_json)
    arquivo_certo_ler = repositorio_certo_ler.ler_arquivo()
    arquivo_mockado_certo_ler = arquivo_certo_lista()
    assert arquivo_certo_ler == arquivo_mockado_certo_ler
    # Teste: arquivo vazio
    repositorio_vazio_ler = RepositorioUniverso(caminho_vazio_json)
    assert repositorio_vazio_ler.ler_arquivo() == []
    # Teste ERRO: caminho não encontrado
    repositorio_nao_encontrado_ler = RepositorioUniverso('caminho_nao_existe.json')
    with pytest.raises(ArquivoNaoEncontrado):
        repositorio_nao_encontrado_ler.ler_arquivo()
    # Teste ERRO: arquivo corrompido
    repositorio_corrompido_ler = RepositorioUniverso(caminho_corrompido_json)
    with pytest.raises(ArquivoCorrompido):
        repositorio_corrompido_ler.ler_arquivo()

def test_repositorio_salvar_arquivo(caminho_vazio_json):
    # Teste: arquivo salvo corretamente
    repositorio_certo_salvar_arquivo = RepositorioUniverso(caminho_vazio_json)
    lista_certa_salvar_arquivo = arquivo_certo_lista()
    assert repositorio_certo_salvar_arquivo.salvar_arquivo(lista_certa_salvar_arquivo) == True
    assert repositorio_certo_salvar_arquivo.ler_arquivo() == lista_certa_salvar_arquivo
    # Teste ERRO: arquivo não encontrado
    repositorio_caminho_errado_salvar_arquivo = RepositorioUniverso('pasta_nao_existe/arquivo_nao_existe.json')
    with pytest.raises(ArquivoNaoEncontrado):
        repositorio_caminho_errado_salvar_arquivo.salvar_arquivo(lista_certa_salvar_arquivo)

def test_repositorio_existe_universo(caminho_certo_json, caminho_vazio_json, caminho_sem_nome_json):
    # Teste: universo existe
    repositorio_certo_existe_universo = RepositorioUniverso(caminho_certo_json)
    resposta_certa_existe_universo = repositorio_certo_existe_universo.existe_universo('Phamelosoph')
    assert resposta_certa_existe_universo == True
    # Teste: universo não existe
    resposta_certa_existe_universo = repositorio_certo_existe_universo.existe_universo('GRANDAR')
    assert  resposta_certa_existe_universo == False
    resposta_certa_existe_universo = repositorio_certo_existe_universo.existe_universo('Forgotten Realms')
    assert resposta_certa_existe_universo == False
    # Teste: arquivo vazio
    repositorio_vazia_existe_universo = RepositorioUniverso(caminho_vazio_json)
    resposta_vazia_existe_universo = repositorio_vazia_existe_universo.existe_universo('Phamelosoph')
    assert resposta_vazia_existe_universo == False
    # Teste ERRO: arquivo corrompido
    repositorio_corrompido_existe_arquivo = RepositorioUniverso(caminho_sem_nome_json)
    with pytest.raises(ArquivoCorrompido):
        repositorio_corrompido_existe_arquivo.existe_universo('Phamelosoph')

def test_repositorio_salvar_universo(caminho_certo_json):
    # Teste: salvamento correto
    repositorio_certo_salvar_universo = RepositorioUniverso(caminho_certo_json)
    dicionario_certo_salvar_universo = universo_novo()
    repositorio_certo_salvar_universo.salvar_universo(dicionario_certo_salvar_universo)
    conferencia_arquivo_certo = arquivo_certo_lista()
    conferencia_arquivo_certo.append(dicionario_certo_salvar_universo.copy())
    assert repositorio_certo_salvar_universo.ler_arquivo() == conferencia_arquivo_certo

def test_repositorio_ler_universo(caminho_certo_json):
    # Teste: leitura correta
    repositorio_certo_ler_universo = RepositorioUniverso(caminho_certo_json)
    universo_certo_ler = 'Phamelosoph'
    universo_certo_dados = universo_leitura()
    assert repositorio_certo_ler_universo.ler_universo(universo_certo_ler) == universo_certo_dados
    # Teste ERRO: universo não encontrado
    repositorio_errado_ler_universo = RepositorioUniverso(caminho_certo_json)
    universo_errado_ler = 'Grayhawk'
    with pytest.raises(UniversoNaoEncontrado):
        repositorio_errado_ler_universo.ler_universo(universo_errado_ler)

def test_repositorio_atualizar_universo(caminho_certo_json):
    # Teste: atualização correta
    repositorio_certo_atualizar_universo = RepositorioUniverso(caminho_certo_json)
    universo_certo_atualizar_nome = 'Phamelosoph'
    universo_certo_atualizar_dict = universo_atualizar()
    repositorio_certo_atualizar_universo.atualizar_universo(universo_certo_atualizar_nome, universo_certo_atualizar_dict)
    assert  repositorio_certo_atualizar_universo.ler_arquivo() == arquivo_certo_atualizar_lista()
    # Teste Erro: universo não encontrado
    repositorio_erro_atualizar_universo = RepositorioUniverso(caminho_certo_json)
    universo_inexistente_atualizar_nome = 'Dragonlance'
    universo_inexistente_atualizar_dict = universo_atualizar()
    with pytest.raises(UniversoNaoEncontrado):
        repositorio_erro_atualizar_universo.atualizar_universo(universo_inexistente_atualizar_nome, universo_inexistente_atualizar_dict)

def test_repositorio_deletar_universo(caminho_certo_json):
    # Teste: deletar corretamente
    repositorio_certo_deletar_universo = RepositorioUniverso(caminho_certo_json)
    universo_certo_deletar_nome = 'Phamelosoph'
    repositorio_certo_deletar_universo.deletar_universo(universo_certo_deletar_nome)
    assert repositorio_certo_deletar_universo.ler_arquivo() == arquivo_deletado_lista()


@patch.object(RepositorioUniverso, 'ler_universo')
def test_universo_ler(mock_method):
    dicionario ={
        'Nome':'Phamelosoph',
        'Resumo':'Phamelosoph é um universo do Nathan Ramos Lima e Silva.',
        'Criado':'01-01-2001',
        'Alterado':'24-05-2025'
    }
    mock_method.return_value = dicionario

    universo_falso_ler = Universo()
    universo_falso_ler.ler('Phamelosoph')
