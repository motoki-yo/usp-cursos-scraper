from typing import List, Optional
from ..interfaces.scraper import WebScraper
from ..interfaces.parser import Parser
from ..models.unidade import Unidade
from ..models.curso import Curso
from ..models.duracao_curso import DuracaoCurso

class ColetaService:
    """
    Serviço responsável pela coleta de dados do sistema Jupiter.
    
    Coordena o processo de coleta de dados utilizando o scraper e o parser.
    
    Attributes:
        scraper: Implementação de WebScraper para coletar dados
        parser: Implementação de Parser para processar os dados
    """

    def __init__(self, scraper: WebScraper, parser: Parser):
        self.scraper = scraper
        self.parser = parser

    def coletar_dados(self, quantidade_unidades: int) -> List[Unidade]:
        """
        Coleta dados das unidades e seus cursos.
        
        Args:
            quantidade_unidades: Número de unidades a serem coletadas
            
        Returns:
            Lista de unidades com seus respectivos cursos
        """
        try:
            self.scraper.acessar_pagina_inicial()
            unidades_disponiveis = self.scraper.obter_unidades()
            unidades_coletadas = []

            for i, (codigo, nome_unidade) in enumerate(unidades_disponiveis):
                if i >= quantidade_unidades:
                    break
                    
                print(f"Coletando unidade {nome_unidade} ({i+1}/{quantidade_unidades})")
                unidade = self._coletar_unidade(codigo, nome_unidade)
                if unidade.cursos:  # Só adiciona se tiver cursos
                    unidades_coletadas.append(unidade)

            return unidades_coletadas
        finally:
            self.scraper.fechar()

    def _coletar_unidade(self, codigo: str, nome: str) -> Unidade:
        """
        Coleta dados de uma unidade específica.
        
        Args:
            codigo: Código da unidade
            nome: Nome da unidade
            
        Returns:
            Objeto Unidade com seus cursos
        """
        self.scraper.selecionar_unidade(codigo)
        cursos = self._coletar_cursos(nome, codigo)
        return Unidade(nome=nome, cursos=cursos)
    
    def _coletar_cursos(self, nome_unidade: str, codigo_unidade: str) -> List[Curso]:
        """
        Coleta dados dos cursos de uma unidade.
        
        Args:
            nome_unidade: Nome da unidade
            codigo_unidade: Código da unidade
        """
        cursos = []
        cursos_lista = self.scraper.obter_cursos()
        
        for codigo_curso, nome_curso in cursos_lista:
            print(f"  Coletando curso {nome_curso}")
            try:
                curso = self._coletar_curso(codigo_curso, nome_curso, nome_unidade)
                if curso:
                    cursos.append(curso)
                
                self.scraper.acessar_pagina_inicial()
                self.scraper.selecionar_unidade(codigo_unidade)
                
            except Exception as e:
                print(f"Erro ao coletar curso {nome_curso}: {e}")
                continue
                
        return cursos

    def _coletar_curso(self, codigo: str, nome: str, nome_unidade: str) -> Optional[Curso]:
        """
        Coleta dados de um curso específico.
        """
        try:
            html_grade = self.scraper.acessar_grade_curso(codigo)
            if not html_grade:
                print(f"  Aviso: Grade curricular não disponível para o curso {nome}")
                return None
                
            duracao = self.parser.extrair_duracoes(html_grade)
            obrigatorias, optativas_livres, optativas_eletivas = self.parser.extrair_disciplinas(html_grade)
            
            return Curso(
                nome=nome,
                unidade=nome_unidade,
                duracao=duracao,
                obrigatorias=obrigatorias,
                optativas_livres=optativas_livres,
                optativas_eletivas=optativas_eletivas
            )
        except Exception as e:
            print(f"Erro ao processar curso {nome}: {e}")
            return None