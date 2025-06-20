# src/interfaces/parser.py
from abc import ABC, abstractmethod
from typing import Tuple, List
from ..models.disciplina import Disciplina
from ..models.duracao_curso import DuracaoCurso

class Parser(ABC):
    """Interface para implementação de parsers de HTML."""
    
    @abstractmethod
    def extrair_duracoes(self, html: str) -> DuracaoCurso:
        """
        Extrai as informações de duração do curso do HTML.
        
        Args:
            html: Código HTML da página.
            
        Returns:
            Objeto DuracaoCurso com as durações extraídas.
        """
        pass

    @abstractmethod
    def extrair_disciplinas(self, html: str) -> Tuple[List[Disciplina], List[Disciplina], List[Disciplina]]:
        """
        Extrai as disciplinas do HTML, separando-as por tipo.
        
        Args:
            html: Código HTML da página.
            
        Returns:
            Tupla contendo três listas:
            - Lista de disciplinas obrigatórias
            - Lista de disciplinas optativas livres
            - Lista de disciplinas optativas eletivas
        """
        pass