from dataclasses import dataclass

@dataclass
class Disciplina:
    """
    Representa uma disciplina acadêmica.
    
    Attributes:
        codigo: Código único da disciplina
        nome: Nome da disciplina
        creditos_aula: Número de créditos em aula
        creditos_trabalho: Número de créditos em trabalho
        carga_horaria: Carga horária total
        carga_estagio: Carga horária de estágio
        carga_praticas: Carga horária de práticas
        atividades_aprofundamento: Horas de atividades de aprofundamento
    """
    codigo: str
    nome: str
    creditos_aula: int
    creditos_trabalho: int
    carga_horaria: int
    carga_estagio: int
    carga_praticas: int
    atividades_aprofundamento: int

    @property
    def creditos_totais(self) -> int:
        """Retorna o total de créditos da disciplina."""
        return self.creditos_aula + self.creditos_trabalho

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nome}"