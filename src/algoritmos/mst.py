from __future__ import annotations
import heapq
from typing import List, Tuple

# -------------------------
# Union-Find (clase con estado)
# -------------------------
class UnionFind:
    __slots__ = ("parent", "rank")
    def __init__(self, elementos: List[str]):
        self.parent = {x: x for x in elementos}
        self.rank   = {x: 0 for x in elementos}

    def find(self, x: str) -> str:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: str, b: str) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

# Helper peso
def _w(g, u: str, v: str) -> float:
    if hasattr(g, "get_weight"):
        w = g.get_weight(u, v)
        if w is not None:
            return float(w)
    return 1.0

# -------------------------
# Kruskal (bosque MST)
# -------------------------
class KruskalMST:
    @staticmethod
    def compute(g) -> Tuple[List[Tuple[str, str, float]], float]:
        """
        Devuelve (edges, total_weight) del bosque generador mínimo.
        En no dirigidos: cada arista una vez.
        """
        verts: List[str] = list(getattr(g, "vertices", lambda: [])())
        uf = UnionFind(verts)

        # Recolectar aristas únicas
        edges = []
        for u in verts:
            for v in g.get_adjacency_list(u):
                if getattr(g, "is_undirected", lambda: True)():
                    if u >= v:  # evitar duplicados (u<v)
                        continue
                w = _w(g, u, v)
                edges.append((w, u, v))

        edges.sort(key=lambda x: (x[0], x[1], x[2]))

        mst: List[Tuple[str, str, float]] = []
        total = 0.0
        for w, u, v in edges:
            if uf.union(u, v):
                mst.append((u, v, w))
                total += w
        return mst, total

# -------------------------
# Prim (bosque MST)
# -------------------------
class PrimMST:
    @staticmethod
    def compute(g) -> Tuple[List[Tuple[str, str, float]], float]:
        """
        Prim por componentes: genera un bosque si el grafo está desconectado.
        """
        verts: List[str] = list(getattr(g, "vertices", lambda: [])())
        visited = set()
        result: List[Tuple[str, str, float]] = []
        total = 0.0

        for start in sorted(verts):
            if start in visited:
                continue
            visited.add(start)
            pq = []
            for v in g.get_adjacency_list(start):
                heapq.heappush(pq, (_w(g, start, v), start, v))

            while pq:
                w, u, v = heapq.heappop(pq)
                if v in visited:
                    continue
                visited.add(v)
                result.append((u, v, w))
                total += w
                for z in g.get_adjacency_list(v):
                    if z not in visited:
                        heapq.heappush(pq, (_w(g, v, z), v, z))
        return result, total
