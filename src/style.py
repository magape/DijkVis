"""
style.py
"""

from dataclasses import dataclass
from math import inf


@dataclass(frozen=True)
class NodeStyle:
    fill_color: str
    outline_color: str
    outline_width: int


@dataclass(frozen=True)
class EdgeStyle:
    color: str
    width: int


CURRENT_NODE_STYLE = NodeStyle("orange", "black", 3)
SOURCE_NODE_STYLE = NodeStyle("lightgreen", "black", 2)
UNREACHABLE_NODE_STYLE = NodeStyle("lightgray", "gray", 2)
VISITED_NODE_STYLE = NodeStyle("lightblue", "black", 2)
UNVISITED_NODE_STYLE = NodeStyle("white", "black", 1)

ACTIVE_EDGE_STYLE = EdgeStyle("orange", 3)
PREDECESSOR_EDGE_STYLE = EdgeStyle("lightgreen", 2)
NORMAL_EDGE_STYLE = EdgeStyle("lightgray", 1)


def edge_key(source: str, target: str) -> tuple[str, str]:
    return (source, target) if source <= target else (target, source)


def get_node_style(node: str, source_node: str, step) -> NodeStyle:
    state = step.state_after
    if node == step.current_node:
        return CURRENT_NODE_STYLE
    if node == source_node:
        return SOURCE_NODE_STYLE
    if state.distances[node] == inf:
        return UNREACHABLE_NODE_STYLE
    if node in state.visited:
        return VISITED_NODE_STYLE
    return UNVISITED_NODE_STYLE


def get_edge_style(source: str, target: str, step) -> EdgeStyle:
    key = edge_key(source, target)
    active_edges = {
        edge_key(a.current_node, a.neighbor) for a in step.analyses
    }
    if key in active_edges:
        return ACTIVE_EDGE_STYLE

    predecessor_edges = {
        edge_key(pred, node)
        for node, pred in step.state_after.predecessors.items()
        if pred is not None
    }
    if key in predecessor_edges:
        return PREDECESSOR_EDGE_STYLE

    return NORMAL_EDGE_STYLE