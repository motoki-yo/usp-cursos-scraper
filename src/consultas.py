from typing import List
from src.models import Unidade
from collections import defaultdict

class ConsultasJupiter:
    def __init__(self, unidades: List[Unidade]):
        self.unidades = unidades
        
    def listar_todas_unidades(self):
        """Lista todas as unidades coletadas."""
        print("\nUnidades disponíveis:")
        for unidade in self.unidades:
            print(f"- {unidade.nome}")

    def listar_cursos_por_unidade(self, nome_unidade: str):
        """Lista todos os cursos de uma unidade específica."""
        nome_unidade = nome_unidade.lower()
        for unidade in self.unidades:
            if unidade.nome.lower() == nome_unidade:
                print(f"\nCursos da unidade {unidade.nome}:")
                for curso in unidade.cursos:
                    print(f"- {curso.nome}")
                return
        print("\nUnidade não encontrada.")

    def detalhar_curso(self, nome_curso: str):
        """Mostra informações detalhadas de um curso específico."""
        nome_curso = nome_curso.lower()
        for unidade in self.unidades:
            for curso in unidade.cursos:
                if curso.nome.lower() == nome_curso:
                    print(f"\nDetalhes do curso: {curso.nome}")
                    print(f"Unidade: {curso.unidade}")
                    print(f"Duração: {curso.duracao_minima} a {curso.duracao_maxima} semestres (ideal: {curso.duracao_ideal})")
                    print("\nDisciplinas obrigatórias:")
                    for disc in curso.obrigatorias:
                        print(f"- {disc.codigo}: {disc.nome}")
                    print("\nDisciplinas optativas livres:")
                    for disc in curso.optativas_livres:
                        print(f"- {disc.codigo}: {disc.nome}")
                    print("\nDisciplinas optativas eletivas:")
                    for disc in curso.optativas_eletivas:
                        print(f"- {disc.codigo}: {disc.nome}")
                    return
        print("\nCurso não encontrado.")

    def buscar_disciplina(self, codigo: str):
        """Busca uma disciplina específica e mostra em quais cursos ela aparece."""
        codigo = codigo.upper()
        cursos_encontrados = list()
        
        for unidade in self.unidades:
            for curso in unidade.cursos:
                for lista in [curso.obrigatorias, curso.optativas_livres, curso.optativas_eletivas]:
                    for disciplina in lista:
                        if disciplina.codigo == codigo:
                            cursos_encontrados.append((disciplina, curso))

        if not cursos_encontrados:
            print("\nDisciplina não encontrada.")
        else:
            disc = cursos_encontrados[0][0]
            print(f"\nDisciplina {codigo}:")
            print(f"Nome: {disc.nome}")
            print(f"Créditos aula: {disc.creditos_aula}")
            print(f"Créditos trabalho: {disc.creditos_trabalho}")
            print(f"Carga horária: {disc.carga_horaria}")
            print("\nPresente nos cursos:")
            for _, curso in cursos_encontrados:
                print(f"- {curso.nome} ({curso.unidade})")

    def listar_disciplinas_comuns(self):
        """Lista disciplinas que aparecem em mais de um curso."""
        mapa = defaultdict(list)
        
        for unidade in self.unidades:
            for curso in unidade.cursos:
                for lista in [curso.obrigatorias, curso.optativas_livres, curso.optativas_eletivas]:
                    for disc in lista:
                        mapa[disc.codigo].append((disc, curso))

        print("\nDisciplinas presentes em mais de um curso:")
        for codigo, ocorrencias in mapa.items():
            if len(ocorrencias) > 1:
                disc = ocorrencias[0][0]
                print(f"\n{codigo} - {disc.nome}")
                print("Presente nos cursos:")
                for _, curso in ocorrencias:
                    print(f"- {curso.nome} ({curso.unidade})")

    def executar_menu(self):
        """Executa o menu interativo de consultas."""
        while True:
            print("\n==== MENU DE CONSULTAS ====")
            print("1. Listar todas as unidades")
            print("2. Listar cursos por unidade")
            print("3. Ver detalhes de um curso")
            print("4. Buscar disciplina por código")
            print("5. Listar disciplinas comuns a mais de um curso")
            print("6. Sair")

            try:
                opcao = input("\nEscolha uma opção: ")

                if opcao == "1":
                    self.listar_todas_unidades()
                elif opcao == "2":
                    nome = input("Nome da unidade: ")
                    self.listar_cursos_por_unidade(nome)
                elif opcao == "3":
                    nome = input("Nome do curso: ")
                    self.detalhar_curso(nome)
                elif opcao == "4":
                    codigo = input("Código da disciplina: ")
                    self.buscar_disciplina(codigo)
                elif opcao == "5":
                    self.listar_disciplinas_comuns()
                elif opcao == "6":
                    print("\nEncerrando consultas...")
                    break
                else:
                    print("\nOpção inválida!")
            except Exception as e:
                print(f"\nErro ao executar consulta: {e}")