"""
Teste pytest pentru parser.py.
"""

import pytest

from parser import parse_graph


def test_parse_single_edge():
    graph = parse_graph("AB2")
    assert graph.has_edge("A", "B")
    assert graph.weight("A", "B") == 2


def test_parse_multiple_edges():
    graph = parse_graph("AB2, AC4, BC1")
    assert graph.edge_count() == 3
    assert graph.weight("A", "B") == 2
    assert graph.weight("A", "C") == 4
    assert graph.weight("B", "C") == 1


def test_parse_isolated_node():
    graph = parse_graph("E")
    assert graph.has_node("E")
    assert graph.edge_count() == 0


def test_parse_mixed_graph():
    graph = parse_graph("AB2, AC4, E")
    assert graph.has_node("E")
    assert graph.has_edge("A", "B")
    assert graph.has_edge("A", "C")


def test_parse_undirected():
    graph = parse_graph("AB5", undirected=True)
    assert graph.has_edge("A", "B")
    assert graph.has_edge("B", "A")


def test_parse_directed():
    graph = parse_graph("AB5", undirected=False)
    assert graph.has_edge("A", "B")
    assert not graph.has_edge("B", "A")


def test_parse_lowercase():
    graph = parse_graph("ab2, ac4, e")
    assert graph.has_node("A")
    assert graph.has_node("C")
    assert graph.has_node("E")


def test_duplicate_edge():
    graph = parse_graph("AB2, AB7")
    assert graph.weight("A", "B") == 7


def test_duplicate_node():
    graph = parse_graph("A, A, A")
    assert graph.node_count() == 1


def test_missing_weight():
    with pytest.raises(ValueError):
        parse_graph("AB")


def test_invalid_weight_text():
    with pytest.raises(ValueError):
        parse_graph("ABX")


def test_invalid_weight_negative():
    with pytest.raises(ValueError):
        parse_graph("AB-2")


def test_invalid_weight_decimal():
    with pytest.raises(ValueError):
        parse_graph("AB3.5")


def test_invalid_node_name():
    with pytest.raises(ValueError):
        parse_graph("1")


def test_invalid_edge_name():
    with pytest.raises(ValueError):
        parse_graph("1A2")


def test_invalid_token():
    with pytest.raises(ValueError):
        parse_graph("ABCDE")


def test_self_loop():
    with pytest.raises(ValueError):
        parse_graph("AA5")


def test_empty_string():
    with pytest.raises(ValueError):
        parse_graph("")


def test_blank_string():
    with pytest.raises(ValueError):
        parse_graph("      ")


def test_spaces_are_ignored():
    graph = parse_graph(" AB2 , AC4 , E ")
    assert graph.has_edge("A", "B")
    assert graph.has_edge("A", "C")
    assert graph.has_node("E")


def test_zero_weight_allowed():
    graph = parse_graph("AB0")
    assert graph.weight("A", "B") == 0