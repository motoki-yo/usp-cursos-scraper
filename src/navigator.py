from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

def iniciar_driver():
    options = Options()
    options.add_argument("--headless")  # opcional: executa sem abrir janela
    driver = webdriver.Chrome(options=options)
    return driver

def acessar_jupiter(driver):
    url = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
    driver.get(url)
    time.sleep(3)  # aguarda o carregamento

def obter_unidades(driver):
    seletor = driver.find_element(By.NAME, "codcg")
    opcoes = seletor.find_elements(By.TAG_NAME, "option")
    unidades = [(op.get_attribute("value"), op.text) for op in opcoes if op.get_attribute("value")]
    return unidades

def selecionar_unidade(driver, codigo_unidade):
    select = Select(driver.find_element(By.NAME, "codcg"))
    select.select_by_value(codigo_unidade)
    driver.find_element(By.NAME, "btnOK").click()
    time.sleep(3)
