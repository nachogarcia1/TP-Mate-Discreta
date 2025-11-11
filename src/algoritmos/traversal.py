from __future__ import annotations
from collections import deque
from typing import Dict, List, Optional, Set

class BFS:
    @staticmethod
    def compute(g, s: str, t: Optional[str] = None, banned: Optional[Set[str]] = None):
        """
        BFS clásico (no ponderado).
        Retorna (dist, parent, orden). Si 't' se da, corta al alcanzarlo.
        """
        banned = banned or set()
        if s in banned:
            return {}, {}, []

        q = deque([s])
        dist: Dict[str, int] = {s: 0}
        parent: Dict[str, Optional[str]] = {s: None}
        orden: List[str] = [s]

        while q:
            u = q.popleft()
            if t is not None and u == t:
                break
            for v in g.get_adjacency_list(u):
                if v in banned or v in dist:
                    continue
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
                orden.append(v)
        return dist, parent, orden

    @staticmethod
    def path(parent: Dict[str, Optional[str]], t: str) -> List[str]:
        if t not in parent:
            return []
        out = []
        cur = t
        while cur is not None:
            out.append(cur)
            cur = parent[cur]
        return out[::-1]


class DFS:
    @staticmethod
    def compute(g, s: str, banned: Optional[Set[str]] = None) -> List[str]:
        """
        DFS iterativo que retorna el preorden del recorrido desde s.
        """
        banned = banned or set()
        if s in banned:
            return []
        vis = {s}
        stack = [s]
        preorder: List[str] = []

        while stack:
            u = stack.pop()
            preorder.append(u)
            # determinismo opcional: recorrer vecinos en orden inverso
            for v in sorted(g.get_adjacency_list(u), reverse=True):
                if v not in vis and v not in banned:
                    vis.add(v)
                    stack.append(v)
        return preorder


class ComponentesConexos:
    @staticmethod
    def compute(g) -> List[List[str]]:
        """
        Lista de componentes (cada una lista de vértices).
        """
        vis: Set[str] = set()
        comps: List[List[str]] = []
        for s in sorted(getattr(g, "vertices", lambda: [])()):
            if s in vis:
                continue
            comp = []
            stack = [s]
            vis.add(s)
            while stack:
                u = stack.pop()
                comp.append(u)
                for v in g.get_adjacency_list(u):
                    if v not in vis:
                        vis.add(v)
                        stack.append(v)
            comps.append(sorted(comp))
        return comps
