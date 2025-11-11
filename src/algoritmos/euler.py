from __future__ import annotations
from collections import defaultdict
from typing import Dict, List

class Hierholzer:
    @staticmethod
    def compute(g) -> List[str]:
        """
        Ruta/circuito euleriano en grafo NO dirigido (si existe).
        Retorna una secuencia de vértices que recorre todas las aristas una vez.
        Si no es euleriano/semieuleriano, retorna lista vacía.
        """
        # Construir adyacencias "modificables" (multiset simple)
        adj: Dict[str, List[str]] = defaultdict(list)
        verts = list(getattr(g, "vertices", lambda: [])())

        # cargar aristas una sola vez
        for u in verts:
            for v in g.get_adjacency_list(u):
                if u < v:
                    adj[u].append(v)
                    adj[v].append(u)

        # Si no hay aristas, devolver vacío o [v]
        if not any(adj.values()):
            return []

        # Elegir start: si hay 0 o 2 impares → válido
        impares = [x for x in adj if len(adj[x]) % 2 == 1]
        if len(impares) == 0:
            start = next(iter(adj))
        elif len(impares) == 2:
            start = impares[0]
        else:
            return []

        # Hierholzer
        stack = [start]
        path: List[str] = []
        local = {u: list(neis) for u, neis in adj.items()}

        while stack:
            u = stack[-1]
            if local.get(u):
                v = local[u].pop()
                # eliminar arista en ambos sentidos
                local[v].remove(u)
                stack.append(v)
            else:
                path.append(stack.pop())

        path.reverse()
        return path
