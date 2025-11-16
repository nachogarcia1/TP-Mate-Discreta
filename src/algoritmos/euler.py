from __future__ import annotations
from collections import defaultdict
from typing import Dict, List


class Hierholzer:
    @staticmethod
    def compute(g) -> List[str]:
        """
        Calcula un camino/circuito euleriano en un grafo NO dirigido (si existe).
        Usa g.edges() para reconstruir el grafo.
        Devuelve la secuencia de vértices que recorre cada arista exactamente una vez.
        Si no es euleriano/semieuleriano, retorna lista vacía.
        """

        # 1) Construir adyacencias como grafo no dirigido
        adj: Dict[str, List[str]] = defaultdict(list)
        for u, v, w in g.edges():
            adj[u].append(v)
            adj[v].append(u)

        if not adj:
            return []

        # 2) Determinar vértices de grado impar
        impares = [v for v, neis in adj.items() if len(neis) % 2 == 1]

        # 3) Si no es euleriano (0 impares) ni semieuleriano (2 impares) → no hay camino
        if len(impares) not in (0, 2):
            return []

        # 4) Elegir vértice inicial de forma determinista
        if len(impares) == 2:
            # Camino euleriano: arrancamos en el menor de los impares
            start = min(impares)
        else:
            # Circuito euleriano: arrancamos en el menor vértice con aristas
            start = min(adj.keys())

        # 5) Copia local de adyacencias para ir "borrando" aristas
        local: Dict[str, List[str]] = {u: list(neis) for u, neis in adj.items()}

        stack: List[str] = [start]
        path: List[str] = []

        # 6) Algoritmo de Hierholzer
        while stack:
            u = stack[-1]
            if local[u]:
                v = local[u].pop()
                local[v].remove(u)
                stack.append(v)
            else:
                path.append(stack.pop())

        path.reverse()
        return path
