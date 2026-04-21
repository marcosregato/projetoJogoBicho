# 🎲 Projeto Jogo do Bicho

Sistema completo para coleta, armazenamento e análise de resultados do Jogo do Bicho utilizando web scraping, banco de dados SQLite e análise estatística.

## ✨ Funcionalidades

- **Web Scraping Automatizado**: Coleta resultados em tempo real do site ojogodobicho.com
- **Banco de Dados Estruturado**: Armazenamento organizado com relacionamentos adequados
- **Análise Estatística**: Visualizações e insights sobre padrões dos resultados
- **Arquitetura Modular**: Código organizado em módulos separados para melhor manutenção
- **Tratamento de Erros**: Robusta gestão de exceções e validação de dados
- **Compatibilidade**: Mantém compatibilidade com código legado

## 📁 Estrutura do Projeto

```
projetoJogoBicho/
├── 📄 README.md                 # Documentação do projeto
├── 🐍 screenScraping.py         # Script principal (legado)
├── 📄 config.py                 # Configurações e constantes
├── 🗄️ database.py              # Módulo de gerenciamento do banco
├── 🕷️ scraper.py               # Módulo de web scraping
├── 🧪 test_funcional.py         # Testes unitários e funcionais
├── 📊 estatisticaJogoBiho.ipynb # Análise estatística e visualizações
├── 🗃️ jogoBichoDB.sql          # Schema do banco de dados
├── 📄 populate_data.sql         # Dados de exemplo
├── 📋 requirements.txt          # Dependências Python
├── 🗂️ .gitignore              # Arquivos ignorados pelo Git
├── 🗂️ .vscode/               # Configurações do VS Code
└── 💾 resultados.db             # Banco de dados SQLite (gerado automaticamente)
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.12+
- Google Chrome instalado
- ChromeDriver (gerenciado automaticamente)

### Configuração do Ambiente

1. **Clone o repositório**:
```bash
git clone <repository-url>
cd projetoJogoBicho
```

2. **Crie e ative o ambiente virtual**:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Modo de Teste (Padrão)
Executa o script com dados de teste:

```bash
python screenScraping.py
```

### Modo de Scraping
Coleta dados reais do site:

```bash
python screenScraping.py --scraping
```

### Usando os Módulos Diretamente

```python
from scraper import JogoBichoScraper
from database import get_connection, fetch_all_results_with_details

# Web scraping
with JogoBichoScraper() as scraper:
    resultados = scraper.get_resultados()
    print(f"Encontrados {len(resultados)} resultados")

# Consulta ao banco
with get_connection() as conn:
    dados = fetch_all_results_with_details(conn)
    for resultado in dados[:5]:
        print(resultado)
```

## 📊 Análise de Dados

O notebook `estatisticaJogoBiho.ipynb` oferece análises estatísticas completas:

- Frequência de animais sorteados
- Distribuição de milhares, centenas e dezenas
- Visualizações com matplotlib
- Análises temporais
- Padrões e tendências

Execute com:
```bash
jupyter notebook estatisticaJogoBiho.ipynb
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais

- **datajogo**: Informações sobre data e horário dos sorteios
- **resultjogo**: Números sorteados (milhar, centena, dezena)
- **grupo**: Prêmios e animais correspondentes

### Relacionamentos
```
datajogo (1) ←→ (N) resultjogo (1) ←→ (N) grupo
```

## 🧪 Testes

Execute a suite de testes:

```bash
python -m pytest test_funcional.py -v
```

Ou execute diretamente:
```bash
python test_funcional.py
```

## ⚙️ Configuração

### Variáveis de Ambiente (Opcional)
```bash
export JOGO_BICHO_DB_PATH="/caminho/customizado.db"
export JOGO_BICHO_HEADLESS="true"
export JOGO_BICHO_TIMEOUT="30"
```

### Configurações no Código
Edite `config.py` para personalizar:
- URLs de scraping
- Tempos de espera
- Estrutura dos dados
- Caminhos do banco

## 🐛 Troubleshooting

### Problemas Comuns

**ChromeDriver não encontrado**:
```bash
# Instale webdriver-manager (já incluído em requirements.txt)
pip install webdriver-manager
```

**Problemas de permissão no Linux**:
```bash
sudo chmod +x /usr/bin/chromedriver
```

**Timeout no scraping**:
- Verifique sua conexão com a internet
- Aumente o timeout em `config.py`

### Logs e Debug

O sistema inclui logging detalhado. Para ativar modo debug:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Métricas e Estatísticas

O sistema coleta automaticamente:
- Frequência de cada animal
- Padrões numéricos
- Distribuição por horário
- Tendências temporais

## 🔧 Desenvolvimento

### Adicionando Novas Funcionalidades

1. **Novos módulos**: Crie arquivos `.py` separados
2. **Configurações**: Adicione constantes em `config.py`
3. **Banco de dados**: Use as funções em `database.py`
4. **Testes**: Adicione casos em `test_funcional.py`

### Padrões de Código

- Use type hints em todas as funções
- Documente com docstrings
- Siga PEP 8
- Adicione testes unitários

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

## 🙏 Agradecimentos

- [Selenium](https://selenium-python.readthedocs.io/) - Web scraping
- [Pandas](https://pandas.pydata.org/) - Análise de dados
- [Matplotlib](https://matplotlib.org/) - Visualizações
- [SQLite](https://sqlite.org/) - Banco de dados

---

**⚠️ Aviso**: Este projeto é para fins educacionais e de análise estatística. O Jogo do Bicho é uma atividade ilegal em muitas jurisdições. Use responsavelmente.
