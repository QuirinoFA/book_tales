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
    def __init__(self):
        super().__init__(f"Universo já existe.")

class UniversoNaoEncontrado(ErroUniverso):
    def __init__(self):
        super().__init__(f"Universo não encontrado.")

class UniversoNomeEmBranco(ErroUniverso):
    def __init__(self):
        super().__init__('Universo com nome em branco.')

class UniversoNomeGrande(ErroUniverso):
    def __init__(self):
        super().__init__('Universo com nome acima de 255 caracteres.')

class UniversoResumoEmBranco(ErroUniverso):
    def __init__(self):
        super().__init__('Universo com resumo em branco.')

class ErroTexto(Exception):
    pass

class TextoJaExiste(ErroTexto):
    def __init__(self):
        super().__init__(f'Texto já existe.')

class TextoNaoEncontrado(ErroTexto):
    def __init__(self):
        super().__init__(f'Texto não encontrado.')

class TextoTituloEmBranco(ErroTexto):
    def __init__(self):
        super().__init__(f'Texto com título em branco.')

class TextoTituloGrande(ErroTexto):
    def __init__(self):
        super().__init__(f'Texto com título acima de 255 caracteres.')

class TextoTextoEmBranco(ErroTexto):
    def __init__(self):
        super().__init__('Texto com texto em branco.')
