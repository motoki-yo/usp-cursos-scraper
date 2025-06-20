from bs4 import BeautifulSoup
from src.models import Disciplina

class JupiterParser:
    @staticmethod
    def extrair_disciplinas(html: str):
        soup = BeautifulSoup(html, "html.parser")
        disciplinas = list()
        
        div_grade = soup.find("div", id="gradeCurricular")
        if not div_grade:
            return list()

        tabelas = div_grade.find_all("table")
        
        for tabela in tabelas:
            tipo_header = tabela.find("tr")
            if not tipo_header:
                continue
                
            for linha in tabela.find_all("tr"):
                if "Semestre Ideal" in linha.get_text() or "Disciplinas" in linha.get_text():
                    continue
                    
                colunas = linha.find_all("td")
                if len(colunas) < 8:
                    continue
                    
                try:
                    codigo_elem = colunas[0].find("a", class_="disciplina")
                    if not codigo_elem:
                        continue
                        
                    codigo = codigo_elem.get("data-coddis")
                    nome = colunas[1].get_text(strip=True)
                    
                    creditos_aula = int(colunas[2].get_text(strip=True) or 0)
                    creditos_trabalho = int(colunas[3].get_text(strip=True) or 0)
                    carga_horaria = int(colunas[4].get_text(strip=True) or 0)
                    carga_estagio = int(colunas[5].get_text(strip=True) or 0)
                    carga_praticas = int(colunas[6].get_text(strip=True) or 0)
                    atividades_aprofundamento = int(colunas[7].get_text(strip=True) or 0)
                    
                    disc = Disciplina(
                        codigo, nome, creditos_aula, creditos_trabalho,
                        carga_horaria, carga_estagio, carga_praticas,
                        atividades_aprofundamento
                    )
                    disciplinas.append(disc)
                    
                except Exception as e:
                    print(f"Erro ao processar disciplina: {e}")
                    continue
        
        return disciplinas