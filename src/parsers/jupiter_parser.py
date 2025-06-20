from typing import Tuple, List, Optional
from bs4 import BeautifulSoup, Tag
from ..interfaces.parser import Parser
from ..models.disciplina import Disciplina
from ..models.duracao_curso import DuracaoCurso
from ..models.grade_curricular import GradeCurricular

class JupiterParser(Parser):
    """
    Parser para extrair informações das páginas do Jupiter.
    
    Implementa a interface Parser para processar o HTML das páginas
    do sistema Jupiter e extrair as informações necessárias.
    """

    def extrair_duracoes(self, html: str) -> DuracaoCurso:
        """
        Extrai as durações do curso do HTML.
        
        Args:
            html: Código HTML da página
            
        Returns:
            Objeto DuracaoCurso com as durações extraídas
            
        Raises:
            ValueError: Se não for possível encontrar as informações de duração
        """
        soup = BeautifulSoup(html, "html.parser")
        try:
            ideal = int(soup.find("span", class_="duridlhab").text)
            minima = int(soup.find("span", class_="durminhab").text)
            maxima = int(soup.find("span", class_="durmaxhab").text)
            
            return DuracaoCurso(
                ideal=ideal,
                minima=minima,
                maxima=maxima
            )
        except (AttributeError, ValueError) as e:
            print(f"Erro ao extrair durações: {e}")
            # Valores padrão em caso de erro
            return DuracaoCurso(ideal=8, minima=8, maxima=12)

    def extrair_disciplinas(self, html: str) -> Tuple[List[Disciplina], List[Disciplina], List[Disciplina]]:
        """
        Extrai as disciplinas do HTML e as organiza por tipo.
        
        Args:
            html: Código HTML da página
            
        Returns:
            Tupla contendo três listas de disciplinas (obrigatórias, optativas livres, optativas eletivas)
        """
        soup = BeautifulSoup(html, "html.parser")
        grade = GradeCurricular()
        
        div_grade = soup.find("div", id="gradeCurricular")
        if not div_grade:
            return grade.get_todas_disciplinas()

        tipo_atual = None
        
        for linha in div_grade.find_all("tr"):
            # Determinar o tipo de disciplina
            tipo_atual = self._identificar_tipo_disciplina(linha, tipo_atual)
            if not tipo_atual or "Semestre Ideal" in linha.get_text():
                continue
            
            # Tentar criar disciplina da linha atual
            disciplina = self._criar_disciplina_da_linha(linha)
            if disciplina:
                grade.adicionar_disciplina(disciplina, tipo_atual)
        
        return grade.get_todas_disciplinas()

    def _identificar_tipo_disciplina(self, linha: Tag, tipo_atual: str) -> str:
        """
        Identifica o tipo de disciplina com base no texto da linha.
        
        Args:
            linha: Linha da tabela HTML
            tipo_atual: Tipo atual de disciplina sendo processado
            
        Returns:
            Novo tipo de disciplina ou tipo atual se não houver mudança
        """
        texto = linha.get_text(strip=True)
        if "Disciplinas Obrigatórias" in texto:
            return "obrigatoria"
        elif "Disciplinas Optativas Livres" in texto:
            return "optativa_livre"
        elif "Disciplinas Optativas Eletivas" in texto:
            return "optativa_eletiva"
        return tipo_atual

    def _criar_disciplina_da_linha(self, linha: Tag) -> Optional[Disciplina]:
        """
        Cria um objeto Disciplina a partir de uma linha da tabela.
        
        Args:
            linha: Linha da tabela HTML
            
        Returns:
            Objeto Disciplina ou None se não for possível criar
        """
        try:
            colunas = linha.find_all("td")
            if len(colunas) < 8:
                return None

            codigo_elem = colunas[0].find("a", class_="disciplina")
            if not codigo_elem:
                return None

            return Disciplina(
                codigo=codigo_elem.get("data-coddis"),
                nome=colunas[1].get_text(strip=True),
                creditos_aula=int(colunas[2].get_text(strip=True) or 0),
                creditos_trabalho=int(colunas[3].get_text(strip=True) or 0),
                carga_horaria=int(colunas[4].get_text(strip=True) or 0),
                carga_estagio=int(colunas[5].get_text(strip=True) or 0),
                carga_praticas=int(colunas[6].get_text(strip=True) or 0),
                atividades_aprofundamento=int(colunas[7].get_text(strip=True) or 0)
            )
        except Exception as e:
            print(f"Erro ao criar disciplina: {e}")
            return None