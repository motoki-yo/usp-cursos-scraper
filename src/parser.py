from bs4 import BeautifulSoup
import json

def extrair_grade_curricular(html):
    soup = BeautifulSoup(html, "html.parser")
    tabela = soup.find("table")  # ajustar o seletor conforme a estrutura
    linhas = tabela.find_all("tr")
    disciplinas = []

    for linha in linhas[1:]:  # pula cabeçalho
        colunas = linha.find_all("td")
        if len(colunas) > 1:
            cod = colunas[0].text.strip()
            nome = colunas[1].text.strip()
            disciplinas.append({"codigo": cod, "nome": nome})
    
    return disciplinas

def salvar_json(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)