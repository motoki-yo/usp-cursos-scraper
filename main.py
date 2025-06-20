import sys
from src.jupiter_collector import JupiterCollector
from src.consultas import ConsultasJupiter

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <quantidade_unidades>")
        sys.exit(1)

    quantidade = int(sys.argv[1])
    print(f"Iniciando coleta de dados para {quantidade} unidades...")

    collector = JupiterCollector()
    unidades = collector.coletar_dados(quantidade)

    print("Coleta concluída. Iniciando menu interativo.")
    consultas = ConsultasJupiter(unidades)
    consultas.executar_menu()