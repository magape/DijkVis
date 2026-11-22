"""
Teste pytest pentru modulul dijkstra.py.
"""

from math import inf

import pytest

from dijkstra import DijkstraSimulator
from graph import Graph


def test_single_node_graph():
    """Graf format dintr-un singur nod."""
    g = Graph()
    g.add_node("A")
    result = DijkstraSimulator(g).run("A")
    assert result.source_node == "A"
    assert result.final_state.distances["A"] == 0
    assert result.final_state.predecessors["A"] is None
    assert len(result.steps) == 1


def test_simple_graph():
    """Graful minim util pentru Dijkstra."""
    g = Graph()
    g.add_edge("A", "B", 5)
    result = DijkstraSimulator(g).run("A")
    assert result.final_state.distances["A"] == 0
    assert result.final_state.distances["B"] == 5
    assert result.final_state.predecessors["B"] == "A"


def test_shorter_indirect_path_found():
    """Verifica gasirea unui drum mai scurt printr-un nod intermediar."""
    g = Graph()
    g.add_edge("A", "B", 10)
    g.add_edge("A", "C", 2)
    g.add_edge("C", "B", 3)
    result = DijkstraSimulator(g).run("A")
    assert result.final_state.distances["B"] == 5
    assert result.final_state.predecessors["B"] == "C"


def test_unreachable_node():
    """Nod izolat."""
    g = Graph()
    g.add_edge("A", "B", 2)
    g.add_node("E")
    result = DijkstraSimulator(g).run("A")
    assert result.final_state.distances["E"] == inf
    assert result.final_state.predecessors["E"] is None


def test_disconnected_component():
    """Componenta neconexa trebuie ignorata."""
    g = Graph()
    g.add_edge("A", "B", 2)
    g.add_edge("B", "C", 3)
    g.add_edge("D", "E", 4)
    result = DijkstraSimulator(g).run("A")
    assert result.final_state.distances["D"] == inf
    assert result.final_state.distances["E"] == inf


def test_invalid_source():
    """Nod sursa inexistent."""
    g = Graph()
    g.add_node("A")
    with pytest.raises(ValueError):
        DijkstraSimulator(g).run("X")


def test_step_count():
    """Fiecare nod accesibil trebuie procesat."""
    g = Graph()
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 1)
    result = DijkstraSimulator(g).run("A")
    assert len(result.steps) == 3


def test_first_step_source_node():
    """Primul pas trebuie sa proceseze sursa."""
    g = Graph()
    g.add_edge("A", "B", 1)
    result = DijkstraSimulator(g).run("A")
    assert result.steps[0].current_node == "A"


def test_analysis_created_for_every_neighbor():
    """Trebuie generata cate o analiza pentru fiecare vecin."""
    g = Graph()
    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 2)
    g.add_edge("A", "D", 3)
    result = DijkstraSimulator(g).run("A")
    assert len(result.steps[0].analyses) == 3


def test_analysis_update_detected():
    """Verifica situatia in care are loc actualizarea distantei."""
    g = Graph()
    g.add_edge("A", "B", 4)
    result = DijkstraSimulator(g).run("A")
    analysis = result.steps[0].analyses[0]
    assert analysis.shorter_path_found is True
    assert analysis.distance_updated is True


def test_analysis_no_update():
    """Verifica situatia in care nu apare o imbunatatire a distantei."""
    g = Graph()
    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 10)
    result = DijkstraSimulator(g).run("A")

    step_b = next(s for s in result.steps if s.current_node == "B")
    analysis_c = next(a for a in step_b.analyses if a.neighbor == "C")
    assert analysis_c.shorter_path_found is False
    assert analysis_c.distance_updated is False


def test_state_before_after_consistency():
    """
    Starea de dupa un pas trebuie sa devina
    starea de inainte a pasului urmator.
    """
    g = Graph()
    g.add_edge("A", "B", 2)
    g.add_edge("B", "C", 3)
    result = DijkstraSimulator(g).run("A")

    for i in range(len(result.steps) - 1):
        current_step = result.steps[i]
        next_step = result.steps[i + 1]
        assert (
            current_step.state_after.distances
            == next_step.state_before.distances
        )
        assert (
            current_step.state_after.predecessors
            == next_step.state_before.predecessors
        )


def test_final_state_matches_last_step():
    """Rezultatul final trebuie sa coincida cu ultimul pas."""
    g = Graph()
    g.add_edge("A", "B", 2)
    g.add_edge("B", "C", 1)
    result = DijkstraSimulator(g).run("A")
    last_step = result.steps[-1]
    assert result.final_state.distances == last_step.state_after.distances
    assert (
        result.final_state.predecessors == last_step.state_after.predecessors
    )


def test_reconstruct_path():
    """Reconstruirea unui drum valid."""
    g = Graph()
    g.add_edge("A", "B", 2)
    g.add_edge("B", "C", 3)
    simulator = DijkstraSimulator(g)
    result = simulator.run("A")
    path = simulator.reconstruct_path(
        result.final_state.predecessors, "A", "C"
    )
    assert path == ["A", "B", "C"]


def test_reconstruct_unreachable_path():
    """Nod inaccesibil."""
    g = Graph()
    g.add_edge("A", "B", 2)
    g.add_node("E")
    simulator = DijkstraSimulator(g)
    result = simulator.run("A")
    path = simulator.reconstruct_path(
        result.final_state.predecessors, "A", "E"
    )
    assert path == []


def test_alphabetical_tie_break():
    """La egalitate trebuie ales nodul cu numele alfabetic mai mic."""
    g = Graph()
    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 1)
    result = DijkstraSimulator(g).run("A")
    assert result.steps[1].current_node == "B"


def test_candidate_distance_calculation():
    """Verifica formula: D(curent) + cost(curent, vecin)."""
    g = Graph()
    g.add_edge("A", "B", 7)
    result = DijkstraSimulator(g).run("A")
    assert result.steps[0].analyses[0].candidate_distance == 7


def test_predecessor_update():
    """Verifica actualizarea predecesorului."""
    g = Graph()
    g.add_edge("A", "B", 2)
    result = DijkstraSimulator(g).run("A")
    assert result.final_state.predecessors["B"] == "A"