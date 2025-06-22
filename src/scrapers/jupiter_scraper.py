from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException 
import chromedriver_autoinstaller
import time
from ..interfaces.scraper import WebScraper

class JupiterScraper(WebScraper):
    """
    Implementação do scraper para o sistema Jupiter.
    
    Utiliza Selenium WebDriver para navegar e coletar dados do sistema Jupiter.
    
    Attributes:
        driver: Instância do WebDriver
        wait_time: Tempo máximo de espera para elementos (em segundos)
    """

    BASE_URL = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
    WAIT_TIME = 0.1

    def __init__(self, headless: bool = True):
        """
        Inicializa o scraper.
        
        Args:
            headless: Se True, executa o navegador em modo headless (sem interface gráfica)
        """
        self.driver = self._iniciar_driver(headless)
        self.wait = WebDriverWait(self.driver, self.WAIT_TIME)

    def _iniciar_driver(self, headless: bool) -> webdriver.Chrome:
        """
        Inicializa e configura o Chrome WebDriver.
        
        Args:
            headless: Se True, executa em modo headless
            
        Returns:
            Instância configurada do Chrome WebDriver
        """
        chromedriver_autoinstaller.install()
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

    def acessar_pagina_inicial(self) -> None:
        """
        Acessa a página inicial do sistema Jupiter.
        
        Raises:
            WebDriverException: Se não for possível acessar a página
        """
        try:
            self.driver.get(self.BASE_URL)
            self.wait.until(EC.element_to_be_clickable((By.ID, "comboUnidade")))
            seletor = Select(self.driver.find_element(By.ID, "comboUnidade"))
            self.wait.until(lambda _: len(seletor.options) > 1)
        except TimeoutException as e:
            raise WebDriverException(f"Erro ao acessar página inicial: {e}")

    def obter_unidades(self) -> List[Tuple[str, str]]:
        """
        Obtém a lista de unidades disponíveis.
        
        Returns:
            Lista de tuplas (código, nome) das unidades
            
        Raises:
            WebDriverException: Se não for possível obter as unidades
        """
        try:
            seletor = Select(self.driver.find_element(By.ID, "comboUnidade"))
            return [
                (option.get_attribute("value"), option.text.strip())
                for option in seletor.options
                if option.get_attribute("value")
            ]
        except Exception as e:
            raise WebDriverException(f"Erro ao obter unidades: {e}")

    def selecionar_unidade(self, codigo: str) -> None:
        """
        Seleciona uma unidade específica.
        
        Args:
            codigo: Código da unidade
            
        Raises:
            WebDriverException: Se não for possível selecionar a unidade
        """
        try:
            seletor = Select(self.driver.find_element(By.ID, "comboUnidade"))
            seletor.select_by_value(codigo)

            seletor_cursos = Select(self.driver.find_element(By.ID, "comboCurso"))
            self.wait.until(lambda _: len(seletor_cursos.options) > 1)
        except Exception as e:
            raise WebDriverException(f"Erro ao selecionar unidade: {e}")

    def obter_cursos(self) -> List[Tuple[str, str]]:
        """
        Obtém a lista de cursos da unidade selecionada.
        
        Returns:
            Lista de tuplas (código, nome) dos cursos
            
        Raises:
            WebDriverException: Se não for possível obter os cursos
        """
        try:
            seletor = Select(self.driver.find_element(By.ID, "comboCurso"))
            return [
                (option.get_attribute("value"), option.text.strip())
                for option in seletor.options
                if option.get_attribute("value")
            ]
        except Exception as e:
            raise WebDriverException(f"Erro ao obter cursos: {e}")

    def acessar_grade_curso(self, codigo_curso: str) -> str:
        """
        Acessa a grade curricular de um curso.
        
        Args:
            codigo_curso: Código do curso
            
        Returns:
            HTML da página da grade curricular ou None se não houver dados
        """
        try:
            self.selecionar_curso(codigo_curso)
            self.clicar_buscar()
            
            # Verifica se existe popup de erro
            try:
                popup = self.driver.find_element(By.ID, "err")
                print(f"Erro ao acessar grade do curso: {codigo_curso}")
                return None
            except NoSuchElementException:
                pass  # Se não encontrou popup, continua normalmente
            
            return self.acessar_aba_grade_curricular()
            
        except Exception as e:
            print(f"Erro ao acessar grade do curso: {e}")
            return None

    def selecionar_curso(self, codigo_curso: str) -> None:
        """
        Seleciona um curso específico.
        
        Args:
            codigo_curso: Código do curso
        """
        seletor = Select(self.driver.find_element(By.ID, "comboCurso"))
        seletor.select_by_value(codigo_curso)

    def clicar_buscar(self) -> None:
        """
        Clica no botão de buscar e aguarda carregamento.
        """
        try:
            botao = self.wait.until(EC.element_to_be_clickable((By.ID, "enviar")))
            botao.click()
            
            # Verifica se há popup de erro
            try:
                popup = self.wait.until(EC.presence_of_element_located((By.ID, "err")))
                return
            except TimeoutException:
                pass
            
            # Se não houver popup, espera pelo link da grade
            self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Grade curricular"))
            )
            
        except Exception as e:
            print(f"Erro ao clicar em buscar: {e}")
            return False

    def acessar_aba_grade_curricular(self) -> str:
        """
        Acessa a aba de grade curricular e retorna seu HTML.
        """
        try:
            # Espera explícita pelo link da grade
            link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Grade curricular"))
            )
            link.click()
            
            # Espera pela presença do elemento da grade
            self.wait.until(
                lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "#gradeCurricular table")) > 0
            )
            
            return self.driver.page_source
        except Exception as e:
            raise WebDriverException(f"Erro ao acessar aba grade curricular: {e}")
    
    def fechar(self) -> None:
        """
        Fecha o navegador e libera recursos.
        """
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        """
        Permite uso do scraper com context manager.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Garante que o driver será fechado ao sair do context manager.
        """
        self.fechar()

    # Métodos implementados para satisfazer a interface WebScraper

    def listar_unidades_urls(self) -> List[str]:
        """
        Retorna uma lista de códigos das unidades que serão usadas para navegar.
        
        Como o sistema Jupiter não possui URLs únicas para cada unidade,
        utilizamos o código da unidade como identificador para seleção via Selenium.
        """
        self.acessar_pagina_inicial()
        unidades = self.obter_unidades()
        return [codigo for codigo, nome in unidades]

    def obter_html(self, codigo_unidade: str) -> str:
        """
        Seleciona a unidade pelo código e retorna o HTML da página atual.
        
        Args:
            codigo_unidade: Código da unidade a ser selecionada.
            
        Returns:
            HTML da página após seleção da unidade.
        """
        self.acessar_pagina_inicial()
        self.selecionar_unidade(codigo_unidade)
        time.sleep(0.2)  # Pequena espera para garantir o carregamento da página
        return self.driver.page_source