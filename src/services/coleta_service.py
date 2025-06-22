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

    def coletar_dados(
        self,
        quantidade: int,
        progress: Optional["Progress"] = None,
        task_id: Optional[int] = None
    ) -> List[Unidade]:
        """
        Coleta dados do Jupiter Web para um número especificado de unidades.

        Args:
            quantidade: Número de unidades a coletar.
            progress: Objeto de progresso do Rich (opcional).
            task_id: ID da tarefa de progresso (opcional).

        Returns:
            Lista de objetos Unidade com cursos e disciplinas preenchidos.
        """
        # Obtem os códigos das unidades (não URLs)
        codigos_unidades = self.scraper.listar_unidades_urls()[:quantidade]
        unidades: List[Unidade] = []

        for codigo_unidade in codigos_unidades:
            # Para cada unidade, coleta os dados detalhados (com cursos)
            try:
                # Aqui coletamos a unidade com seus cursos
                unidade = self._coletar_unidade_por_codigo(codigo_unidade, progress, task_id)
                unidades.append(unidade)
            except Exception as e:
                print(f"Erro ao coletar unidade {codigo_unidade}: {e}")
                continue

            # Atualiza progresso por unidade coletada
            if progress and task_id is not None:
                progress.update(task_id, advance=1)

        return unidades

    def _coletar_unidade_por_codigo(
        self,
        codigo: str,
        progress: Optional["Progress"] = None,
        task_id: Optional[int] = None
    ) -> Unidade:
        """
        Coleta dados de uma unidade específica dado seu código.
        
        Args:
            codigo: Código da unidade
            progress: Objeto de progresso (opcional)
            task_id: ID da tarefa de progresso (opcional)
            
        Returns:
            Objeto Unidade com seus cursos coletados
        """
        # Acessa a página inicial e seleciona a unidade pelo código
        self.scraper.acessar_pagina_inicial()
        self.scraper.selecionar_unidade(codigo)
        
        # Obtem o nome da unidade (por exemplo, via lista de unidades)
        lista_unidades = self.scraper.obter_unidades()
        nome = next((nome for cod, nome in lista_unidades if cod == codigo), "Unidade Desconhecida")
        
        # Coleta os cursos da unidade
        cursos = self._coletar_cursos(nome, codigo, progress, task_id)
        
        return Unidade(nome=nome, cursos=cursos)
    
    def _coletar_cursos(
        self,
        nome_unidade: str,
        codigo_unidade: str,
        progress: Optional["Progress"] = None,
        task_id: Optional[int] = None
    ) -> List[Curso]:
        """
        Coleta dados dos cursos de uma unidade.
        
        Args:
            nome_unidade: Nome da unidade
            codigo_unidade: Código da unidade
            progress: Objeto de progresso (opcional)
            task_id: ID da tarefa de progresso (opcional)
        """
        cursos = []
        cursos_lista = self.scraper.obter_cursos()
        
        for codigo_curso, nome_curso in cursos_lista:
            print(f"  Coletando curso {nome_curso}")
            try:
                curso = self._coletar_curso(codigo_curso, nome_curso, nome_unidade)
                if curso:
                    cursos.append(curso)

                if progress and task_id is not None:
                    progress.update(task_id, advance=1)
                
                # Após coletar o curso, retorna para a página da unidade para continuar
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