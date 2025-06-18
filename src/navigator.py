import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller


def iniciar_driver(headless=True):
    chromedriver_autoinstaller.install()
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    return driver


def acessar_jupiter(driver):
    url = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
    driver.get(url)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "comboUnidade"))
        )
    except Exception:
        print("Elemento 'comboUnidade' não encontrado após 20s")
        with open("pagina_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("debug_jupiter.png")

def obter_unidades(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
    seletor = Select(driver.find_element(By.ID, "comboUnidade"))
    unidades = [
        (option.get_attribute("value"), option.text.strip())
        for option in seletor.options
        if option.get_attribute("value")
    ]
    return unidades


def selecionar_unidade(driver, codigo_unidade):
    seletor = Select(driver.find_element(By.ID, "comboUnidade"))
    seletor.select_by_value(codigo_unidade)
    # Esperar comboCurso ser populado
    wait = WebDriverWait(driver, 15)
    wait.until(
        lambda d: len(Select(d.find_element(By.ID, "comboCurso")).options) > 1
    )
    time.sleep(1)


def obter_cursos(driver):
    seletor = Select(driver.find_element(By.ID, "comboCurso"))
    cursos = [
        (option.get_attribute("value"), option.text.strip())
        for option in seletor.options
        if option.get_attribute("value")
    ]
    return cursos


def selecionar_curso(driver, codigo_curso):
    seletor = Select(driver.find_element(By.ID, "comboCurso"))
    seletor.select_by_value(codigo_curso)
    time.sleep(0.5)


def clicar_buscar(driver):
    botao_buscar = driver.find_element(By.ID, "enviar")
    botao_buscar.click()
    # Esperar carregar a página do curso (link Grade Curricular)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Grade Curricular"))
    )
    time.sleep(1)


def acessar_aba_grade_curricular(driver):
    try:
        link = driver.find_element(By.LINK_TEXT, "Grade Curricular")
        link.click()
        time.sleep(3)
    except Exception as e:
        print("Erro ao acessar aba Grade Curricular:", e)
        return False
    return True


def obter_html_grade(driver):
    return driver.page_source


def coletar_cursos_unidade(driver, codigo_unidade):
    selecionar_unidade(driver, codigo_unidade)
    cursos = obter_cursos(driver)
    dados_cursos = []

    for codigo_curso, nome_curso in cursos:
        print(f"    Coletando curso: {nome_curso}")
        selecionar_curso(driver, codigo_curso)
        clicar_buscar(driver)

        sucesso = acessar_aba_grade_curricular(driver)
        if not sucesso:
            print(f"    Falha ao acessar grade curricular do curso {nome_curso}")
            continue

        html_grade = obter_html_grade(driver)
        dados_cursos.append((nome_curso, html_grade))

        # Voltar para a página inicial (formulário) para continuar coletando
        driver.back()
        time.sleep(3)
        # Re-selecionar a unidade para recarregar cursos e evitar erro
        selecionar_unidade(driver, codigo_unidade)

    return dados_cursos