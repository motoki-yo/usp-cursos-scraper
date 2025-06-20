from dataclasses import dataclass, field
from typing import List, Optional
from .disciplina import Disciplina
from .duracao_curso import DuracaoCurso

@dataclass
class Curso:
    """
    Representa um curso acadêmico.
    
    Attributes:
        nome: Nome do curso
        unidade: Nome da unidade que oferece o curso
        duracao: Objeto contendo as durações do curso
        obrigatorias: Lista de disciplinas obrigatórias
        optativas_livres: Lista de disciplinas optativas livres
        optativas_eletivas: Lista de disciplinas optativas eletivas
    """
    nome: str
    unidade: str
    duracao: DuracaoCurso
    obrigatorias: List[Disciplina] = field(default_factory=list)
    optativas_livres: List[Disciplina] = field(default_factory=list)
    optativas_eletivas: List[Disciplina] = field(default_factory=list)

    @property
    def todas_disciplinas(self) -> List[Disciplina]:
        """Retorna uma lista com todas as disciplinas do curso."""
        return self.obrigatorias + self.optativas_livres + self.optativas_eletivas

    def buscar_disciplina(self, codigo: str) -> Optional[Disciplina]:
        """
        Busca uma disciplina pelo código.
        
        Args:
            codigo: Código da disciplina a ser buscada
            
        Returns:
            Disciplina encontrada ou None se não encontrar
        """
        return next((d for d in self.todas_disciplinas if d.codigo == codigo), None)

    def __str__(self) -> str:
        return f"{self.nome} ({self.unidade})"