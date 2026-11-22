"""
Teste pentru layout.py.
"""

from math import isclose, pi

import pytest

from graph import Graph
from layout import ELLIPSE_A, ELLIPSE_B, compute_angles, compute_layout

TOL = 1e-9


def assert_close(actual, expected):
    assert isclose(actual, expected, abs_tol=TOL)


@pytest.mark.parametrize(
    "node_count, expected",
    [
        (1, [-pi]),
        (2, [-pi, 0]),
        (3, [-pi, -pi / 3, -5 * pi / 3]),
        (4, [-pi, -pi / 2, -3 * pi / 2, 0]),
        (5, [-pi, -3 * pi / 5, -7 * pi / 5, -pi / 5, -9 * pi / 5]),
        (
            6,
            [-pi, -2 * pi / 3, -4 * pi / 3, -pi / 3, -5 * pi / 3, 0],
        ),
        (
            7,
            [
                -pi,
                -5 * pi / 7,
                -9 * pi / 7,
                -3 * pi / 7,
                -11 * pi / 7,
                -pi / 7,
                -13 * pi / 7,
            ],
        ),
        (
            8,
            [
                -pi,
                -3 * pi / 4,
                -5 * pi / 4,
                -pi / 2,
                -3 * pi / 2,
                -pi / 4,
                -7 * pi / 4,
                0,
            ],
        ),
    ],
)
def test_compute_angles(node_count, expected):
    angles = compute_angles(node_count)
    assert len(angles) == len(expected)
    for actual, exp in zip(angles, expected):
        assert_close(actual, exp)


@pytest.mark.parametrize("node_count", [1, 2, 3, 4, 5, 6, 7, 8])
def test_layout_contains_all_nodes(node_count):
    g = Graph()
    for i in range(node_count):
        g.add_node(chr(ord("A") + i))

    layout = compute_layout(g)
    assert len(layout) == node_count
    for i in range(node_count):
        assert chr(ord("A") + i) in layout


@pytest.mark.parametrize("node_count", [2, 3, 4, 5, 6, 7, 8])
def test_points_belong_to_ellipse(node_count):
    g = Graph()
    for i in range(node_count):
        g.add_node(chr(ord("A") + i))

    layout = compute_layout(g)
    for x, y in layout.values():
        lhs = (x * x) / (ELLIPSE_A**2) + (y * y) / (ELLIPSE_B**2)
        assert isclose(lhs, 1.0, abs_tol=TOL)


def test_single_node_centered():
    g = Graph()
    g.add_node("A")
    assert compute_layout(g) == {"A": (0.0, 0.0)}


def test_layout_is_deterministic():
    g = Graph()
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 1)
    assert compute_layout(g) == compute_layout(g)


def test_nodes_are_sorted():
    g = Graph()
    for node in "DACB":
        g.add_node(node)
    layout = compute_layout(g)
    assert list(layout.keys()) == ["A", "B", "C", "D"]


def test_layout_for_four_nodes():
    g = Graph()
    for node in "ABCD":
        g.add_node(node)
    layout = compute_layout(g)
    assert_close(layout["A"][0], -ELLIPSE_A)
    assert_close(layout["D"][0], ELLIPSE_A)
    assert_close(layout["B"][1], -ELLIPSE_B)
    assert_close(layout["C"][1], ELLIPSE_B)


def test_layout_for_two_nodes():
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    layout = compute_layout(g)
    assert_close(layout["A"][0], -ELLIPSE_A)
    assert_close(layout["B"][0], ELLIPSE_A)
    assert_close(layout["A"][1], 0.0)
    assert_close(layout["B"][1], 0.0)