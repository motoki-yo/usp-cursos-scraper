import sys
from src.navigator import (
    iniciar_driver,
    acessar_jupiter,
    obter_unidades,
    selecionar_unidade,
    obter_cursos,
    selecionar_curso,
    clicar_buscar,
    acessar_aba_grade_curricular,
    obter_html_grade,
)
from src.parser import extrair_disciplinas
from src.models import Unidade, Curso
from typing import List


def coletar_dados(quantidade_unidades: int) -> List[Unidade]:
    driver = iniciar_driver(headless=False)
    acessar_jupiter(driver)
    unidades_disponiveis = obter_unidades(driver)
    unidades_coletadas = []

    for i, (codigo, nome_unidade) in enumerate(unidades_disponiveis):
        if i >= quantidade_unidades:
            break
        print(f"Coletando unidade {nome_unidade} ({i+1}/{quantidade_unidades})")

        selecionar_unidade(driver, codigo)
        cursos_lista = obter_cursos(driver)

        cursos_obj = []
        for codigo_curso, nome_curso in cursos_lista:
            print(f"  Coletando curso {nome_curso}")
            selecionar_curso(driver, codigo_curso)
            clicar_buscar(driver)

            sucesso = acessar_aba_grade_curricular(driver)
            if not sucesso:
                print(f"    Falha ao acessar grade curricular do curso {nome_curso}")
                continue

            html_grade = obter_html_grade(driver)
            disciplinas = extrair_disciplinas(html_grade)

            # Valores padrão para durações
            duracao_ideal = 8
            duracao_minima = 6
            duracao_maxima = 12

            curso_obj = Curso(
                nome=nome_curso,
                unidade=nome_unidade,
                duracao_ideal=duracao_ideal,
                duracao_minima=duracao_minima,
                duracao_maxima=duracao_maxima,
                obrigatorias=disciplinas,
                optativas_livres=[],
                optativas_eletivas=[]
            )
            cursos_obj.append(curso_obj)

        unidade_obj = Unidade(nome=nome_unidade, cursos=cursos_obj)
        unidades_coletadas.append(unidade_obj)

        # Voltar para página inicial para escolher outra unidade
        acessar_jupiter(driver)

    driver.quit()
    return unidades_coletadas


def listar_todas_unidades(unidades: List[Unidade]):
    for unidade in unidades:
        print(f"- {unidade.nome}")


def listar_cursos_por_unidade(unidades: List[Unidade], nome_unidade: str):
    for unidade in unidades:
        if unidade.nome.lower() == nome_unidade.lower():
            print(f"Cursos da unidade {unidade.nome}:")
            for curso in unidade.cursos:
                print(f"- {curso.nome}")
            return
    print("Unidade não encontrada.")


def detalhar_curso(unidades: List[Unidade], nome_curso: str):
    for unidade in unidades:
        for curso in unidade.cursos:
            if curso.nome.lower() == nome_curso.lower():
                print(f"Curso: {curso.nome}")
                print(f"Unidade: {curso.unidade}")
                print(f"Duração: {curso.duracao_minima} a {curso.duracao_maxima} semestres (ideal: {curso.duracao_ideal})")
                print(f"Disciplinas obrigatórias ({len(curso.obrigatorias)}): {[d.nome for d in curso.obrigatorias]}")
                print(f"Disciplinas optativas livres ({len(curso.optativas_livres)}): {[d.nome for d in curso.optativas_livres]}")
                print(f"Disciplinas optativas eletivas ({len(curso.optativas_eletivas)}): {[d.nome for d in curso.optativas_eletivas]}")
                return
    print("Curso não encontrado.")


def buscar_disciplina_por_codigo(unidades: List[Unidade], codigo: str):
    cursos_encontrados = []
    for unidade in unidades:
        for curso in unidade.cursos:
            for lista in [curso.obrigatorias, curso.optativas_livres, curso.optativas_eletivas]:
                for disciplina in lista:
                    if disciplina.codigo.lower() == codigo.lower():
                        cursos_encontrados.append((disciplina, curso.nome))

    if not cursos_encontrados:
        print("Disciplina não encontrada.")
    else:
        print(f"Disciplina {codigo} encontrada em:")
        for disciplina, curso_nome in cursos_encontrados:
            print(f"- Curso: {curso_nome} | Nome: {disciplina.nome}")


def listar_disciplinas_comuns(unidades: List[Unidade]):
    from collections import defaultdict
    mapa = defaultdict(set)
    for unidade in unidades:
        for curso in unidade.cursos:
            for lista in [curso.obrigatorias, curso.optativas_livres, curso.optativas_eletivas]:
                for d in lista:
                    mapa[d.codigo].add(curso.nome)

    print("Disciplinas presentes em mais de um curso:")
    for cod, cursos in mapa.items():
        if len(cursos) > 1:
            print(f"{cod} -> {', '.join(cursos)}")


def menu(unidades: List[Unidade]):
    while True:
        print("\n==== MENU ====")
        print("1. Listar todas as unidades")
        print("2. Listar cursos por unidade")
        print("3. Ver detalhes de um curso")
        print("4. Buscar disciplina por código")
        print("5. Listar disciplinas comuns a mais de um curso")
        print("6. Sair")

        op = input("Escolha uma opção: ")

        if op == "1":
            listar_todas_unidades(unidades)
        elif op == "2":
            nome = input("Nome da unidade: ")
            listar_cursos_por_unidade(unidades, nome)
        elif op == "3":
            nome = input("Nome do curso: ")
            detalhar_curso(unidades, nome)
        elif op == "4":
            cod = input("Código da disciplina: ")
            buscar_disciplina_por_codigo(unidades, cod)
        elif op == "5":
            listar_disciplinas_comuns(unidades)
        elif op == "6":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <quantidade_unidades>")
        sys.exit(1)

    quantidade = int(sys.argv[1])
    print(f"Iniciando coleta de dados para {quantidade} unidades...")

    unidades = coletar_dados(quantidade)

    print("Coleta concluída. Iniciando menu interativo.")
    menu(unidades)