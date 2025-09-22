import pytest
import json
from reader import Universo, RepositorioUniverso
from reader import UniversoJaExiste, ArquivoNaoEncontrado, ArquivoCorrompido, UniversoNaoEncontrado
from unittest.mock import patch

def arquivo_certo_lista() ->list:
    arquivo_c_l = [
        {
            'Nome': 'Forgotten Realms',
            'Resumo': 'Forgotten Realms é um universo de Dungeons and Dragons.',
            'Criado': '07-1987',
            'Alterado': '25-05-2025'
        },
        {
            'Nome': 'Grayhawk',
            'Resumo': 'Grayhawk é um cenário de RGP criado por Gary Gygax para o jogo Dungeons and Dragons.',
            'Criado': '07-1987',
            'Alterado': '19-06-2025'
        }
    ]
    return arquivo_c_l

def universo_dicionario() ->dict:
    dicionario_d = {
        'Nome': 'Forgotten Realms',
        'Resumo': 'Forgotten Realms é um universo de Dungeons and Dragons.',
        'Criado': '07-1987',
        'Alterado': '25-05-2025'
    }
    return dicionario_d

def dicionario_criar() -> dict:
    dicionario_c = {
        'Nome': 'Dragonlance',
        'Resumo': 'Dragonlance é um cenário de RPG de Dungeons and Dragons.',
        'Criado': '03-1987',
        'Alterado': '25-05-2025'
    }
    return dicionario_c

def arquivo_corrompido_lista() ->str:
    arquivo_c_l = """{'Nome': "Arquivo corrompido JSON"
        'Resumo': "OláMundo"
        'Criado': "Não faço ideia"
        'Alterado' : 000
        """
    return arquivo_c_l

def dicionario_atualizar() -> dict:
    dicionario_a ={
        'Nome': 'Forgotten Realms',
        'Resumo': 'Forgotten Realms não é mais o universo principal de Dungeons and Dragons.',
        'Criado': '07-1987',
        'Alterado': '25-05-2025'
    }
    return dicionario_a

@pytest.fixture
def mock_repositorio_certo(tmp_path):
    mock_dicionario_arquivo_certo = arquivo_certo_lista()
    mock_inicializar_arquivo_certo = tmp_path / 'caminho.json'
    with open(mock_inicializar_arquivo_certo, mode='w', encoding='utf-8') as a_r_i:
        json.dump(mock_dicionario_arquivo_certo, a_r_i, ensure_ascii=False, allow_nan=False, indent=4)
    mock_repositorio_final = RepositorioUniverso(str(mock_inicializar_arquivo_certo))
    mock_repositorio_final.caminho = str(mock_inicializar_arquivo_certo)
    return mock_repositorio_final

@pytest.fixture
def mock_repositorio_inexistente():
    mock_inicializar_arquivo_inexistente = 'caminho_nao_existe/caminho.json'
    mock_inexistente_final = RepositorioUniverso(str(mock_inicializar_arquivo_inexistente))
    mock_inexistente_final.caminho = str(mock_inicializar_arquivo_inexistente)
    return mock_inexistente_final

@pytest.fixture
def mock_repositorio_corrompido(tmp_path):
    mock_dicionario_corrompido = arquivo_corrompido_lista()
    mock_ler_arquivo_corrompido = tmp_path / 'corrompido.json'
    with open(mock_ler_arquivo_corrompido, mode='w', encoding='utf-8') as a_r_c_c:
        a_r_c_c.write(mock_dicionario_corrompido)
    mock_corrompido_final = RepositorioUniverso(str(mock_ler_arquivo_corrompido))
    mock_corrompido_final.caminho = str(mock_ler_arquivo_corrompido)
    return mock_corrompido_final

def test_universo_inicializar(mock_repositorio_certo):
    # Teste: inicializando teste certo
    caminho_inicializar = mock_repositorio_certo.caminho
    with patch ('reader.universo.caminho', new=caminho_inicializar):
        universo_inicializar_certo = Universo()
        assert universo_inicializar_certo.repositorio.caminho == mock_repositorio_certo.caminho

def test_universo_criar(mock_repositorio_certo, mock_repositorio_inexistente):
    # Teste: criar universo certo
    caminho_criar_certo = mock_repositorio_certo.caminho
    with patch('reader.universo.caminho', new=caminho_criar_certo):
        universo_criar_certo = Universo()
        u_d_c = dicionario_criar()
        universo_criar_certo.criar(u_d_c['Nome'], u_d_c['Resumo'])
        assert mock_repositorio_certo.ler_universo(u_d_c['Nome']) == universo_criar_certo.para_dict()

    # Teste ERRO: universo já existente
    caminho_criar_existente = mock_repositorio_certo.caminho
    with patch('reader.universo.caminho', new=caminho_criar_existente):
        universo_criar_existente = Universo()
        u_d_e = universo_dicionario()
        with pytest.raises(UniversoJaExiste):
            universo_criar_existente.criar(u_d_e['Nome'], u_d_e['Resumo'])

    # Teste ERRO: arquivo não encontrado
    caminho_criar_inexistente = mock_repositorio_inexistente.caminho
    with patch('reader.universo.caminho', new=caminho_criar_inexistente):
        universo_inexistente_criar = Universo()
        u_d_c_i = universo_dicionario()
        with pytest.raises(ArquivoNaoEncontrado):
            universo_inexistente_criar.ler(u_d_c_i['Nome'])

