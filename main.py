"""
Sistema de Coleta e Consulta de Dados do Jupiter Web.

Este script é o ponto de entrada do sistema que coleta e permite consultar
dados dos cursos da USP através do sistema Jupiter Web.

Authors:
    Guilherme Panza
    Melissa Motoki
"""

import sys
import argparse
from typing import List
from src.services.coleta_service import ColetaService
from src.services.consulta_service import ConsultaService
from src.scrapers.jupiter_scraper import JupiterScraper
from src.parsers.jupiter_parser import JupiterParser
from src.ui.menu import Menu
from src.models.unidade import Unidade

def parse_argumentos() -> argparse.Namespace:
    """
    Processa os argumentos da linha de comando.
    
    Returns:
        Namespace com os argumentos processados
    """
    parser = argparse.ArgumentParser(
        description='Coleta e consulta dados dos cursos da USP no sistema Jupiter.'
    )
    parser.add_argument(
        'quantidade_unidades',
        type=int,
        help='Número de unidades a serem coletadas'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Executa o navegador em modo headless (sem interface gráfica)'
    )
    return parser.parse_args()

def coletar_dados(quantidade: int, headless: bool = True) -> List[Unidade]:
    """
    Realiza a coleta dos dados do Jupiter.
    
    Args:
        quantidade: Número de unidades a serem coletadas
        headless: Se True, executa o navegador em modo headless
        
    Returns:
        Lista de unidades coletadas com seus cursos
    """
    print(f"Iniciando coleta de dados para {quantidade} unidades...")
    
    try:
        with JupiterScraper(headless=headless) as scraper:
            parser = JupiterParser()
            coleta_service = ColetaService(scraper, parser)
            unidades = coleta_service.coletar_dados(quantidade)
            
        print(f"Coleta finalizada. {len(unidades)} unidades coletadas.")
        return unidades
        
    except Exception as e:
        print(f"Erro durante a coleta: {e}")
        raise

def main() -> None:
    """Função principal do programa."""
    try:
        # Processamento dos argumentos
        args = parse_argumentos()
        
        if args.quantidade_unidades < 1:
            print("Quantidade de unidades deve ser maior que zero")
            sys.exit(1)
            
        # Coleta de dados
        unidades = coletar_dados(args.quantidade_unidades, args.headless)
        
        if not unidades:
            print("Nenhuma unidade foi coletada")
            sys.exit(1)
            
        # Inicialização do sistema de consultas
        print("Iniciando sistema de consultas...")
        consulta_service = ConsultaService(unidades)
        menu = Menu(consulta_service)
        
        # Execução do menu interativo
        print("Iniciando menu interativo")
        menu.executar()
        
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()