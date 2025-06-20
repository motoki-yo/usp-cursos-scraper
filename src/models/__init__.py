"""
Módulo de modelos de dados.

Contém as classes que representam as entidades do sistema.
"""

from .curso import Curso
from .disciplina import Disciplina
from .duracao_curso import DuracaoCurso
from .grade_curricular import GradeCurricular
from .unidade import Unidade

__all__ = [
    'Curso',
    'Disciplina',
    'DuracaoCurso',
    'GradeCurricular',
    'Unidade'
]