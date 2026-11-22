"""
Teste pytest pentru clasa Graph.

Rulare:

    pytest

sau:

    pytest -v
"""

import pytest

from graph import Graph


def assert_graph_invariant(graph):
    """
    Verifica invariantul principal al clasei Graph.

    Orice nod care apare ca destinatie
    intr-o muchie trebuie sa existe
    si ca nod al grafului.
    """
    for source in graph.nodes():
        for target in graph.neighbors(source):
            assert graph.has_node(target)


def test_empty_graph():
    """Verifica starea initiala a grafului."""
    g = Graph()
    assert g.node_count() == 0
    assert g.edge_count() == 0
    assert g.nodes() == []
    assert g.edges() == []
    assert_graph_invariant(g)


def test_add_node():
    """Verifica adaugarea unui nod."""
    g = Graph()
    g.add_node("A")
    assert g.has_node("A")
    assert g.node_count() == 1
    assert_graph_invariant(g)


def test_add_duplicate_node():
    """Adaugarea repetata a aceluiasi nod nu trebuie sa creeze duplicate."""
    g = Graph()
    g.add_node("A")
    g.add_node("A")
    g.add_node("A")
    assert g.node_count() == 1
    assert_graph_invariant(g)


def test_add_edge_creates_nodes():
    """Adaugarea unei muchii creeaza automat nodurile implicate."""
    g = Graph()
    g.add_edge("A", "B", 3)
    assert g.has_node("A")
    assert g.has_node("B")
    assert g.has_edge("A", "B")
    assert g.weight("A", "B") == 3
    assert_graph_invariant(g)


def test_add_multiple_edges():
    """Verifica adaugarea mai multor muchii."""
    g = Graph()
    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "D", 3)
    assert g.edge_count() == 3
    assert_graph_invariant(g)


def test_neighbors():
    """Verifica returnarea vecinilor."""
    g = Graph()
    g.add_edge("A", "B", 5)
    g.add_edge("A", "C", 7)
    assert g.neighbors("A") == {"B": 5, "C": 7}
    assert_graph_invariant(g)


def test_neighbors_returns_copy():
    """
    Modificarea rezultatului returnat de neighbors() nu trebuie sa afecteze
    structura interna a grafului.
    """
    g = Graph()
    g.add_edge("A", "B", 3)
    neighbors = g.neighbors("A")
    neighbors["C"] = 100
    assert not g.has_node("C")
    assert_graph_invariant(g)


def test_duplicate_edge_updates_weight():
    """Muchiile duplicate actualizeaza ponderea."""
    g = Graph()
    g.add_edge("A", "B", 3)
    g.add_edge("A", "B", 10)
    assert g.weight("A", "B") == 10
    assert g.edge_count() == 1
    assert_graph_invariant(g)


def test_remove_edge():
    """Verifica eliminarea unei muchii."""
    g = Graph()
    g.add_edge("A", "B", 3)
    g.remove_edge("A", "B")
    assert not g.has_edge("A", "B")
    assert g.edge_count() == 0
    assert_graph_invariant(g)


def test_remove_nonexistent_edge():
    """Eliminarea unei muchii inexistente nu trebuie sa genereze eroare."""
    g = Graph()
    g.remove_edge("A", "B")
    assert_graph_invariant(g)


def test_remove_node():
    """Verifica eliminarea unui nod."""
    g = Graph()
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 2)
    g.add_edge("C", "A", 3)
    g.remove_node("B")
    assert not g.has_node("B")
    assert not g.has_edge("A", "B")
    assert not g.has_edge("B", "C")
    assert_graph_invariant(g)


def test_remove_nonexistent_node():
    """Eliminarea unui nod inexistent nu trebuie sa genereze eroare."""
    g = Graph()
    g.remove_node("X")
    assert_graph_invariant(g)


def test_nodes_are_sorted():
    """Nodurile trebuie returnate in ordine alfabetica."""
    g = Graph()
    for node in ("D", "A", "C", "B"):
        g.add_node(node)
    assert g.nodes() == ["A", "B", "C", "D"]
    assert_graph_invariant(g)


def test_uppercase_normalization():
    """Verifica transformarea interna a numelor nodurilor in majuscule."""
    g = Graph()
    g.add_edge("a", "b", 4)
    assert g.nodes() == ["A", "B"]
    assert g.has_node("A")
    assert g.has_node("a")
    assert g.has_node("B")
    assert g.has_node("b")
    assert_graph_invariant(g)


def test_weight_zero_allowed():
    """Ponderea zero este permisa."""
    g = Graph()
    g.add_edge("A", "B", 0)
    assert g.weight("A", "B") == 0
    assert_graph_invariant(g)


def test_negative_weight_not_allowed():
    """Ponderile negative trebuie respinse."""
    g = Graph()
    with pytest.raises(ValueError):
        g.add_edge("A", "B", -1)


def test_non_integer_weight_not_allowed():
    """Ponderile trebuie sa fie intregi."""
    g = Graph()
    with pytest.raises(TypeError):
        g.add_edge("A", "B", 3.5)


def test_empty_node_name():
    """Numele vid nu este permis."""
    g = Graph()
    with pytest.raises(ValueError):
        g.add_node("")


def test_blank_node_name():
    """Numele format doar din spatii nu este permis."""
    g = Graph()
    with pytest.raises(ValueError):
        g.add_node("   ")


def test_non_string_node():
    """Numele nodului trebuie sa fie text."""
    g = Graph()
    with pytest.raises(TypeError):
        g.add_node(123)


def test_weight_nonexistent_edge():
    """Nu putem obtine ponderea unei muchii inexistente."""
    g = Graph()
    with pytest.raises(ValueError):
        g.weight("A", "B")


def test_neighbors_nonexistent_node():
    """Nu putem obtine vecinii unui nod inexistent."""
    g = Graph()
    with pytest.raises(ValueError):
        g.neighbors("X")


def test_clear_graph():
    """Verifica golirea completa a grafului."""
    g = Graph()
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 2)
    g.clear()
    assert g.node_count() == 0
    assert g.edge_count() == 0
    assert_graph_invariant(g)


def test_large_graph_invariant():
    """Verifica invariantul pe un graf mai mare."""
    g = Graph()
    edges = [
        ("A", "B", 1),
        ("B", "C", 2),
        ("C", "D", 3),
        ("D", "E", 4),
        ("E", "F", 5),
        ("F", "G", 6),
        ("G", "H", 7),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    assert_graph_invariant(g)


def test_all_internal_nodes_are_uppercase():
    """Toate nodurile sunt scrise cu majuscule."""
    g = Graph()
    g.add_edge("a", "b", 4)
    g.add_edge("c", "d", 5)
    assert all(node == node.upper() for node in g.nodes())