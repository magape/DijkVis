"""
Teste de integrare intre:

    graph.py
si

    dijkstra.py

Aceste teste verifica functionarea
comuna a celor doua module.
"""

from math import inf

from graph import Graph
from dijkstra import DijkstraSimulator


def test_classic_example_directed():
    """
    Exemplu orientat.

    Muchii:

        A -> B = 7
        A -> C = 9
        A -> F = 14

        B -> C = 10
        B -> D = 15

        C -> D = 11
        C -> F = 2

        D -> E = 6

        E -> F = 9

    Distante minime din A:

        A = 0
        B = 7
        C = 9
        D = 20
        E = 26
        F = 11
    """

    g = Graph()

    g.add_edge("A", "B", 7)
    g.add_edge("A", "C", 9)
    g.add_edge("A", "F", 14)

    g.add_edge("B", "C", 10)
    g.add_edge("B", "D", 15)

    g.add_edge("C", "D", 11)
    g.add_edge("C", "F", 2)

    g.add_edge("D", "E", 6)

    g.add_edge("E", "F", 9)

    result = DijkstraSimulator(g).run("A")

    expected = {
        "A": 0,
        "B": 7,
        "C": 9,
        "D": 20,
        "E": 26,
        "F": 11,
    }

    assert result.final_state.distances == expected


def test_classic_example_undirected():
    """
    Exemplul clasic neorientat.

    Fiecare muchie este adaugata
    in ambele sensuri.

    Distante minime din A:

        A = 0
        B = 7
        C = 9
        D = 20
        E = 20
        F = 11
    """

    g = Graph()

    edges = [
        ("A", "B", 7),
        ("A", "C", 9),
        ("A", "F", 14),
        ("B", "C", 10),
        ("B", "D", 15),
        ("C", "D", 11),
        ("C", "F", 2),
        ("D", "E", 6),
        ("E", "F", 9),
    ]

    for source, target, weight in edges:

        g.add_edge(source, target, weight)
        g.add_edge(target, source, weight)

    result = DijkstraSimulator(g).run("A")

    expected = {
        "A": 0,
        "B": 7,
        "C": 9,
        "D": 20,
        "E": 20,
        "F": 11,
    }

    assert result.final_state.distances == expected


def test_graph_is_directed():
    """
    Verifica faptul ca Graph este orientat.

    A -> B nu implica automat
    existenta muchiei B -> A.
    """

    g = Graph()

    g.add_edge("A", "B", 5)

    result = DijkstraSimulator(g).run("B")

    assert result.final_state.distances["A"] == inf


def test_bidirectional_edges_simulate_undirected_graph():
    """
    Un graf neorientat se obtine
    prin introducerea muchiilor
    in ambele sensuri.
    """

    g = Graph()

    g.add_edge("A", "B", 5)
    g.add_edge("B", "A", 5)

    result = DijkstraSimulator(g).run("B")

    assert result.final_state.distances["A"] == 5


def test_isolated_node():
    """
    Nod izolat.
    """

    g = Graph()

    g.add_edge("A", "B", 3)

    g.add_node("E")

    result = DijkstraSimulator(g).run("A")

    assert result.final_state.distances["E"] == inf

    assert result.final_state.predecessors["E"] is None


def test_disconnected_component():
    """
    Componenta neconectata.
    """

    g = Graph()

    g.add_edge("A", "B", 2)
    g.add_edge("B", "C", 3)

    g.add_edge("D", "E", 4)

    result = DijkstraSimulator(g).run("A")

    assert result.final_state.distances["D"] == inf
    assert result.final_state.distances["E"] == inf


def test_shorter_indirect_path():
    """
    Drumul indirect trebuie ales
    daca este mai scurt.
    """

    g = Graph()

    g.add_edge("A", "B", 10)

    g.add_edge("A", "C", 2)

    g.add_edge("C", "B", 3)

    result = DijkstraSimulator(g).run("A")

    assert result.final_state.distances["B"] == 5

    assert result.final_state.predecessors["B"] == "C"


def test_step_count_equals_accessible_nodes():
    """
    Fiecare nod accesibil trebuie
    procesat exact o data.
    """

    g = Graph()

    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 2)

    g.add_node("E")

    result = DijkstraSimulator(g).run("A")

    assert len(result.steps) == 3


def test_before_after_consistency():
    """
    Starea de dupa un pas trebuie
    sa fie identica cu starea de dinainte
    a pasului urmator.
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
            ==
            next_step.state_before.distances
        )

        assert (
            current_step.state_after.predecessors
            ==
            next_step.state_before.predecessors
        )

        assert (
            current_step.state_after.visited
            ==
            next_step.state_before.visited
        )


def test_analyses_match_neighbor_count():
    """
    Fiecare vecin trebuie sa produca
    exact o analiza.
    """

    g = Graph()

    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 2)
    g.add_edge("A", "D", 3)

    result = DijkstraSimulator(g).run("A")

    first_step = result.steps[0]

    expected_count = len(
        g.neighbors(first_step.current_node)
    )

    assert len(first_step.analyses) == expected_count


def test_reconstruct_path():
    """
    Reconstruirea unui drum minim.
    """

    g = Graph()

    g.add_edge("A", "B", 2)
    g.add_edge("B", "C", 3)
    g.add_edge("C", "D", 4)

    simulator = DijkstraSimulator(g)

    result = simulator.run("A")

    path = simulator.reconstruct_path(
        result.final_state.predecessors,
        "A",
        "D"
    )

    assert path == ["A", "B", "C", "D"]


def test_unreachable_path():
    """
    Drumul catre un nod inaccesibil
    trebuie sa fie vid.
    """

    g = Graph()

    g.add_edge("A", "B", 1)

    g.add_node("X")

    simulator = DijkstraSimulator(g)

    result = simulator.run("A")

    path = simulator.reconstruct_path(
        result.final_state.predecessors,
        "A",
        "X"
    )

    assert path == []


def test_alphabetical_tie_break():
    """
    La egalitate trebuie ales nodul
    cu numele alfabetic mai mic.
    """

    g = Graph()

    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 1)

    result = DijkstraSimulator(g).run("A")

    assert result.steps[1].current_node == "B"