# USP Cursos Scraper

Este projeto coleta dados dos cursos de graduação da USP a partir do sistema JúpiterWeb, usando Selenium WebDriver e BeautifulSoup para automatizar a navegação e extrair as informações de grade curricular.

## 🔧 Tecnologias usadas

- Python 3
- Selenium
- BeautifulSoup (bs4)
- ChromeDriver (instalado automaticamente)

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
    
    python main.py
    

⚠️ *O programa utiliza o modo headless, então o Chrome não será exibido visualmente.*


## 📌 Objetivo

Navegar por todas as unidades e cursos da USP, acessando a aba "Grade Curricular" de cada curso e extraindo os dados das disciplinas oferecidas.

## ✅ Funcionalidades implementadas

- Acesso automático à página inicial do JúpiterWeb
- Seleção de unidades via menu suspenso
- Extração da lista de cursos e suas respectivas grades curriculares (em andamento)

## 📄 Licença

Este projeto está licenciado sob a licença MIT.
