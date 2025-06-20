from dataclasses import dataclass

@dataclass
class DuracaoCurso:
    """
    Representa as durações de um curso.
    
    Attributes:
        ideal: Duração ideal em semestres
        minima: Duração mínima em semestres
        maxima: Duração máxima em semestres
    """
    ideal: int
    minima: int
    maxima: int

    def __str__(self) -> str:
        return f"{self.minima} a {self.maxima} semestres (ideal: {self.ideal})"