from dataclasses import dataclass, field
from typing import List, Tuple
from .disciplina import Disciplina

@dataclass
class GradeCurricular:
    """
    Representa uma grade curricular com suas disciplinas.
    
    Attributes:
        obrigatorias: Lista de disciplinas obrigatórias
        optativas_livres: Lista de disciplinas optativas livres
        optativas_eletivas: Lista de disciplinas optativas eletivas
    """
    obrigatorias: List[Disciplina] = field(default_factory=list)
    optativas_livres: List[Disciplina] = field(default_factory=list)
    optativas_eletivas: List[Disciplina] = field(default_factory=list)

    def adicionar_disciplina(self, disciplina: Disciplina, tipo: str) -> None:
        """
        Adiciona uma disciplina à lista apropriada.
        
        Args:
            disciplina: Disciplina a ser adicionada
            tipo: Tipo da disciplina ('obrigatoria', 'optativa_livre' ou 'optativa_eletiva')
        """
        if tipo == "obrigatoria":
            self.obrigatorias.append(disciplina)
        elif tipo == "optativa_livre":
            self.optativas_livres.append(disciplina)
        elif tipo == "optativa_eletiva":
            self.optativas_eletivas.append(disciplina)

    def get_todas_disciplinas(self) -> Tuple[List[Disciplina], List[Disciplina], List[Disciplina]]:
        """
        Retorna todas as disciplinas separadas por tipo.
        
        Returns:
            Tupla contendo as listas de disciplinas (obrigatórias, optativas livres, optativas eletivas)
        """
        return self.obrigatorias, self.optativas_livres, self.optativas_eletivas