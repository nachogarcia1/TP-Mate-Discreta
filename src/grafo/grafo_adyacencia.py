from .interfaz_grafo import Grafo

class GrafoAdyacencia(Grafo):
    def __init__(self, no_dirigido: bool = True):
        self.vs: list[str] = []
        self.name_to_idx: dict[str, int] = {}
        self.matrix: list[list[float]] = []
        self.vertex_count: int = 0
        self.edge_count: int = 0    # en no dirigidos, cuenta cada arista una sola vez
        self.no_dirigido = no_dirigido

    # ---------- helpers internos ----------
    def _ensure_vertex(self, v: str) -> int:
        """Crea el vértice si no existe y devuelve su índice."""
        if v in self.name_to_idx:
            return self.name_to_idx[v]
        idx = self.vertex_count
        self.vs.append(v)
        self.name_to_idx[v] = idx
        # expandir matriz
        for fila in self.matrix:
            fila.append(0.0)
        self.matrix.append([0.0] * (idx + 1))
        self.vertex_count += 1
        return idx

    # ---------- interfaz requerida ----------
    def add_vertex(self, v: str):
        self._ensure_vertex(v)

    def delete_vertex(self, v: str):
        if v not in self.name_to_idx:
            return
        idx = self.name_to_idx[v]

        # calcular cuántas aristas elimina este vértice
        # En no dirigidos: cada arista (idx, j) cuenta una sola vez
        deg = sum(1 for w in self.matrix[idx] if w != 0.0)
        if self.no_dirigido:
            self.edge_count -= deg
        else:
            # dirigidos: salientes + entrantes
            out_deg = deg
            in_deg = sum(1 for fila in self.matrix if fila[idx] != 0.0)
            self.edge_count -= (out_deg + in_deg)

        # quitar fila y columna idx
        self.matrix.pop(idx)
        for fila in self.matrix:
            fila.pop(idx)

        # actualizar vs y name_to_idx
        self.vs.pop(idx)
        # reconstruir name_to_idx (índices cambiaron)
        self.name_to_idx.clear()
        for i, name in enumerate(self.vs):
            self.name_to_idx[name] = i

        self.vertex_count -= 1

    def add_edge(self, u: str, v: str, w: float = 1.0):
        """Compatible con la interfaz (u, v). Si te llaman sin peso, usa 1.0."""
        i = self._ensure_vertex(u)
        j = self._ensure_vertex(v)

        # si no existía la arista, incrementa contador
        if self.matrix[i][j] == 0.0:
            self.matrix[i][j] = float(w)
            if self.no_dirigido:
                self.matrix[j][i] = float(w)
                self.edge_count += 1
            else:
                self.edge_count += 1
        else:
            # si ya existía, actualizá el peso (por si el vial actualiza tiempos)
            self.matrix[i][j] = float(w)
            if self.no_dirigido:
                self.matrix[j][i] = float(w)

    def delete_edge(self, u: str, v: str):
        if u not in self.name_to_idx or v not in self.name_to_idx:
            return
        i = self.name_to_idx[u]
        j = self.name_to_idx[v]
        if self.matrix[i][j] != 0.0:
            self.matrix[i][j] = 0.0
            if self.no_dirigido:
                self.matrix[j][i] = 0.0
                self.edge_count -= 1
            else:
                self.edge_count -= 1

    def exists_edge(self, u: str, v: str) -> bool:
        if u not in self.name_to_idx or v not in self.name_to_idx:
            return False
        i = self.name_to_idx[u]
        j = self.name_to_idx[v]
        return self.matrix[i][j] != 0.0

    def order(self) -> int:
        return self.vertex_count

    def get_adjacency_list(self, v: str) -> list[str]:
        if v not in self.name_to_idx:
            return []
        i = self.name_to_idx[v]
        out: list[str] = []
        for j, peso in enumerate(self.matrix[i]):
            if peso != 0.0:
                out.append(self.vs[j])
        return out

    # ---------- helpers opcionales (útiles para algoritmos) ----------
    def get_weight(self, u: str, v: str) -> float or None:
        if u not in self.name_to_idx or v not in self.name_to_idx:
            return None
        i = self.name_to_idx[u]
        j = self.name_to_idx[v]
        w = self.matrix[i][j]
        return w if w != 0.0 else None

    def vertices(self) -> list[str]:
        return list(self.vs)

    def edges(self) -> list[tuple[str, str, float]]:
        """Devuelve aristas con peso. En no dirigidos, cada arista una sola vez (i<j)."""
        es = []
        for i in range(self.vertex_count):
            for j in range(self.vertex_count):
                if self.matrix[i][j] != 0.0:
                    if self.no_dirigido and j <= i:
                        continue
                    es.append((self.vs[i], self.vs[j], self.matrix[i][j]))
        return es
