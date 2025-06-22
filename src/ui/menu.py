import os
from typing import Callable, Dict
from colorama import init, Fore
import questionary
from ..services.consulta_service import ConsultaService

class Menu:
    """
    Interface de menu para interação com o usuário.

    Gerencia a exibição do menu e o processamento das opções escolhidas.

    Attributes:
        consulta_service: Serviço para realizar consultas nos dados
        opcoes: Dicionário de opções do menu e suas funções correspondentes
    """

    def __init__(self, consulta_service: ConsultaService):
        init(autoreset=True)
        self.consulta_service = consulta_service
        self.opcoes: Dict[str, Callable] = {
            "Listar todas as unidades": self._listar_unidades,
            "Listar cursos por unidade": self._listar_cursos_unidade,
            "Ver detalhes de um curso": self._detalhar_curso,
            "Buscar disciplina por código": self._buscar_disciplina,
            "Listar disciplinas comuns a mais de um curso": self._listar_disciplinas_comuns,
            "Analisar carga horária de um curso": self._analisar_carga_curso,
            "Comparar dois cursos": self._comparar_cursos,
            "Listar disciplinas por número mínimo de créditos": self._listar_disciplinas_por_creditos,
            "Analisar unidade": self._analisar_unidade,
            "Sair": self._sair
        }

    def limpar_console(self) -> None:
        """Limpa o console para melhor visualização."""
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # macOS e Linux
            os.system('clear')

    def executar(self) -> None:
        """Executa o loop principal do menu."""
        while True:
            opcao = questionary.select(
                "Escolha uma opção:",
                choices=list(self.opcoes.keys())
            ).ask()

            if opcao is None:
                print(Fore.RED + "\n❌ Encerrando...")
                break

            acao = self.opcoes.get(opcao)
            try:
                if acao() is False:
                    break
            except Exception as e:
                print(Fore.RED + f"\n❌ Erro: {e}")
            input(Fore.YELLOW + "\nPressione Enter para continuar...")
            
            # Limpa o console antes de mostrar o menu novamente
            self.limpar_console()

    def _listar_unidades(self) -> None:
        """Lista todas as unidades disponíveis."""
        print(Fore.BLUE + "\n🏢 Unidades disponíveis:")
        for nome in self.consulta_service.listar_unidades():
            print(f"- {nome}")

    def _listar_cursos_unidade(self) -> None:
        """Lista os cursos de uma unidade específica."""
        nome = questionary.text("Nome da unidade:").ask()
        dados = self.consulta_service.listar_cursos_por_unidade(nome)

        if not dados:
            print(Fore.RED + "\nUnidade não encontrada. Tente o nome completo ou a sigla (ex: EACH)")
            return

        _, cursos = dados
        print(Fore.BLUE + f"\n📘 Cursos da unidade {nome}:")
        for curso in cursos:
            print(f"- {curso}")

    def _detalhar_curso(self) -> None:
        """Mostra informações detalhadas de um curso."""
        cursos = self.consulta_service.listar_todos_cursos()
        if not cursos:
            print(Fore.RED + "\nNenhum curso disponível.")
            return

        nome = questionary.select("Selecione o curso:", choices=cursos).ask()
        curso = self.consulta_service.buscar_curso(nome)

        if curso:
            print(Fore.BLUE + f"\n📘 Curso: {curso.nome}")
            print(f"Unidade: {curso.unidade} | Duração: {curso.duracao}")

            print("\n📚 Obrigatórias:")
            for disc in curso.obrigatorias:
                print(f"- {disc}")

            print("\n✏️ Optativas livres:")
            for disc in curso.optativas_livres:
                print(f"- {disc}")

            print("\n🎯 Optativas eletivas:")
            for disc in curso.optativas_eletivas:
                print(f"- {disc}")
        else:
            print(Fore.RED + "\nCurso não encontrado.")

    def _buscar_disciplina(self) -> None:
        """Busca e exibe informações de uma disciplina."""
        codigos = self.consulta_service.listar_codigos_disciplinas()
        if not codigos:
            print(Fore.RED + "\nNenhuma disciplina cadastrada.")
            return

        codigo = questionary.select("Selecione o código da disciplina:", choices=codigos).ask()
        ocorrencias = self.consulta_service.buscar_disciplina(codigo)

        if ocorrencias:
            disc = ocorrencias[0][0]
            print(Fore.BLUE + f"\n📗 {codigo} - {disc.nome}")
            print(f"Créditos aula: {disc.creditos_aula} | Trabalho: {disc.creditos_trabalho} | Carga horária: {disc.carga_horaria}")
            print("\n📘 Presente nos cursos:")
            for _, curso in ocorrencias:
                print(f"- {curso}")
        else:
            print(Fore.RED + "\nDisciplina não encontrada.")

    def _listar_disciplinas_comuns(self) -> None:
        """Lista disciplinas que aparecem em mais de um curso."""
        comuns = self.consulta_service.listar_disciplinas_comuns()
        if comuns:
            print(Fore.BLUE + "\n🔁 Disciplinas presentes em mais de um curso:")
            for codigo, ocorrencias in comuns.items():
                disc = ocorrencias[0][0]
                print(Fore.YELLOW + f"\n{codigo} - {disc.nome}")
                for _, curso in ocorrencias:
                    print(f"  - {curso}")
        else:
            print(Fore.YELLOW + "\nNenhuma disciplina comum encontrada.")

    def _analisar_carga_curso(self) -> None:
        """Analisa e exibe a distribuição de carga horária de um curso."""
        cursos = self.consulta_service.listar_todos_cursos()
        if not cursos:
            print(Fore.RED + "\nNenhum curso disponível.")
            return

        nome = questionary.select("Selecione o curso:", choices=cursos).ask()
        dados = self.consulta_service.analisar_carga_curso(nome)

        if not dados:
            print(Fore.RED + "\nCurso não encontrado.")
            return

        print(Fore.BLUE + f"\n📊 Análise do curso {dados['nome']}:")
        print(f"Total de créditos: {dados['total_creditos']} | Carga horária total: {dados['total_ch']}h")
        print(f"Obrigatórias: {dados['qtd_obrigatorias']} | Optativas Livres: {dados['qtd_optativas_livres']} | Optativas Eletivas: {dados['qtd_optativas_eletivas']}")

    def _comparar_cursos(self) -> None:
        """Compara e exibe informações de dois cursos."""
        cursos = self.consulta_service.listar_todos_cursos()
        if len(cursos) < 2:
            print(Fore.RED + "\nÉ necessário pelo menos dois cursos para comparar.")
            return

        nome1 = questionary.select("Primeiro curso:", choices=cursos).ask()
        nome2 = questionary.select("Segundo curso:", choices=[c for c in cursos if c != nome1]).ask()

        resultado = self.consulta_service.comparar_cursos(nome1, nome2)
        if not resultado:
            print(Fore.RED + "\nUm ou ambos os cursos não encontrados.")
            return

        curso1, curso2 = resultado
        print(Fore.BLUE + f"\n📈 Comparação entre {curso1['nome']} e {curso2['nome']}:")
        print(f"{curso1['nome']}: {curso1['total_disciplinas']} disciplinas, {curso1['total_ch']}h")
        print(f"{curso2['nome']}: {curso2['total_disciplinas']} disciplinas, {curso2['total_ch']}h")

    def _listar_disciplinas_por_creditos(self) -> None:
        """Lista disciplinas filtradas por número mínimo de créditos."""
        try:
            min_creditos = int(questionary.text("Número mínimo de créditos:").ask())
        except ValueError:
            print(Fore.RED + "\nPor favor, insira um número válido.")
            return

        disciplinas = self.consulta_service.listar_disciplinas_por_creditos(min_creditos)

        if not disciplinas:
            print(Fore.YELLOW + "\nNenhuma disciplina encontrada com esse número de créditos.")
            return

        print(Fore.BLUE + f"\n📌 Disciplinas com {min_creditos} ou mais créditos:")
        for disciplina, curso, unidade in disciplinas:
            print(f"{disciplina.codigo} - {disciplina.nome} ({disciplina.creditos_totais} créditos)")
            print(f"  Curso: {curso.nome} | Unidade: {unidade.nome}")

    def _analisar_unidade(self) -> None:
        """Analisa e exibe informações detalhadas de uma unidade."""
        nome = questionary.text("Nome ou sigla da unidade:").ask()
        dados = self.consulta_service.analisar_unidade(nome)

        if not dados:
            print(Fore.RED + "\nUnidade não encontrada. Tente o nome completo ou a sigla.")
            return

        print(Fore.BLUE + f"\n🏛️ Unidade: {dados['nome']}")
        print(f"Total de cursos: {dados['total_cursos']}")
        for curso in dados['cursos']:
            print(f"\n• {curso['nome']}:")
            print(f"  Disciplinas: {curso['disciplinas']} | Carga horária: {curso['carga_horaria']}")
        print(f"\nTotal de disciplinas na unidade: {dados['total_disciplinas']}")
        print(f"Carga horária total: {dados['total_ch']}h")

    def _sair(self) -> bool:
        """
        Finaliza a execução do menu.

        Returns:
            False para indicar que o loop do menu deve ser encerrado
        """
        print(Fore.GREEN + "\n✅ Encerrando consultas. Até mais!")
        return False