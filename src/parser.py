from bs4 import BeautifulSoup
from src.models import Disciplina


def extrair_disciplinas(html):
    soup = BeautifulSoup(html, "html.parser")

    # Procurar a tabela que geralmente tem atributo border="1"
    tabela = soup.find("table", attrs={"border": "1"})
    if not tabela:
        print("Tabela de disciplinas não encontrada.")
        return []

    disciplinas = []
    linhas = tabela.find_all("tr")

    # Pular cabeçalho (assumindo que a primeira linha é cabeçalho)
    for linha in linhas[1:]:
        colunas = linha.find_all("td")
        if len(colunas) < 7:
            continue
        try:
            codigo = colunas[0].get_text(strip=True)
            nome = colunas[1].get_text(strip=True)
            creditos_aula = int(colunas[2].get_text(strip=True) or 0)
            creditos_trabalho = int(colunas[3].get_text(strip=True) or 0)
            carga_horaria = int(colunas[4].get_text(strip=True) or 0)
            carga_estagio = int(colunas[5].get_text(strip=True) or 0)
            carga_praticas = int(colunas[6].get_text(strip=True) or 0)
            atividades_aprofundamento = 0
            if len(colunas) > 7:
                atividades_aprofundamento = int(colunas[7].get_text(strip=True) or 0)

            disc = Disciplina(
                codigo,
                nome,
                creditos_aula,
                creditos_trabalho,
                carga_horaria,
                carga_estagio,
                carga_praticas,
                atividades_aprofundamento,
            )
            disciplinas.append(disc)
        except Exception as e:
            print(f"Erro ao processar linha: {e}")

    return disciplinas