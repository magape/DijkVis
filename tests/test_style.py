"""
Teste pentru style.py.
"""

from math import inf

from dijkstra import DijkstraState, NeighborAnalysis, Step
from style import (
    ACTIVE_EDGE_STYLE,
    CURRENT_NODE_STYLE,
    NORMAL_EDGE_STYLE,
    PREDECESSOR_EDGE_STYLE,
    SOURCE_NODE_STYLE,
    UNREACHABLE_NODE_STYLE,
    UNVISITED_NODE_STYLE,
    VISITED_NODE_STYLE,
    edge_key,
    get_edge_style,
    get_node_style,
)


def build_step():
    before = DijkstraState(
        distances={"A": 0, "B": inf, "C": inf},
        predecessors={"A": None, "B": None, "C": None},
        visited=set(),
    )
    after = DijkstraState(
        distances={"A": 0, "B": 5, "C": inf},
        predecessors={"A": None, "B": "A", "C": None},
        visited={"A"},
    )
    analysis = NeighborAnalysis(
        current_node="A",
        neighbor="B",
        edge_weight=5,
        current_node_distance=0,
        old_neighbor_distance=inf,
        candidate_distance=5,
        shorter_path_found=True,
        distance_updated=True,
        old_predecessor=None,
        new_predecessor="A",
    )
    return Step(
        step_number=1,
        current_node="A",
        state_before=before,
        analyses=[analysis],
        state_after=after,
    )


def test_edge_key_is_order_independent():
    assert edge_key("A", "B") == edge_key("B", "A")


def test_current_has_highest_priority():
    assert get_node_style("A", "A", build_step()) == CURRENT_NODE_STYLE


def test_source_style():
    assert get_node_style("B", "B", build_step()) == SOURCE_NODE_STYLE


def test_unreachable_style():
    assert get_node_style("C", "A", build_step()) == UNREACHABLE_NODE_STYLE


def test_visited_style():
    assert get_node_style("A", "B", build_step()) == CURRENT_NODE_STYLE


def test_unvisited_style():
    step = build_step()
    step.state_after.visited.clear()
    assert get_node_style("B", "A", step) == UNVISITED_NODE_STYLE


def test_active_edge_style():
    assert get_edge_style("A", "B", build_step()) == ACTIVE_EDGE_STYLE


def test_active_has_priority_over_predecessor():
    assert get_edge_style("B", "A", build_step()) == ACTIVE_EDGE_STYLE


def test_predecessor_edge_style():
    step = build_step()
    step.analyses.clear()
    assert get_edge_style("A", "B", step) == PREDECESSOR_EDGE_STYLE


def test_normal_edge_style():
    assert get_edge_style("A", "C", build_step()) == NORMAL_EDGE_STYLE


def test_deterministic():
    step = build_step()
    assert get_node_style("A", "A", step) == get_node_style("A", "A", step)
    assert get_edge_style("A", "B", step) == get_edge_style("A", "B", step)