import json
from erros import ArquivoCorrompido, ArquivoNaoEncontrado, UniversoNaoEncontrado


class RepositorioUniverso:
    def __init__(self, r_caminho):
        self.caminho = r_caminho

    def ler_arquivo(self) -> list:
        try:
            with open(self.caminho, mode='r', encoding='utf-8') as j_l_a:
                tab_l_a = json.load(j_l_a)
            return tab_l_a
        except FileNotFoundError:
            raise ArquivoNaoEncontrado(self.caminho)
        except json.JSONDecodeError:
            raise ArquivoCorrompido(self.caminho)

    def salvar_arquivo(self, tab_s_a:list) -> bool:
        try:
            with open(self.caminho, mode='w', encoding='utf-8') as j_s_a:
                json.dump(tab_s_a, j_s_a, ensure_ascii=False, allow_nan=False, indent=4)
            return True
        except FileNotFoundError:
            raise ArquivoNaoEncontrado(self.caminho)

    def existe_universo(self, e_u_nome:str) -> bool:
        tab_e_u = self.ler_arquivo()
        try:
            for e_universo in tab_e_u:
                if e_universo['Nome'] == e_u_nome:
                    return True
            return False
        except KeyError:
            raise ArquivoCorrompido(self.caminho)

    def salvar_universo(self, s_u_novo:dict) ->bool:
        tab_s_u = self.ler_arquivo()
        tab_s_u.append(s_u_novo.copy())
        self.salvar_arquivo(tab_s_u)
        return True

    def ler_universo(self, l_u_nome:str) ->dict:
        tab_l_u = self.ler_arquivo()
        for l_universo in tab_l_u:
            if l_universo.get('Nome') == l_u_nome:
                return l_universo
        raise UniversoNaoEncontrado(self.caminho)

    def atualizar_universo(self, v_u_nome:str, a_u_universo:dict) ->bool:
        tab_a_u = self.ler_arquivo()
        for a_universo in tab_a_u:
            if a_universo['Nome'] == v_u_nome:
                a_universo['Nome'] = a_u_universo['Nome']
                a_universo['Resumo'] = a_u_universo['Resumo']
                a_universo['Criado'] = a_u_universo['Criado']
                a_universo['Alterado'] = a_u_universo['Alterado']
                self.salvar_arquivo(tab_a_u)
                return True
        raise UniversoNaoEncontrado(self.caminho)

    def deletar_universo(self, d_u_nome:str) ->bool:
        tab_d_u = self.ler_arquivo()
        for d_universo in tab_d_u:
            if d_universo['Nome'] == d_u_nome:
                tab_d_u.remove(d_universo)
                self.salvar_arquivo(tab_d_u)
                return True
        raise UniversoNaoEncontrado(self.caminho)