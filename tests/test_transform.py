"""
Teste pentru transform.py.
"""

from math import isclose

from transform import compute_scale, transform_layout, transform_point

TOL = 1e-9


def assert_close(actual, expected):
    assert isclose(actual, expected, abs_tol=TOL)


def test_default_scale():
    scale = compute_scale()
    expected = min((900 - 2 * 50) / (2 * 4000), (700 - 2 * 30) / (2 * 2800))
    assert_close(scale, expected)


def test_center():
    x, y = transform_point(0, 0)
    assert_close(x, 450)
    assert_close(y, 350)


def test_left_extreme():
    x, y = transform_point(-4000, 0)
    assert_close(x, 50)
    assert_close(y, 350)


def test_right_extreme():
    x, y = transform_point(4000, 0)
    assert_close(x, 850)
    assert_close(y, 350)


def test_top_extreme():
    x, y = transform_point(0, 1400)
    scale = compute_scale()
    assert_close(x, 450)
    assert_close(y, 350 - scale * 1400)


def test_bottom_extreme():
    x, y = transform_point(0, -1400)
    scale = compute_scale()
    assert_close(x, 450)
    assert_close(y, 350 + scale * 1400)


def test_transform_layout():
    layout = {"A": (-4000, 0), "B": (4000, 0)}
    transformed = transform_layout(layout)
    ax, ay = transformed["A"]
    bx, by = transformed["B"]
    assert_close(ax, 50)
    assert_close(ay, 350)
    assert_close(bx, 850)
    assert_close(by, 350)


def test_preserve_node_names():
    layout = {"A": (1, 2), "B": (3, 4), "C": (5, 6)}
    transformed = transform_layout(layout)
    assert set(transformed.keys()) == {"A", "B", "C"}


def test_deterministic():
    layout = {"A": (-100, 50), "B": (200, -70)}
    assert transform_layout(layout) == transform_layout(layout)


def test_custom_canvas_size():
    x, y = transform_point(0, 0, canvas_width=1200, canvas_height=800)
    assert_close(x, 600)
    assert_close(y, 400)


def test_custom_margins():
    scale = compute_scale(
        canvas_width=900, canvas_height=700, margin_x=100, margin_y=60
    )
    expected = min((900 - 200) / (2 * 4000), (700 - 120) / (2 * 2800))
    assert_close(scale, expected)


def test_same_scale_used_on_both_axes():
    """
    Verifică faptul că se utilizează
    aceeași scală pentru axele X și Y,
    fără deformarea elipsei.
    """
    scale = compute_scale()
    left_x, _ = transform_point(-2000, 0)
    right_x, _ = transform_point(2000, 0)
    _, top_y = transform_point(0, 1400)
    _, bottom_y = transform_point(0, -1400)

    assert_close(right_x - left_x, 4000 * scale)
    assert_close(bottom_y - top_y, 2800 * scale)