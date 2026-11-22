"""
Teste pentru funcțiile geometrice din renderer.py.
"""

from math import isclose

from renderer import (
    NODE_RADIUS,
    compute_edge_endpoints,
    compute_weight_position,
    edge_key,
)

TOL = 1e-9


def assert_close(actual, expected):
    assert isclose(actual, expected, abs_tol=TOL)


def test_edge_key_is_order_independent():
    assert edge_key("A", "B") == edge_key("B", "A")


def test_horizontal_edge_endpoints():
    sx, sy, ex, ey = compute_edge_endpoints(0, 0, 100, 0)
    assert_close(sx, NODE_RADIUS)
    assert_close(sy, 0)
    assert_close(ex, 100 - NODE_RADIUS)
    assert_close(ey, 0)


def test_vertical_edge_endpoints():
    sx, sy, ex, ey = compute_edge_endpoints(0, 0, 0, 100)
    assert_close(sx, 0)
    assert_close(ex, 0)
    assert_close(sy, NODE_RADIUS)
    assert_close(ey, 100 - NODE_RADIUS)


def test_diagonal_edge_endpoints_are_shorter():
    sx, sy, ex, ey = compute_edge_endpoints(0, 0, 100, 100)
    assert (ex - sx) < 100
    assert (ey - sy) < 100


def test_zero_length_edge():
    assert compute_edge_endpoints(10, 20, 10, 20) == (10, 20, 10, 20)


def test_weight_position_horizontal():
    x, y = compute_weight_position(10, 50, 110, 50)
    assert_close(x, 60)
    assert_close(y, 50)


def test_weight_position_vertical():
    x, y = compute_weight_position(50, 10, 50, 110)
    assert_close(x, 50)
    assert_close(y, 60)


def test_weight_position_diagonal():
    x, y = compute_weight_position(10, 20, 30, 40)
    assert_close(x, 20)
    assert_close(y, 30)


def test_weight_position_is_midpoint():
    x, y = compute_weight_position(-10, -30, 30, 10)
    assert_close(x, 10)
    assert_close(y, -10)