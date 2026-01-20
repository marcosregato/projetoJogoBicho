# Projeto Jogo do Bicho

Este projeto realiza a coleta automatizada (web scraping) dos resultados do "Jogo do Bicho" utilizando Python e Selenium, armazenando as informações em um banco de dados SQLite local.

## Estrutura do Projeto

- `screenScraping.py`: Script principal que realiza o scraping e gerencia o banco de dados.
- `test_funcional.py`: Testes unitários e funcionais.
- `resultados.db`: Banco de dados SQLite (gerado automaticamente).

## Pré-requisitos

- Python 3.12+
- Google Chrome instalado (para o Selenium WebDriver)

## Instalação

1. Configure o ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

Executando o script (exemplo)

O script cria/usa o banco `resultados.db` no diretório do projeto. O bloco `__main__`:

- Inicializa o banco de dados e cria as tabelas se necessário.
- Insere registros de teste em `dataJogo`, `resultJogo` e `grupo`.
- Imprime os resultados da tabela `resultJogo`.

```bash
# Com o ambiente virtual ativado:
python screenScraping.py
```

Rodando os testes

```bash
./bin/python3 -m pytest -q tests --ignore=lib --ignore=lib64
```

Arquivo de banco gerado

- [resultados.db](resultados.db) (criado no diretório do projeto quando o script é executado)
