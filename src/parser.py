"""
parser.py

Transforma reprezentarea textuala a unui graf
intr-un obiect Graph.
"""

import re

from graph import Graph

EDGE_PATTERN = re.compile(r"^([A-Z])([A-Z])([0-9]+)$")
NODE_PATTERN = re.compile(r"^[A-Z]$")


def parse_graph(text: str, undirected: bool = False) -> Graph:
    """
    Construieste un obiect Graph dintr-un sir.

    Exemple:

        AB2, AC4, BC1

        AB2, AC4, E
    """
    if not isinstance(text, str):
        raise TypeError("Textul grafului trebuie sa fie sir de caractere.")

    text = text.strip()
    if not text:
        raise ValueError("Graful este gol.")

    graph = Graph()
    text = text.upper()
    tokens = [token.strip() for token in text.split(",")]

    for token in tokens:
        if not token:
            raise ValueError("Element gol in lista.")

        edge_match = EDGE_PATTERN.fullmatch(token)
        if edge_match:
            source = edge_match.group(1)
            target = edge_match.group(2)
            weight = int(edge_match.group(3))

            if source == target:
                raise ValueError(
                    f"Muchiile de forma {token} nu sunt permise."
                )

            graph.add_edge(source, target, weight)
            if undirected:
                graph.add_edge(target, source, weight)

            continue

        node_match = NODE_PATTERN.fullmatch(token)
        if node_match:
            graph.add_node(token)
            continue

        if len(token) == 2:
            raise ValueError(f"Muchia '{token}' nu contine o pondere.")

        raise ValueError(f"Format invalid: '{token}'")

    return graph