"""
Graph analysis module for Buenos Aires city networks.
Students must implement all functions marked with TODO.
"""

from src.output import (
    format_componentes_conexos,
    format_orden_fallos,
    format_camino_minimo,
    format_simulacion_corte,
    format_ruta_recoleccion,
    format_plantas_asignadas,
    format_puentes_y_articulaciones,
)

# -----------------------------
# Graph loading
# -----------------------------

def load_graph(path):
    """
    Load a simple graph from a file.

    Args:
        path: File path

    Returns:
        Adjacency dictionary {node: [neighbors]}
    """
    # TODO: Implement
    pass


def load_weighted_graph(path):
    """
    Load a weighted graph from a file.

    Args:
        path: File path

    Returns:
        Adjacency dictionary {node: [(neighbor, weight), ...]}
    """
    # TODO: Implement
    pass


def process_queries(queries_file, output_file, electric_graph, road_graph, water_graph):
    """
    Process queries from file and generate output.

    Args:
        queries_file: Path to queries file
        output_file: Path to output file
        electric_graph: Electric network graph
        road_graph: Road network graph
        water_graph: Water network graph
    """
    # TODO: Implement
    pass
