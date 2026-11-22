"""
dijkstra.py

Implementarea algoritmului Dijkstra și
structurile asociate vizualizării pas cu pas.
"""

from dataclasses import dataclass
from math import inf


# --------------------------------------------------
# Structuri de date
# --------------------------------------------------


@dataclass
class DijkstraState:
    """Instantaneu al algoritmului într-un anumit moment."""

    distances: dict[str, float]
    predecessors: dict[str, str | None]
    visited: set[str]


@dataclass
class NeighborAnalysis:
    """Analiza unei operații de relaxare pentru un vecin nevizitat."""

    current_node: str
    neighbor: str
    edge_weight: int
    current_node_distance: float
    old_neighbor_distance: float
    candidate_distance: float
    shorter_path_found: bool
    distance_updated: bool
    old_predecessor: str | None
    new_predecessor: str | None


@dataclass
class Step:
    """Un pas complet al algoritmului, de la selecție la procesarea vecinilor."""

    step_number: int
    current_node: str
    state_before: DijkstraState
    analyses: list[NeighborAnalysis]
    state_after: DijkstraState


@dataclass
class DijkstraResult:
    """Rezultatul complet al execuției algoritmului."""

    source_node: str
    final_state: DijkstraState
    steps: list[Step]


# --------------------------------------------------
# Simulator
# --------------------------------------------------


class DijkstraSimulator:
    """Executorul algoritmului Dijkstra."""

    def __init__(self, graph):
        self._graph = graph

    def run(self, source_node: str) -> DijkstraResult:
        """Execută algoritmul Dijkstra și returnează istoricul pas cu pas."""
        source_node = source_node.strip().upper()
        if not self._graph.has_node(source_node):
            raise ValueError(f"Nodul sursă '{source_node}' nu există.")

        nodes = self._graph.nodes()

        # Inițializare
        distances = {node: inf for node in nodes}
        predecessors = {node: None for node in nodes}
        visited = set()
        distances[source_node] = 0

        steps = []
        step_number = 1

        # Bucla principală
        while True:
            current_node = self._select_next_node(distances, visited)
            if current_node is None:
                break

            state_before = DijkstraState(
                distances=distances.copy(),
                predecessors=predecessors.copy(),
                visited=visited.copy(),
            )

            analyses = []
            neighbors = self._graph.neighbors(current_node)

            # Determinism: vecinii sunt analizați în ordine alfabetică.
            for neighbor in sorted(neighbors):
                # Dijkstra canonic: nodurile vizitate au distanțe definitive.
                if neighbor in visited:
                    continue

                edge_weight = neighbors[neighbor]
                current_node_distance = distances[current_node]
                old_neighbor_distance = distances[neighbor]
                candidate_distance = current_node_distance + edge_weight
                shorter_path_found = candidate_distance < old_neighbor_distance
                old_predecessor = predecessors[neighbor]

                if shorter_path_found:
                    distances[neighbor] = candidate_distance
                    predecessors[neighbor] = current_node
                    distance_updated = True
                else:
                    distance_updated = False

                new_predecessor = predecessors[neighbor]

                analyses.append(
                    NeighborAnalysis(
                        current_node=current_node,
                        neighbor=neighbor,
                        edge_weight=edge_weight,
                        current_node_distance=current_node_distance,
                        old_neighbor_distance=old_neighbor_distance,
                        candidate_distance=candidate_distance,
                        shorter_path_found=shorter_path_found,
                        distance_updated=distance_updated,
                        old_predecessor=old_predecessor,
                        new_predecessor=new_predecessor,
                    )
                )

            # Distanța nodului curent devine definitivă.
            visited.add(current_node)

            state_after = DijkstraState(
                distances=distances.copy(),
                predecessors=predecessors.copy(),
                visited=visited.copy(),
            )

            steps.append(
                Step(
                    step_number=step_number,
                    current_node=current_node,
                    state_before=state_before,
                    analyses=analyses,
                    state_after=state_after,
                )
            )

            step_number += 1

        final_state = DijkstraState(
            distances=distances.copy(),
            predecessors=predecessors.copy(),
            visited=visited.copy(),
        )

        return DijkstraResult(
            source_node=source_node,
            final_state=final_state,
            steps=steps,
        )

    def _select_next_node(self, distances, visited):
        """Selectează nodul nevizitat cu distanța minimă (tie-break alfabetic)."""
        candidates = sorted(node for node in distances if node not in visited)
        if not candidates:
            return None

        best_node = min(candidates, key=lambda node: distances[node])

        # Dacă cea mai mică distanță este infinită, restul nodurilor sunt inaccesibile.
        if distances[best_node] == inf:
            return None

        return best_node

    @staticmethod
    def reconstruct_path(predecessors, source_node, target_node):
        """Reconstruiește drumul minim folosind dicționarul de predecesori."""
        source_node = source_node.upper()
        target_node = target_node.upper()

        path = []
        current = target_node

        while current is not None:
            path.append(current)
            if current == source_node:
                break
            current = predecessors[current]

        path.reverse()

        if not path or path[0] != source_node:
            return []

        return path