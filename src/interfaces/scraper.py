# src/interfaces/scraper.py
from abc import ABC, abstractmethod
from typing import List, Tuple

class WebScraper(ABC):
    """Interface para implementação de web scrapers."""
    
    @abstractmethod
    def acessar_pagina_inicial(self) -> None:
        """Acessa a página inicial do sistema."""
        pass

    @abstractmethod
    def obter_unidades(self) -> List[Tuple[str, str]]:
        """
        Obtém a lista de unidades disponíveis.
        
        Returns:
            Lista de tuplas (código, nome) das unidades.
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