"""
Paquete de estructuras de grafos.
Contiene la interfaz y la implementación principal usada por los algoritmos.
"""

from .interfaz_grafo import Grafo
from .grafo_adyacencia import GrafoAdyacencia

__all__ = [
    "Grafo",
    "GrafoAdyacencia",
]