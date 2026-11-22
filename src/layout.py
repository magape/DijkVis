"""
layout.py

Poziționarea nodurilor pe o elipsă canonică.
"""

from math import cos, pi, sin

ELLIPSE_A = 4000.0
ELLIPSE_B = 2800.0


def compute_angles(node_count: int) -> list[float]:
    """Generează unghiurile asociate nodurilor în radiani."""
    step = 2 * pi / node_count
    return [
        -pi + (-1) ** (i + 1) * ((i + 1) // 2) * step
        for i in range(node_count)
    ]


def ellipse_point(angle: float) -> tuple[float, float]:
    """Transformă unghiul în coordonate pe elipsă."""
    return ELLIPSE_A * cos(angle), ELLIPSE_B * sin(angle)


def compute_layout(graph) -> dict[str, tuple[float, float]]:
    """Calculează pozițiile geometrice ale nodurilor."""
    nodes = sorted(graph.nodes())
    if len(nodes) == 1:
        return {nodes[0]: (0.0, 0.0)}

    angles = compute_angles(len(nodes))
    return {
        node: ellipse_point(angle)
        for node, angle in zip(nodes, angles)
    }