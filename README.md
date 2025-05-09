# 📖 book_tales

**book_tales** é um projeto simples escrito em Python que permite salvar e ler textos como se fossem pequenos contos ou anotações. Ideal para organizar histórias de RPG, anotações pessoais ou rascunhos rápidos.

## ✨ Funcionalidades

- Salvar textos com título e autor em arquivos `.json`
- Ler textos salvos diretamente do terminal
- Verificação se o título já existe, para evitar sobrescrever sem confirmação
- Interface de terminal amigável

## 🗃 Estrutura do Projeto

```bash
book_tales/
├── main.py        # Ponto de entrada do programa (menu interativo)
└── reader.py      # Lógica de salvar e ler arquivos JSON
```

## 🚀 Como usar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/book_tales.git
cd book_tales
```
2. Execute o programa:
```bash
python main.py
```
3. Escolha entre:
```bash
[S] para salvar um novo texto

[L] para ler um texto existente

[N] para sair
```