from src.navigator import iniciar_driver, acessar_jupiter, obter_unidades, selecionar_unidade
from src.parser import extrair_grade_curricular, salvar_json

def main():
    driver = iniciar_driver()
    acessar_jupiter(driver)

    unidades = obter_unidades(driver)

    for codigo, nome in unidades:
        print(f"Processando unidade: {nome}")
        selecionar_unidade(driver, codigo)

        # TODO: coletar cursos dessa unidade
        # TODO: navegar para grade curricular de cada curso
        # TODO: usar parser e salvar resultados
    
    driver.quit()

if __name__ == "__main__":
    main()