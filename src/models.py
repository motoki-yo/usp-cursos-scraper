from typing import List

class Disciplina:
    def __init__(
        self,
        codigo: str,
        nome: str,
        creditos_aula: int,
        creditos_trabalho: int,
        carga_horaria: int,
        carga_estagio: int,
        carga_praticas: int,
        atividades_aprofundamento: int
    ):
        self.codigo = codigo
        self.nome = nome
        self.creditos_aula = creditos_aula
        self.creditos_trabalho = creditos_trabalho
        self.carga_horaria = carga_horaria
        self.carga_estagio = carga_estagio
        self.carga_praticas = carga_praticas
        self.atividades_aprofundamento = atividades_aprofundamento

    def __repr__(self):
        return f"Disciplina({self.codigo}, {self.nome})"


class Curso:
    def __init__(
        self,
        nome: str,
        unidade: str,
        duracao_ideal: int,
        duracao_minima: int,
        duracao_maxima: int,
        obrigatorias: List[Disciplina],
        optativas_livres: List[Disciplina],
        optativas_eletivas: List[Disciplina]
    ):
        self.nome = nome
        self.unidade = unidade
        self.duracao_ideal = duracao_ideal
        self.duracao_minima = duracao_minima
        self.duracao_maxima = duracao_maxima
        self.obrigatorias = obrigatorias
        self.optativas_livres = optativas_livres
        self.optativas_eletivas = optativas_eletivas

    def __repr__(self):
        return f"Curso({self.nome})"


class Unidade:
    def __init__(self, nome: str, cursos: List[Curso]):
        self.nome = nome
        self.cursos = cursos

    def __repr__(self):
        return f"Unidade({self.nome})"
