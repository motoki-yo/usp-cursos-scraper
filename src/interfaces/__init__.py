"""
Módulo de interfaces do sistema.

Este módulo contém as interfaces (contratos) que definem o comportamento
esperado das diferentes partes do sistema.
"""

from .parser import Parser
from .scraper import WebScraper

__all__ = [
    'Parser',
    'WebScraper'
]