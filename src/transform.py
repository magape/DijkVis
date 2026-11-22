"""
transform.py

Transformarea coordonatelor geometrice
în coordonate canvas.
"""

from layout import ELLIPSE_A, ELLIPSE_B

DEFAULT_CANVAS_WIDTH = 900
DEFAULT_CANVAS_HEIGHT = 700
DEFAULT_MARGIN_X = 50
DEFAULT_MARGIN_Y = 30


def compute_scale(
    canvas_width: int = DEFAULT_CANVAS_WIDTH,
    canvas_height: int = DEFAULT_CANVAS_HEIGHT,
    margin_x: int = DEFAULT_MARGIN_X,
    margin_y: int = DEFAULT_MARGIN_Y,
) -> float:
    """
    Calculează scara unică utilizată
    pentru transformare.
    """
    usable_width = canvas_width - 2 * margin_x
    usable_height = canvas_height - 2 * margin_y
    scale_x = usable_width / (2 * ELLIPSE_A)
    scale_y = usable_height / (2 * ELLIPSE_B)

    return min(scale_x, scale_y)


def transform_point(
    x: float,
    y: float,
    canvas_width: int = DEFAULT_CANVAS_WIDTH,
    canvas_height: int = DEFAULT_CANVAS_HEIGHT,
    margin_x: int = DEFAULT_MARGIN_X,
    margin_y: int = DEFAULT_MARGIN_Y,
) -> tuple[float, float]:
    """
    Transformă un punct geometric
    într-un punct canvas.
    """
    scale = compute_scale(
        canvas_width,
        canvas_height,
        margin_x,
        margin_y,
    )
    cx = canvas_width / 2
    cy = canvas_height / 2

    return (
        cx + scale * x,
        cy - scale * y,
    )


def transform_layout(
    layout: dict[str, tuple[float, float]],
    canvas_width: int = DEFAULT_CANVAS_WIDTH,
    canvas_height: int = DEFAULT_CANVAS_HEIGHT,
    margin_x: int = DEFAULT_MARGIN_X,
    margin_y: int = DEFAULT_MARGIN_Y,
) -> dict[str, tuple[float, float]]:
    """
    Transformă toate punctele unui layout.
    """
    return {
        node: transform_point(
            x,
            y,
            canvas_width,
            canvas_height,
            margin_x,
            margin_y,
        )
        for node, (x, y) in layout.items()
    }