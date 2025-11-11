from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple

class TarjanCriticos:
    @staticmethod
    def compute(g) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        Retorna (articulaciones, puentes) en grafo NO dirigido.
        - articulaciones: lista de vértices
        - puentes: lista de tuplas (u, v) con u < v
        """
        time = 0
        disc: Dict[str, int] = {}
        low: Dict[str, int] = {}
        parent: Dict[str, Optional[str]] = {}
        arts: Set[str] = set()
        edges: Set[Tuple[str, str]] = set()

        def dfs(u: str):
            nonlocal time
            time += 1
            disc[u] = low[u] = time
            children = 0
            for v in g.get_adjacency_list(u):
                if v not in disc:
                    parent[v] = u
                    children += 1
                    dfs(v)
                    low[u] = min(low[u], low[v])
                    # Articulación
                    if parent.get(u) is None and children > 1:
                        arts.add(u)
                    if parent.get(u) is not None and low[v] >= disc[u]:
                        arts.add(u)
                    # Puente
                    if low[v] > disc[u]:
                        a, b = (u, v) if u < v else (v, u)
                        edges.add((a, b))
                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])

        for s in getattr(g, "vertices", lambda: [])():
            if s not in disc:
                parent[s] = None
                dfs(s)

        return sorted(arts), sorted(edges)
