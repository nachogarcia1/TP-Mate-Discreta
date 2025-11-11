from __future__ import annotations
import heapq
from typing import Dict, Optional, Tuple, Set, List

def _w(g, u: str, v: str) -> float:
    # Usa get_weight si existe; si no, 1.0
    if hasattr(g, "get_weight"):
        w = g.get_weight(u, v)
        if w is not None:
            return float(w)
    return 1.0

class Dijkstra:
    @staticmethod
    def compute(g, s: str, t: Optional[str] = None, banned: Optional[Set[str]] = None) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        """
        Dijkstra con heap. Retorna (dist, parent). Si t se da, puede cortar.
        """
        banned = banned or set()
        if s in banned:
            return {}, {}

        dist: Dict[str, float] = {s: 0.0}
        parent: Dict[str, Optional[str]] = {s: None}
        pq = [(0.0, s)]

        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            if t is not None and u == t:
                break
            for v in g.get_adjacency_list(u):
                if v in banned:
                    continue
                nd = d + _w(g, u, v)
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    parent[v] = u
                    heapq.heappush(pq, (nd, v))
        return dist, parent

    @staticmethod
    def path(parent: Dict[str, Optional[str]], t: str) -> List[str]:
        if t not in parent:
            return []
        out: List[str] = []
        cur = t
        while cur is not None:
            out.append(cur)
            cur = parent[cur]
        return out[::-1]
