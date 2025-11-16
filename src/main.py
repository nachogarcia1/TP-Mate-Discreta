"""
Módulo principal para 'Los 100 Grafos Porteños'.
- Carga los tres grafos (eléctrico, vial, hídrico)
- Procesa el archivo de consultas y escribe el archivo de respuestas
"""

from typing import List, Dict, Tuple, Optional, Set

from src.grafo.grafo_adyacencia import GrafoAdyacencia
from src.algoritmos import (
    BFS, ComponentesConexos, Dijkstra, TarjanCriticos, Hierholzer
)

from src.output import (
    format_componentes_conexos,
    format_orden_fallos,
    format_camino_minimo,
    format_simulacion_corte,
    format_ruta_recoleccion,
    format_plantas_asignadas,
    format_puentes_y_articulaciones,
)

# ----------------------------------------------------
# CARGA DE GRAFOS (según formatos del enunciado)
# ----------------------------------------------------

def load_graph(path: str) -> GrafoAdyacencia:
    """
    Carga grafo simple (no dirigido).
    Formato: 'Barrio1 Barrio2' por línea.
    """
    g = GrafoAdyacencia(no_dirigido=True)
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            u, v = parts[0], parts[1]
            g.add_edge(u, v)
    return g


def load_weighted_graph(path: str) -> GrafoAdyacencia:
    """
    Carga grafo ponderado (no dirigido, pesos positivos).
    Formato: 'Barrio1 Barrio2 Tiempo' por línea.
    """
    g = GrafoAdyacencia(no_dirigido=True)
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            u, v, w = parts[0], parts[1], float(parts[2])
            g.add_edge(u, v, w)
    return g


# ----------------------------------------------------
# HELPERS DE PARSEO DE CONSULTAS
# ----------------------------------------------------

def _parse_cortes(line: str) -> List[str]:
    """
    Busca 'cortes:' en la línea y devuelve lista de barrios (soporta coma o espacios).
    """
    low = line.lower()
    if "cortes:" not in low:
        return []
    rhs = line.split("cortes:", 1)[1]
    # reemplazo comas por espacios y spliteo
    cortes = [c.strip() for c in rhs.replace(",", " ").split() if c.strip()]
    return cortes


def _parse_plantas(line: str) -> List[str]:
    """
    Busca 'plantas:' en la línea. Si no está, toma el resto de tokens.
    """
    low = line.lower()
    if "plantas:" in low:
        rhs = line.split("plantas:", 1)[1]
        plantas = [p.strip() for p in rhs.replace(",", " ").split() if p.strip()]
        return plantas
    # fallback: tokens luego del comando PLANTAS
    tokens = line.strip().split()
    return tokens[1:] if len(tokens) > 1 else []


# ----------------------------------------------------
# ASIGNACIÓN DE PLANTAS (multi-origen)
# ----------------------------------------------------

def _asignar_plantas_bfs_multiorigen(g: GrafoAdyacencia, plantas: List[str]) -> Dict[str, Optional[str]]:
    """
    Asigna a cada barrio la planta más cercana en cantidad de aristas (no ponderado).
    En empates de distancia, elige lexicográficamente la planta con nombre menor.
    Implementación: Dijkstra/BFS multi-origen con cola de prioridad (dist, nodo, planta).
    """
    import heapq
    dist: Dict[str, int] = {}
    owner: Dict[str, str] = {}
    pq: List[Tuple[int, str, str]] = []

    # inicialización: cada planta a distancia 0 de sí misma
    for p in plantas:
        dist[p] = 0
        owner[p] = p
        heapq.heappush(pq, (0, p, p))

    while pq:
        d, u, planta = heapq.heappop(pq)
        if dist.get(u, float("inf")) < d or owner.get(u) != planta:
            continue
        for v in g.get_adjacency_list(u):
            nd = d + 1
            better = (nd < dist.get(v, float("inf"))) or (
                nd == dist.get(v, float("inf")) and planta < owner.get(v, "\uffff")
            )
            if better:
                dist[v] = nd
                owner[v] = planta
                heapq.heappush(pq, (nd, v, planta))

    # completar con None los barrios aislados que no se alcanzan
    asign = {v: owner.get(v, None) for v in g.vertices()}
    return asign


# ----------------------------------------------------
# PROCESAMIENTO DE CONSULTAS
# ----------------------------------------------------

