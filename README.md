# USP Cursos Scraper

### Alunos: 
    Guilherme Sousa Panza
    Melissa Motoki Nogueira
Este projeto coleta dados dos cursos de graduação da USP a partir do sistema JúpiterWeb, usando Selenium WebDriver para automação da navegação e extração das informações de grade curricular. Também conta com interface interativa no terminal usando Rich e Questionary.

## 🔧 Tecnologias usadas

- Python 3
- Selenium
- Rich (para interface de terminal)
- Questionary (para prompts interativos)
- BeautifulSoup (bs4) — usado no parser
- ChromeDriver (instalado automaticamente pelo chromedriver_autoinstaller)

## 🚀 Como executar

### 1. **Clonar o repositório**
    
    git clone https://github.com/seu-usuario/usp-cursos-scraper.git
    cd usp-cursos-scraper
    

### 2. **Criar ambiente virtual (opcional, mas recomendado)**

    python3 -m venv venv
    source venv/bin/activate
    

### 3. **Instalar as dependências**
   
    pip install -r requirements.txt
    

### 4. **Executar o programa**
    
    python main.py NUMERO_DE_UNIDADES [--headless]

NUMERO_DE_UNIDADES: quantidade de unidades USP a serem coletadas (e.g. python main.py 3 - coleta dados de três unidades)
--headless (opcional): executa o navegador em modo headless (sem interface gráfica)
    

## 📌 Objetivo

Navegar automaticamente por todas as unidades e cursos da USP, acessando a aba "Grade Curricular" de cada curso e extraindo os dados das disciplinas oferecidas. Permite consulta interativa dos dados coletados via terminal.

## ✅ Funcionalidades implementadas

- Acesso automático à página inicial do JúpiterWeb
- Seleção dinâmica de unidades e cursos via Selenium
- Extração detalhada das grades curriculares dos cursos
- Interface de menu interativa com opções de consulta e análise dos dados
- Barra de progresso visual durante a coleta com Rich
- Limpeza da tela para melhor usabilidade no terminal
- Execução opcional em modo headless

## 📄 Licença

Este projeto está licenciado sob a licença MIT.
