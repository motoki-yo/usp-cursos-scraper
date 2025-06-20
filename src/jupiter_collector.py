from src.jupiter_scraper import JupiterScraper
from src.jupiter_parser import JupiterParser
from src.models import Unidade, Curso

class JupiterCollector:
    def __init__(self):
        self.scraper = JupiterScraper()
        self.parser = JupiterParser()
        
    def coletar_dados(self, quantidade_unidades: int):
        self.scraper.acessar_pagina_inicial()
        unidades_disponiveis = self.scraper.obter_unidades()
        unidades_coletadas = list()

        for i, (codigo, nome_unidade) in enumerate(unidades_disponiveis):
            if i >= quantidade_unidades:
                break
                
            print(f"Coletando unidade {nome_unidade} ({i+1}/{quantidade_unidades})")
            self.scraper.selecionar_unidade(codigo)
            
            cursos_lista = self.scraper.obter_cursos()
            cursos_obj = list()
            
            for codigo_curso, nome_curso in cursos_lista:
                print(f"  Coletando curso {nome_curso}")
                
                html_grade = self.scraper.acessar_grade_curso(codigo_curso)
                disciplinas = self.parser.extrair_disciplinas(html_grade)
                
                curso_obj = Curso(
                    nome=nome_curso,
                    unidade=nome_unidade,
                    duracao_ideal=8,
                    duracao_minima=6,
                    duracao_maxima=12,
                    obrigatorias=disciplinas,
                    optativas_livres=list(),
                    optativas_eletivas=list()
                )
                cursos_obj.append(curso_obj)
                
                self.scraper.acessar_pagina_inicial()
                self.scraper.selecionar_unidade(codigo)
                
            unidade_obj = Unidade(nome=nome_unidade, cursos=cursos_obj)
            unidades_coletadas.append(unidade_obj)
            
        self.scraper.fechar()
        return unidades_coletadas