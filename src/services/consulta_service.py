from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from ..models.unidade import Unidade
from ..models.curso import Curso
from ..models.disciplina import Disciplina

class ConsultaService:
    """
    Serviço responsável por realizar consultas nos dados coletados.
    
    Mantém índices para otimizar as consultas e fornece métodos
    para diferentes tipos de busca.
    
    Attributes:
        unidades: Lista de unidades com seus dados
        _index_unidades: Dicionário para busca rápida de unidades
        _index_cursos: Dicionário para busca rápida de cursos
        _index_disciplinas: Dicionário para busca rápida de disciplinas
    """

    def __init__(self, unidades: List[Unidade]):
        self.unidades = unidades
        self._index_unidades = self._criar_index_unidades()
        self._index_siglas = self._criar_index_siglas()
        self._index_cursos = self._criar_index_cursos()
        self._index_disciplinas = self._criar_index_disciplinas()

    def _criar_index_unidades(self) -> Dict[str, Unidade]:
        """Cria índice para busca rápida de unidades."""
        return {unidade.nome.lower(): unidade for unidade in self.unidades}
    
    def _criar_index_siglas(self) -> Dict[str, Unidade]:
        """Cria índice para busca por sigla."""
        return {
            self._extrair_sigla(unidade.nome): unidade 
            for unidade in self.unidades
        }
    
    @staticmethod
    def _extrair_sigla(nome: str) -> str:
        """
        Extrai a sigla de uma unidade do seu nome completo.
        
        Args:
            nome: Nome completo da unidade (ex: "Escola de Artes, Ciências e Humanidades - ( EACH )")
            
        Returns:
            Sigla da unidade (ex: "EACH")
        """
        try:
            # Procura o texto entre parênteses e remove espaços
            inicio = nome.rfind('(')
            fim = nome.rfind(')')
            if inicio != -1 and fim != -1:
                return nome[inicio+1:fim].strip()
            return ""
        except Exception:
            return ""

    def _criar_index_cursos(self) -> Dict[str, Curso]:
        """Cria índice para busca rápida de cursos."""
        return {
            curso.nome.lower(): curso
            for unidade in self.unidades
            for curso in unidade.cursos
        }

    def _criar_index_disciplinas(self) -> Dict[str, List[Tuple[Disciplina, Curso]]]:
        """Cria índice para busca rápida de disciplinas."""
        index = defaultdict(list)
        for unidade in self.unidades:
            for curso in unidade.cursos:
                for disciplina in curso.todas_disciplinas:
                    index[disciplina.codigo].append((disciplina, curso))
        return index

    def listar_unidades(self) -> List[str]:
        """
        Lista todas as unidades disponíveis.
        
        Returns:
            Lista com os nomes das unidades
        """
        return [unidade.nome for unidade in self.unidades]

    def buscar_unidade(self, termo: str) -> Optional[Unidade]:
        """
        Busca uma unidade pelo nome completo ou sigla.
        
        Args:
            termo: Nome completo ou sigla da unidade
            
        Returns:
            Unidade encontrada ou None
        """
        termo = termo.strip()
        # Tenta buscar por nome completo
        unidade = self._index_unidades.get(termo.lower())
        if unidade:
            return unidade
            
        # Se não encontrou, tenta buscar por sigla
        return self._index_siglas.get(termo.upper())
    
    def listar_cursos_por_unidade(self, termo: str) -> Optional[tuple]:
        """
        Obtém os cursos de uma unidade específica.
        
        Args:
            termo: Nome completo ou sigla da unidade
            
        Returns:
            Tupla (nome_unidade, lista_cursos) ou None se não encontrada
        """
        unidade = self.buscar_unidade(termo)
        if unidade:
            return unidade.nome, [curso.nome for curso in unidade.cursos]
        return None

    def buscar_curso(self, nome: str) -> Optional[Curso]:
        """
        Busca um curso pelo nome.
        
        Args:
            nome: Nome do curso
            
        Returns:
            Curso encontrado ou None
        """
        return self._index_cursos.get(nome.lower())

    def buscar_disciplina(self, codigo: str) -> List[Tuple[Disciplina, Curso]]:
        """
        Busca uma disciplina pelo código.
        
        Args:
            codigo: Código da disciplina
            
        Returns:
            Lista de tuplas (disciplina, curso) onde a disciplina aparece
        """
        return self._index_disciplinas.get(codigo.upper(), [])

    def listar_disciplinas_comuns(self) -> Dict[str, List[Tuple[Disciplina, Curso]]]:
        """
        Lista disciplinas que aparecem em mais de um curso.
        
        Returns:
            Dicionário com código da disciplina e lista de ocorrências
        """
        return {
            codigo: ocorrencias
            for codigo, ocorrencias in self._index_disciplinas.items()
            if len(ocorrencias) > 1
        }
    
    def analisar_carga_curso(self, nome_curso: str) -> Optional[dict]:
        """
        Analisa a distribuição de carga horária de um curso.
        
        Returns:
            Dicionário com as informações do curso ou None se não encontrado
        """
        curso = self.buscar_curso(nome_curso)
        if not curso:
            return None

        return {
            'nome': curso.nome,
            'total_creditos': sum(d.creditos_totais for d in curso.todas_disciplinas),
            'total_ch': sum(d.carga_horaria for d in curso.todas_disciplinas),
            'qtd_obrigatorias': len(curso.obrigatorias),
            'qtd_optativas_livres': len(curso.optativas_livres),
            'qtd_optativas_eletivas': len(curso.optativas_eletivas)
        }

    def comparar_cursos(self, nome_curso1: str, nome_curso2: str) -> Optional[tuple]:
        """
        Compara dois cursos.
        
        Returns:
            Tupla com dados dos dois cursos ou None se algum não for encontrado
        """
        curso1 = self.buscar_curso(nome_curso1)
        curso2 = self.buscar_curso(nome_curso2)
        
        if not curso1 or not curso2:
            return None

        dados_curso1 = {
            'nome': curso1.nome,
            'total_disciplinas': len(curso1.todas_disciplinas),
            'total_ch': sum(d.carga_horaria for d in curso1.todas_disciplinas)
        }
        
        dados_curso2 = {
            'nome': curso2.nome,
            'total_disciplinas': len(curso2.todas_disciplinas),
            'total_ch': sum(d.carga_horaria for d in curso2.todas_disciplinas)
        }
        
        return dados_curso1, dados_curso2

    def listar_disciplinas_por_creditos(self, min_creditos: int) -> List[tuple]:
        """
        Lista disciplinas com número mínimo de créditos.
        
        Returns:
            Lista de tuplas (disciplina, curso, unidade)
        """
        resultados = []
        for unidade in self.unidades:
            for curso in unidade.cursos:
                for disc in curso.todas_disciplinas:
                    if disc.creditos_totais >= min_creditos:
                        resultados.append((disc, curso, unidade))
        return resultados

    def analisar_unidade(self, nome_unidade: str) -> Optional[dict]:
        """
        Analisa uma unidade.
        
        Returns:
            Dicionário com dados da unidade ou None se não encontrada
        """
        unidade = self.buscar_unidade(nome_unidade)
        if not unidade:
            return None

        cursos_info = []
        total_disciplinas = 0
        total_ch = 0
        
        for curso in unidade.cursos:
            disc_curso = len(curso.todas_disciplinas)
            ch_curso = sum(d.carga_horaria for d in curso.todas_disciplinas)
            total_disciplinas += disc_curso
            total_ch += ch_curso
            
            cursos_info.append({
                'nome': curso.nome,
                'disciplinas': disc_curso,
                'carga_horaria': ch_curso
            })
        
        return {
            'nome': unidade.nome,
            'total_cursos': len(unidade.cursos),
            'cursos': cursos_info,
            'total_disciplinas': total_disciplinas,
            'total_ch': total_ch
        }