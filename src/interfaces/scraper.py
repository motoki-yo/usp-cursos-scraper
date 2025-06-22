from abc import ABC, abstractmethod
from typing import List, Tuple

class WebScraper(ABC):
    """Interface para implementação de web scrapers."""
    
    @abstractmethod
    def acessar_pagina_inicial(self) -> None:
        """Acessa a página inicial do sistema."""
        pass

    @abstractmethod
    def listar_unidades_urls(self) -> List[str]:
        """
        Obtém a lista de URLs das unidades disponíveis para coleta.

        Returns:
            Lista de URLs para cada unidade.
        """
        pass

    @abstractmethod
    def obter_html(self, url: str) -> str:
        """
        Obtém o HTML bruto da página dada a URL.

        Args:
            url: URL da página a ser obtida.

        Returns:
            Conteúdo HTML da página.
        """
        pass

    @abstractmethod
    def selecionar_unidade(self, codigo: str) -> None:
        """
        Seleciona uma unidade específica.
        
        Args:
            codigo: Código da unidade a ser selecionada.
        """
        pass

    @abstractmethod
    def obter_cursos(self) -> List[Tuple[str, str]]:
        """
        Obtém a lista de cursos da unidade selecionada.
        
        Returns:
            Lista de tuplas (código, nome) dos cursos.
        """
        pass

    @abstractmethod
    def acessar_grade_curso(self, codigo_curso: str) -> str:
        """
        Acessa a grade curricular de um curso específico.
        
        Args:
            codigo_curso: Código do curso.
            
        Returns:
            HTML da página da grade curricular.
        """
        pass

    @abstractmethod
    def fechar(self) -> None:
        """Fecha o navegador e libera recursos."""
        pass