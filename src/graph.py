"""
graph.py

Clasa Graph reprezinta un graf orientat ponderat.

Responsabilitati:
- gestionarea nodurilor;
- gestionarea muchiilor;
- gestionarea ponderilor.

Nu gestioneaza:
- algoritmul Dijkstra;
- coordonatele nodurilor;
- reprezentarea grafica;
- interfata utilizator.
"""


class Graph:
    """
    Reprezentare prin lista de adiacenta.

    Exemplu valid:

    {
        "A": {
            "B": 3,
            "C": 4
        },
        "B": {
            "D": 2
        },
        "C": {},
        "D": {}
    }

    INVARIANT 1

    Pentru orice nod care apare intr-o muchie,
    exista o cheie corespunzatoare in _adjacency.

    Exemplu valid:

    {
        "A": {"B": 3},
        "B": {}
    }

    Exemplu invalid:

    {
        "A": {"B": 3}
    }

    INVARIANT 2

    Toate numele nodurilor sunt memorate
    folosind majuscule.
    """

    def __init__(self):
        # Structura interna a grafului: fiecare nod exista ca cheie.
        self._adjacency = {}

    def add_node(self, node):
        node = self._normalize_node(node)
        if node not in self._adjacency:
            self._adjacency[node] = {}

    def remove_node(self, node):
        node = self._normalize_node(node)
        if node not in self._adjacency:
            return

        # Eliminam muchiile care ajung in nod.
        for neighbors in self._adjacency.values():
            neighbors.pop(node, None)

        # Eliminam nodul si muchiile care pleaca din el.
        del self._adjacency[node]

    def add_edge(self, source, target, weight):
        source = self._normalize_node(source)
        target = self._normalize_node(target)
        self._validate_weight(weight)

        self.add_node(source)
        self.add_node(target)
        self._adjacency[source][target] = weight

    def remove_edge(self, source, target):
        source = self._normalize_node(source)
        target = self._normalize_node(target)
        if source in self._adjacency:
            self._adjacency[source].pop(target, None)

    def has_node(self, node):
        node = self._normalize_node(node)
        return node in self._adjacency

    def has_edge(self, source, target):
        source = self._normalize_node(source)
        target = self._normalize_node(target)
        return source in self._adjacency and target in self._adjacency[source]

    def neighbors(self, node):
        node = self._normalize_node(node)
        if node not in self._adjacency:
            raise ValueError(f"Nod inexistent: {node}")
        return dict(self._adjacency[node])

    def weight(self, source, target):
        source = self._normalize_node(source)
        target = self._normalize_node(target)
        if not self.has_edge(source, target):
            raise ValueError(f"Muchia {source}->{target} nu exista.")
        return self._adjacency[source][target]

    def nodes(self):
        return sorted(self._adjacency.keys())

    def edges(self):
        result = []
        for source in sorted(self._adjacency):
            for target, weight in sorted(self._adjacency[source].items()):
                result.append((source, target, weight))
        return result

    def node_count(self):
        return len(self._adjacency)

    def edge_count(self):
        return sum(len(neighbors) for neighbors in self._adjacency.values())

    def clear(self):
        self._adjacency.clear()

    def _normalize_node(self, node):
        if not isinstance(node, str):
            raise TypeError("Numele nodului trebuie sa fie text.")

        node = node.strip().upper()
        if not node:
            raise ValueError("Numele nodului nu poate fi gol.")

        return node

    def _validate_weight(self, weight):
        if not isinstance(weight, int):
            raise TypeError("Ponderea trebuie sa fie numar intreg.")

        if weight < 0:
            raise ValueError("Ponderile negative nu sunt permise.")

    def __str__(self):
        lines = []
        for node in self.nodes():
            neighbors = self._adjacency[node]
            if neighbors:
                text = ", ".join(
                    f"{neighbor}({weight})"
                    for neighbor, weight in sorted(neighbors.items())
                )
            else:
                text = "-"
            lines.append(f"{node} -> {text}")
        return "\n".join(lines)

    def __repr__(self):
        return f"Graph(nodes={self.node_count()}, edges={self.edge_count()})"