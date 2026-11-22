"""
renderer.py

Desenarea grafului pe un Tkinter Canvas.
"""

from math import hypot, inf

from style import get_edge_style, get_node_style

NODE_RADIUS = 25
DISTANCE_OFFSET_X = 9
DISTANCE_OFFSET_Y = NODE_RADIUS + 10
WEIGHT_OFFSET_X = 0
WEIGHT_OFFSET_Y = 0

NODE_FONT = ("Segoe UI", 16, "bold")
DISTANCE_FONT = ("Segoe UI", 14, "bold")
WEIGHT_FONT = ("Segoe UI", 14, "bold")

DISTANCE_TEXT_COLOR = "darkblue"
WEIGHT_TEXT_COLOR = "darkred"


def edge_key(source: str, target: str) -> tuple[str, str]:
    """Cheie neorientată pentru muchii."""
    return (source, target) if source <= target else (target, source)


def format_distance(value) -> str:
    """Convertește o distanță în text."""
    return "∞" if value == inf else str(value)


def compute_edge_endpoints(
    x1: float, y1: float, x2: float, y2: float
) -> tuple[float, float, float, float]:
    """Mută capetele muchiei pe conturul nodurilor."""
    dx, dy = x2 - x1, y2 - y1
    length = hypot(dx, dy)
    if length == 0:
        return x1, y1, x2, y2
    ux, uy = dx / length, dy / length
    return (
        x1 + ux * NODE_RADIUS,
        y1 + uy * NODE_RADIUS,
        x2 - ux * NODE_RADIUS,
        y2 - uy * NODE_RADIUS,
    )


def compute_weight_position(
    x1: float, y1: float, x2: float, y2: float
) -> tuple[float, float]:
    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2

    return (
        midpoint_x - WEIGHT_OFFSET_X,
        midpoint_y - WEIGHT_OFFSET_Y,
    )


def draw_node(
    canvas, x: float, y: float, label: str, distance: str, style
) -> None:
    """Desenează un nod, eticheta și distanța lui."""
    canvas.create_oval(
        x - NODE_RADIUS,
        y - NODE_RADIUS,
        x + NODE_RADIUS,
        y + NODE_RADIUS,
        fill=style.fill_color,
        outline=style.outline_color,
        width=style.outline_width,
    )
    canvas.create_text(
        x - DISTANCE_OFFSET_X,
        y - DISTANCE_OFFSET_Y,
        text=distance,
        font=DISTANCE_FONT,
        fill=DISTANCE_TEXT_COLOR,
    )
    canvas.create_text(x, y, text=label, font=NODE_FONT)


def draw_edge(
    canvas, x1: float, y1: float, x2: float, y2: float, weight: int, style
) -> None:
    """Desenează o muchie și ponderea ei."""
    sx, sy, ex, ey = compute_edge_endpoints(x1, y1, x2, y2)
    canvas.create_line(sx, sy, ex, ey, fill=style.color, width=style.width)
    weight_x, weight_y = compute_weight_position(sx, sy, ex, ey)
    canvas.create_text(
        weight_x,
        weight_y,
        text=str(weight),
        font=WEIGHT_FONT,
        fill=WEIGHT_TEXT_COLOR,
    )


def draw_graph(canvas, graph, positions, source_node, step) -> None:
    """Desenează starea curentă a algoritmului."""
    canvas.delete("all")
    drawn_edges = set()

    # Muchiile se desenează înaintea nodurilor.
    for source in graph.nodes():
        for target, weight in graph.neighbors(source).items():
            key = edge_key(source, target)
            if key not in drawn_edges:
                drawn_edges.add(key)
                x1, y1 = positions[source]
                x2, y2 = positions[target]
                draw_edge(
                    canvas,
                    x1,
                    y1,
                    x2,
                    y2,
                    weight,
                    get_edge_style(source, target, step),
                )

    distances = step.state_after.distances
    for node in sorted(graph.nodes()):
        x, y = positions[node]
        draw_node(
            canvas,
            x,
            y,
            node,
            format_distance(distances[node]),
            get_node_style(node, source_node, step),
        )