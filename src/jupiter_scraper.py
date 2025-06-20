from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time

class JupiterScraper:
    def __init__(self, headless=True):
        self.driver = self._iniciar_driver(headless)

    def _iniciar_driver(self, headless):
        chromedriver_autoinstaller.install()
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)
        
    def acessar_pagina_inicial(self):
        url = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "comboUnidade"))
        )
        time.sleep(2)
        
    def obter_unidades(self):
        wait = WebDriverWait(self.driver, 30)
        seletor = Select(self.driver.find_element(By.ID, "comboUnidade"))
        wait.until(lambda _: len(seletor.options) > 1)
        return [
            (option.get_attribute("value"), option.text.strip())
            for option in seletor.options
            if option.get_attribute("value")
        ]

    def selecionar_unidade(self, codigo_unidade: str):
        seletor = Select(self.driver.find_element(By.ID, "comboUnidade"))
        seletor.select_by_value(codigo_unidade)

    def obter_cursos(self):
        wait = WebDriverWait(self.driver, 30)
        seletor = Select(self.driver.find_element(By.ID, "comboCurso"))
        wait.until(lambda _: len(seletor.options) > 1)
        return [
            (option.get_attribute("value"), option.text.strip())
            for option in seletor.options
            if option.get_attribute("value")
        ]

    def acessar_grade_curso(self, codigo_curso: str):
        self.selecionar_curso(codigo_curso)
        self.clicar_buscar()
        return self.acessar_aba_grade_curricular()
    
    def selecionar_curso(self, codigo_curso: str):
        seletor = Select(self.driver.find_element(By.ID, "comboCurso"))
        time.sleep(2)
        seletor.select_by_value(codigo_curso)

    def clicar_buscar(self):
        wait = WebDriverWait(self.driver, 30)
        botao = wait.until(EC.element_to_be_clickable((By.ID, "enviar")))
        botao.click()
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Grade curricular")))
        time.sleep(2)
        
    def acessar_aba_grade_curricular(self):
        wait = WebDriverWait(self.driver, 30)
        link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Grade curricular")))
        link.click()
        wait.until(EC.presence_of_element_located((By.ID, "gradeCurricular")))
        time.sleep(2)
        return self.driver.page_source

    def fechar(self):
        self.driver.quit()