def process_queries(
    queries_file: str,
    output_file: str,
    electric_graph: GrafoAdyacencia,
    road_graph: GrafoAdyacencia,
    water_graph: GrafoAdyacencia,
):
    """
    Lee el archivo de consultas y escribe las respuestas formateadas.
    Soporta tanto los nombres "cortos" como los del enunciado/consultas.txt:
      - COMPONENTES_CONEXOS ELECTRICA
      - ORDEN_FALLOS ELECTRICA
      - CAMINO_MINIMO <origen> <destino>
      - CAMINO_MINIMO_SIMULAR_CORTE {a,b,c} <origen> <destino>
      - CAMINO_RECOLECCION_BASURA
      - PLANTAS_ASIGNADAS p1 p2 ...
      - PUENTES_Y_ARTICULACIONES
    """
    outputs: List[str] = []

    with open(queries_file, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            tokens = line.split()
            op = tokens[0].upper()

            # ---------------- Eléctrica ----------------
            if op in ("COMPONENTES_CONEXOS", "COMPONENTES_ELECTRICA"):
                comps = ComponentesConexos.compute(electric_graph)
                outputs.append(format_componentes_conexos(comps))

            elif op in ("ORDEN_FALLOS", "ORDEN_FALLOS_ELECTRICA"):
                grados = [
                    (v, len(electric_graph.get_adjacency_list(v)))
                    for v in electric_graph.vertices()
                ]
                outputs.append(format_orden_fallos(grados))

            # ---------------- Vial (ponderado) ----------------
            elif op == "CAMINO_MINIMO":
                if len(tokens) < 3:
                    outputs.append(format_camino_minimo("?", "?", float("inf"), []))
                    continue
                origen, destino = tokens[1], tokens[2]
                dist, parent = Dijkstra.compute(road_graph, origen, destino)
                d = dist.get(destino, float("inf"))
                camino = Dijkstra.path(parent, destino)
                outputs.append(format_camino_minimo(origen, destino, d, camino))

            elif op in ("SIMULAR_CORTE", "CAMINO_MINIMO_SIMULAR_CORTE"):
                # Soportar dos formatos:
                # 1) SIMULAR_CORTE origen destino cortes: a,b,c
                # 2) CAMINO_MINIMO_SIMULAR_CORTE {a,b,c} origen destino   (como en consultas.txt)
                origen = destino = "?"
                cortes: List[str] = []

                # Formato con llaves: CAMINO_MINIMO_SIMULAR_CORTE {a,b,c} origen destino
                if len(tokens) >= 4 and tokens[1].startswith("{"):
                    cortes_token = tokens[1]
                    cortes_str = cortes_token.strip("{}")
                    cortes = [c.strip() for c in cortes_str.split(",") if c.strip()]
                    origen, destino = tokens[2], tokens[3]
                else:
                    # Formato original: SIMULAR_CORTE origen destino cortes: ...
                    if len(tokens) >= 3:
                        origen, destino = tokens[1], tokens[2]
                    cortes = _parse_cortes(line)

                if origen == "?" or destino == "?":
                    outputs.append(
                        format_simulacion_corte(origen, destino, cortes, float("inf"), [])
                    )
                    continue

                dist, parent = Dijkstra.compute(
                    road_graph, origen, destino, banned=set(cortes)
                )
                d = dist.get(destino, float("inf"))
                camino = Dijkstra.path(parent, destino)
                outputs.append(
                    format_simulacion_corte(origen, destino, cortes, d, camino)
                )

            elif op in ("RUTA_RECOLECCION", "CAMINO_RECOLECCION_BASURA"):
                ruta = Hierholzer.compute(road_graph)
                if not ruta:
                    comps = ComponentesConexos.compute(road_graph)
                    ruta = max(comps, key=len) if comps else []
                outputs.append(format_ruta_recoleccion(ruta))

            # ---------------- Hídrica ----------------
            elif op in ("PUENTES_Y_ARTICULACIONES", "PUENTES_ARTICULACIONES"):
                articulaciones, puentes = TarjanCriticos.compute(water_graph)
                outputs.append(
                    format_puentes_y_articulaciones(articulaciones, puentes)
                )

            elif op in ("PLANTAS", "PLANTAS_ASIGNADAS"):
                # PLANTAS_ASIGNADAS Saavedra VillaSoldati
                # o PLANTAS plantas: Saavedra, VillaSoldati
                plantas = _parse_plantas(line)
                asign = _asignar_plantas_bfs_multiorigen(water_graph, plantas)
                outputs.append(format_plantas_asignadas(plantas, asign))

            else:
                # Comando desconocido → comentario (te puede ayudar a debuggear)
                outputs.append(f"# Consulta desconocida: {line}\n")

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("\n".join(outputs))
