class ErroArquivo(Exception):
    pass

class ArquivoNaoEncontrado(ErroArquivo):
    def __init__(self, a_n_e_caminho):
        self.caminho = a_n_e_caminho
        super().__init__(f"Arquivo não encontrado. Caminho: {self.caminho}")

class ArquivoCorrompido(ErroArquivo):
    def __init__(self, a_c_caminho):
        self.caminho = a_c_caminho
        super().__init__(f"Arquivo corrompido. Caminho: {self.caminho}")

class ErroUniverso(Exception):
    pass

class UniversoJaExiste(ErroUniverso):
    def __init__(self, u_j_e_caminho):
        self.caminho = u_j_e_caminho
        super().__init__(f"Universo já existe. Caminho {self.caminho}")

class UniversoNaoEncontrado(ErroUniverso):
    def __init__(self,  u_n_e_caminho):
        self.caminho = u_n_e_caminho
        super().__init__(f"Universo não encontrado. Caminho {self.caminho}")