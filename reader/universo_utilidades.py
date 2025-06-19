from universo import Universo

def nome_universo_valido():
    while True:
        n_v_nome = str(input('Nome: '))
        if n_v_nome:
            return n_v_nome
        else:
            print('ERRO! Digite um nome para o universo!')

def salvar_universo() ->None:
    su_nome = nome_universo_valido()
    su_resumo = str(input('Resumo: '))
    su_salva = Universo()
    su_salva.criar(su_nome, su_resumo)

def ler_universo() ->None:
    lu_nome = nome_universo_valido()
    lu_uni = Universo()
    lu_uni.ler(lu_nome)
    print(f'Nome: {lu_uni.nome}')
    print(f'Resumo: {lu_uni.resumo}')
    print(f'Criado: {lu_uni.criado}')
    print(f'Alterado: {lu_uni.alterado}')

def atualizar_universo() -> None:
    print('Velho Universo ', end='')
    vu_nome = nome_universo_valido()
    au_universo = Universo()
    au_universo.ler(vu_nome)
    print('Novo Universo ', end='')
    au_nome = nome_universo_valido()
    au_resumo = str(input('Resumo: '))
    au_universo.atualizar(au_nome, au_resumo)

def deletar_universo() ->None:
    du_nome = nome_universo_valido()
    du_universo = Universo()
    du_universo.ler(du_nome)
    du_universo.deletar()