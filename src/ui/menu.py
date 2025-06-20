from typing import Callable, Dict
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
        self.consulta_service = consulta_service
        self.opcoes: Dict[str, Callable] = {
            "1": self._listar_unidades,
            "2": self._listar_cursos_unidade,
            "3": self._detalhar_curso,
            "4": self._buscar_disciplina,
            "5": self._listar_disciplinas_comuns,
            "6": self._analisar_carga_curso,
            "7": self._comparar_cursos,
            "8": self._listar_disciplinas_por_creditos,
            "9": self._analisar_unidade,
            "10": self._sair
        }

    def executar(self) -> None:
        """Executa o loop principal do menu."""
        while True:
            self._exibir_menu()
            try:
                opcao = input("\nEscolha uma opção: ")
                if opcao in self.opcoes:
                    if self.opcoes[opcao]() is False:  # Se retornar False, sai do loop
                        break
                else:
                    print("\nOpção inválida!")
            except Exception as e:
                print(f"\nErro ao executar operação: {e}")

    def _exibir_menu(self) -> None:
        """Exibe as opções do menu."""
        print("\n==== MENU DE CONSULTAS ====")
        print("1. Listar todas as unidades")
        print("2. Listar cursos por unidade")
        print("3. Ver detalhes de um curso")
        print("4. Buscar disciplina por código")
        print("5. Listar disciplinas comuns a mais de um curso")
        print("6. Analisar carga horária de um curso")
        print("7. Comparar dois cursos")
        print("8. Listar disciplinas por número mínimo de créditos")
        print("9. Analisar unidade")
        print("10. Sair")

    def _listar_unidades(self) -> None:
        """Lista todas as unidades disponíveis."""
        print("\nUnidades disponíveis:")
        for nome in self.consulta_service.listar_unidades():
            print(f"- {nome}")

    def _listar_cursos_unidade(self) -> None:
        """Lista os cursos de uma unidade específica."""
        nome = input("Nome da unidade: ")
        cursos = self.consulta_service.listar_cursos_por_unidade(nome)
        
        if cursos:
            print(f"\nCursos da unidade {nome}:")
            for curso in cursos:
                print(f"- {curso}")
        else:
            print("\nUnidade não encontrada ou sem cursos.")

    def _detalhar_curso(self) -> None:
        """Mostra informações detalhadas de um curso."""
        nome = input("Nome do curso: ")
        curso = self.consulta_service.buscar_curso(nome)
        
        if curso:
            print(f"\nDetalhes do curso: {curso.nome}")
            print(f"Unidade: {curso.unidade}")
            print(f"Duração: {curso.duracao}")
            
            print("\nDisciplinas obrigatórias:")
            for disc in curso.obrigatorias:
                print(f"- {disc}")
                
            print("\nDisciplinas optativas livres:")
            for disc in curso.optativas_livres:
                print(f"- {disc}")
                
            print("\nDisciplinas optativas eletivas:")
            for disc in curso.optativas_eletivas:
                print(f"- {disc}")
        else:
            print("\nCurso não encontrado.")

    def _buscar_disciplina(self) -> None:
        """Busca e exibe informações de uma disciplina."""
        codigo = input("Código da disciplina: ")
        ocorrencias = self.consulta_service.buscar_disciplina(codigo)
        
        if ocorrencias:
            disc = ocorrencias[0][0]  # Primeira ocorrência para info da disciplina
            print(f"\nDisciplina {codigo}:")
            print(f"Nome: {disc.nome}")
            print(f"Créditos aula: {disc.creditos_aula}")
            print(f"Créditos trabalho: {disc.creditos_trabalho}")
            print(f"Carga horária: {disc.carga_horaria}")
            
            print("\nPresente nos cursos:")
            for _, curso in ocorrencias:
                print(f"- {curso}")
        else:
            print("\nDisciplina não encontrada.")

    def _listar_disciplinas_comuns(self) -> None:
        """Lista disciplinas que aparecem em mais de um curso."""
        disciplinas_comuns = self.consulta_service.listar_disciplinas_comuns()
        
        if disciplinas_comuns:
            print("\nDisciplinas presentes em mais de um curso:")
            for codigo, ocorrencias in disciplinas_comuns.items():
                disc = ocorrencias[0][0]
                print(f"\n{codigo} - {disc.nome}")
                print("Presente nos cursos:")
                for _, curso in ocorrencias:
                    print(f"- {curso}")
        else:
            print("\nNenhuma disciplina comum encontrada.")
    
    def _analisar_carga_curso(self) -> None:
        """Analisa e exibe a distribuição de carga horária de um curso."""
        nome = input("Nome do curso: ")
        dados = self.consulta_service.analisar_carga_curso(nome)
        
        if not dados:
            print("\nCurso não encontrado.")
            return
            
        print(f"\nAnálise do curso: {dados['nome']}")
        print(f"Total de créditos: {dados['total_creditos']}")
        print(f"Carga horária total: {dados['total_ch']} horas")
        print("\nDistribuição de disciplinas:")
        print(f"Obrigatórias: {dados['qtd_obrigatorias']}")
        print(f"Optativas Livres: {dados['qtd_optativas_livres']}")
        print(f"Optativas Eletivas: {dados['qtd_optativas_eletivas']}")

    def _comparar_cursos(self) -> None:
        """Compara e exibe informações de dois cursos."""
        nome1 = input("Nome do primeiro curso: ")
        nome2 = input("Nome do segundo curso: ")
        
        resultado = self.consulta_service.comparar_cursos(nome1, nome2)
        if not resultado:
            print("\nUm ou ambos os cursos não encontrados.")
            return
            
        curso1, curso2 = resultado
        print(f"\nComparação entre {curso1['nome']} e {curso2['nome']}:")
        
        print(f"\n{curso1['nome']}:")
        print(f"Total de disciplinas: {curso1['total_disciplinas']}")
        print(f"Carga horária total: {curso1['total_ch']}")
        
        print(f"\n{curso2['nome']}:")
        print(f"Total de disciplinas: {curso2['total_disciplinas']}")
        print(f"Carga horária total: {curso2['total_ch']}")

    def _listar_disciplinas_por_creditos(self) -> None:
        """Lista disciplinas filtradas por número mínimo de créditos."""
        try:
            min_creditos = int(input("Número mínimo de créditos: "))
        except ValueError:
            print("\nPor favor, insira um número válido.")
            return
            
        disciplinas = self.consulta_service.listar_disciplinas_por_creditos(min_creditos)
        
        if not disciplinas:
            print("\nNenhuma disciplina encontrada com esse número de créditos.")
            return
            
        print(f"\nDisciplinas com {min_creditos} ou mais créditos:")
        for disciplina, curso, unidade in disciplinas:
            print(f"{disciplina.codigo} - {disciplina.nome} "
                f"({disciplina.creditos_totais} créditos)")
            print(f"  Curso: {curso.nome}")
            print(f"  Unidade: {unidade.nome}\n")

    def _analisar_unidade(self) -> None:
        """Analisa e exibe informações detalhadas de uma unidade."""
        nome = input("Nome ou sigla da unidade: ")
        dados = self.consulta_service.analisar_unidade(nome)
        
        if not dados:
            print("\nUnidade não encontrada. Tente o nome completo ou a sigla (ex: EACH)")
            return
            
        print(f"\nAnálise da unidade: {dados['nome']}")
        print(f"Total de cursos: {dados['total_cursos']}")
        
        for curso in dados['cursos']:
            print(f"\nCurso: {curso['nome']}")
            print(f"  Disciplinas: {curso['disciplinas']}")
            print(f"  Carga horária: {curso['carga_horaria']}")
        
        print(f"\nTotal de disciplinas na unidade: {dados['total_disciplinas']}")
        print(f"Carga horária total da unidade: {dados['total_ch']}")

    def _sair(self) -> bool:
        """
        Finaliza a execução do menu.
        
        Returns:
            False para indicar que o loop do menu deve ser encerrado
        """
        print("\nEncerrando consultas...")
        return False