def test_universo_ler(mock_repositorio_certo, mock_repositorio_inexistente, mock_repositorio_corrompido):
    # Teste: ler universos existentes
    caminho_ler_certo = mock_repositorio_certo.caminho
    with patch('reader.universo.caminho', new=caminho_ler_certo):
        universo_ler_certo = Universo()
        u_d_l = universo_dicionario()
        universo_ler_certo.ler(u_d_l['Nome'])
        assert universo_ler_certo.nome == u_d_l['Nome']

    # Teste ERRO: arquivo não encontrado
    caminho_ler_arquivo_inexistente = mock_repositorio_inexistente.caminho
    with patch('reader.universo.caminho', new=caminho_ler_arquivo_inexistente):
        universo_ler_inexistente = Universo()
        u_d_l_i = universo_dicionario()
        with pytest.raises(ArquivoNaoEncontrado):
            universo_ler_inexistente.ler(u_d_l_i['Nome'])

    # Teste ERRO: arquivo corrompido
    caminho_ler_corrompido = mock_repositorio_corrompido.caminho
    with patch('reader.universo.caminho', new=caminho_ler_corrompido):
        universo_ler_corrompido = Universo()
        u_d_c_c = universo_dicionario()
        with pytest.raises(ArquivoCorrompido):
            universo_ler_corrompido.ler(u_d_c_c['Nome'])

    # Teste ERRO: universo não encontrado
    caminho_ler_universo_inexistente = mock_repositorio_certo.caminho
    with patch('reader.universo.caminho', new=caminho_ler_universo_inexistente):
        universo_ler_nao_encontrado = Universo()
        with pytest.raises(UniversoNaoEncontrado):
            universo_ler_nao_encontrado.ler('SpellJam')

def test_universo_atualizar(mock_repositorio_certo, mock_repositorio_inexistente, mock_repositorio_corrompido):
    # Teste: atualizar universo existente
    caminho_atualizar_certo = mock_repositorio_certo.caminho
    with patch('reader.universo.caminho', new=caminho_atualizar_certo):
        universo_atualizar_certo = Universo()
        u_d_a = dicionario_atualizar()
        universo_atualizar_certo.ler(u_d_a['Nome'])
        universo_atualizar_certo.atualizar(u_d_a['Nome'], u_d_a['Resumo'])
        assert universo_atualizar_certo.nome == u_d_a['Nome']
        assert universo_atualizar_certo.resumo == u_d_a['Resumo']
        assert universo_atualizar_certo.criado == u_d_a['Criado']
        assert universo_atualizar_certo.alterado != u_d_a['Alterado']

    # Teste ERRO: arquivo não encontrado
    caminho_atualizar_arquivo_inexistente = mock_repositorio_inexistente.caminho
    with patch('reader.universo.caminho', new=caminho_atualizar_arquivo_inexistente):
        universo_atualizar_inexistente = Universo()
        u_d_a_i = dicionario_atualizar()
        with pytest.raises(ArquivoNaoEncontrado):
            universo_atualizar_inexistente.atualizar(u_d_a_i['Nome'], u_d_a_i['Resumo'])

    # Teste ERRO: arquivo corrompido
    caminho_atualizar_corrompido = mock_repositorio_corrompido.caminho
    with patch('reader.universo.caminho', new=caminho_atualizar_corrompido):
        universo_atualizar_corrompido = Universo()
        u_d_a_c = dicionario_atualizar()
        with pytest.raises(ArquivoCorrompido):
            universo_atualizar_corrompido.atualizar(u_d_a_c['Nome'], u_d_a_c['Resumo'])

    # Teste ERRO: universo não encontrado
    caminho_atualizar_universo_inexistente = mock_repositorio_certo.caminho
    with patch('reader.universo.caminho', new=caminho_atualizar_universo_inexistente):
        universo_atualizar_nao_encontrado = Universo()
        u_d_a_u_i = dicionario_atualizar()
        with pytest.raises(UniversoNaoEncontrado):
            universo_atualizar_nao_encontrado.atualizar(u_d_a_u_i['Nome'], u_d_a_u_i['Resumo'])

def test_universo_deletar(mock_repositorio_certo, mock_repositorio_inexistente, mock_repositorio_corrompido):
    # Teste: deletar universo existente
    caminho_deletar_certo = mock_repositorio_certo.caminho
    with patch('reader.universo.caminho', new=caminho_deletar_certo):
        universo_deletar_certo = Universo()
        u_d_c = dicionario_atualizar()
        universo_deletar_certo.ler(u_d_c['Nome'])
        universo_deletar_certo.deletar()
        with pytest.raises(UniversoNaoEncontrado):
            universo_deletar_certo.ler(u_d_c['Nome'])

    # Teste ERRO: arquivo não encontrado
    caminho_deletar_arquivo_inexistente = mock_repositorio_inexistente.caminho
    with patch('reader.universo.caminho', new=caminho_deletar_arquivo_inexistente):
        universo_deletar_arquivo_inexistente = Universo()
        with pytest.raises(ArquivoNaoEncontrado):
            universo_deletar_arquivo_inexistente.deletar()

    # Teste ERRO: arquivo corrompido
    caminho_deletar_corrompido = mock_repositorio_corrompido.caminho
    with patch('reader.universo.caminho', new=caminho_deletar_corrompido):
        universo_deletar_corrompido = Universo()
        with pytest.raises(ArquivoCorrompido):
            universo_deletar_corrompido.deletar()

    # Teste ERRO: universo não encontrado
    caminho_deletar_nao_encontrado = mock_repositorio_certo.caminho
    with patch('reader.universo.caminho', new=caminho_deletar_nao_encontrado):
        universo_deletar_nao_encontrado = Universo()
        with pytest.raises(UniversoNaoEncontrado):
            universo_deletar_nao_encontrado.deletar()
