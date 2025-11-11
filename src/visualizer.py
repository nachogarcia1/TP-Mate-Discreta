"""
Graph visualization module.
Generates .dot files for visualization with Graphviz.
"""

from pathlib import Path

# --- helpers de introspección/adaptación ---

def _is_graph_class(g) -> bool:
    # Detecta objetos tipo GrafoAdyacencia sin importar el módulo
    return hasattr(g, "vertices") and hasattr(g, "get_adjacency_list")

def _nodes(g):
    if _is_graph_class(g):
        return list(g.vertices())
    # dict de adyacencia
    return list(g.keys())

def _neighbors_simple(g, u):
    if _is_graph_class(g):
        return list(g.get_adjacency_list(u))
    # dict: {u: [v,...]} o {u: [(v,w),...]} -> normalizamos
    neis = g[u]
    if not neis:
        return []
    if isinstance(neis[0], tuple):
        return [v for v, _ in neis]
    return list(neis)

def _weight(g, u, v):
    if _is_graph_class(g):
        return g.get_weight(u, v)
    # dict: puede ser simple o ponderado
    for item in g[u]:
        if isinstance(item, tuple):
            vv, w = item
            if vv == v:
                return w
        else:
            if item == v:
                return 1.0
    return None

def _q(name: str) -> str:
    # Quote seguro para DOT (escapa comillas internas)
    return '"' + str(name).replace('"', '\\"') + '"'


def draw_simple_graph(g, filename, title="Graph"):
    """
    Generates a .dot file for a simple (unweighted) graph.

    Args:
        g: GrafoAdyacencia o dict {node: [neighbors]}
    """
    nodes = sorted(_nodes(g))
    lines = []
    lines.append("graph {")
    lines.append(f"  label={_q(title)};")
    lines.append("  labelloc=top;")
    lines.append("  labeljust=left;")
    lines.append("  node [shape=circle];")
    lines.append("")

    # Nodos (incluye aislados)
    for u in nodes:
        lines.append(f"  {_q(u)};")

    # Aristas (evitar duplicados)
    added = set()
    for u in nodes:
        for v in _neighbors_simple(g, u):
            if u == v:
                continue
            edge = frozenset({u, v})
            if edge in added:
                continue
            lines.append(f"  {_q(u)} -- {_q(v)};")
            added.add(edge)

    lines.append("}")
    Path(filename).write_text("\n".join(lines), encoding="utf-8")
    return Path(filename)


def draw_weighted_graph(g, filename, title="Weighted Graph"):
    """
    Generates a .dot file for a weighted graph.

    Args:
        g: GrafoAdyacencia o dict {node: [(neighbor, weight)]} o {node: [neighbor]}
    """
    nodes = sorted(_nodes(g))
    lines = []
    lines.append("graph {")
    lines.append(f"  label={_q(title)};")
    lines.append("  labelloc=top;")
    lines.append("  labeljust=left;")
    lines.append("  node [shape=circle];")
    lines.append("")

    for u in nodes:
        lines.append(f"  {_q(u)};")

    added = set()
    for u in nodes:
        for v in _neighbors_simple(g, u):
            if u == v:
                continue
            edge = frozenset({u, v})
            if edge in added:
                continue
            w = _weight(g, u, v)
            if w is None:
                w = 1.0
            weight_str = str(int(w)) if float(w).is_integer() else str(w)
            lines.append(f"  {_q(u)} -- {_q(v)} [label={_q(weight_str)}];")
            added.add(edge)

    lines.append("}")
    Path(filename).write_text("\n".join(lines), encoding="utf-8")
    return Path(filename)


def draw_connected_components(g, components, filename, title="Connected Components"):
    # Si querés colorear por componente, lo podemos agregar; por ahora reusa simple.
    return draw_simple_graph(g, filename, title)


def visualize_graphs(electric_graph, road_graph, water_graph, output_dir="resources"):
    """
    Genera .dot para los tres grafos. Acepta GrafoAdyacencia o dicts.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    results = {}

    print("📊 Generating graph .dot files...")

    print("  → Generating electrico.dot...")
    path = draw_simple_graph(
        electric_graph, f"{output_dir}/electrico.dot", "Red Eléctrica"
    )
    results["electric"] = path
    print(f"    ✓ Saved: {path}")

    print("  → Generating vial.dot...")
    path = draw_weighted_graph(
        road_graph, f"{output_dir}/vial.dot", "Red Vial"
    )
    results["road"] = path
    print(f"    ✓ Saved: {path}")

    print("  → Generating hidrico.dot...")
    path = draw_simple_graph(
        water_graph, f"{output_dir}/hidrico.dot", "Red Hídrica"
    )
    results["water"] = path
    print(f"    ✓ Saved: {path}")

    print(f"✓ .dot files generated ({len(results)} graphs)")
    print("  To visualize: dot -Tpng resources/electrico.dot -o resources/electrico.png")
    return results
