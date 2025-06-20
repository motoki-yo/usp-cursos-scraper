from dataclasses import dataclass, field
from typing import List, Optional
from .curso import Curso

@dataclass
class Unidade:
    """
    Representa uma unidade acadêmica.
    
    Attributes:
        nome: Nome da unidade
        cursos: Lista de cursos oferecidos pela unidade
    """
    nome: str
    cursos: List[Curso] = field(default_factory=list)

    def adicionar_curso(self, curso: Curso) -> None:
        """
        Adiciona um novo curso à unidade.
        
        Args:
            curso: Curso a ser adicionado
        """
        self.cursos.append(curso)

    def buscar_curso(self, nome: str) -> Optional[Curso]:
        """
        Busca um curso pelo nome.
        
        Args:
            nome: Nome do curso a ser buscado
            
        Returns:
            Curso encontrado ou None se não encontrar
        """
        nome = nome.lower()
        return next((c for c in self.cursos if c.nome.lower() == nome), None)

    def __str__(self) -> str:
        return self.nome