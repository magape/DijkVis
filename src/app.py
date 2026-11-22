"""
app.py

GUI-ul principal al aplicației DijkVis.
"""

import tkinter as tk
from tkinter import messagebox

from dijkstra import DijkstraSimulator
from layout import compute_layout
from parser import parse_graph
from renderer import draw_graph
from style import (
    ACTIVE_EDGE_STYLE,
    CURRENT_NODE_STYLE,
    NORMAL_EDGE_STYLE,
    PREDECESSOR_EDGE_STYLE,
    SOURCE_NODE_STYLE,
    UNREACHABLE_NODE_STYLE,
    UNVISITED_NODE_STYLE,
    VISITED_NODE_STYLE,
)
from transform import transform_layout

WINDOW_TITLE = "DijkVis"
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
DEFAULT_GRAPH = "AB5, AC2, BC1, BD4, CE7, DE3"
DEFAULT_SOURCE = "A"

LEGEND_ITEMS = (
    ("● Nod sursă", SOURCE_NODE_STYLE.fill_color),
    ("● Nod curent", CURRENT_NODE_STYLE.fill_color),
    ("● Nod vizitat", VISITED_NODE_STYLE.fill_color),
    ("● Nod nevizitat", UNVISITED_NODE_STYLE.fill_color),
    ("● Nod izolat", UNREACHABLE_NODE_STYLE.fill_color),
    ("● Muchie normală", NORMAL_EDGE_STYLE.color),
    ("● Muchie activă", ACTIVE_EDGE_STYLE.color),
    ("● Muchie predecesor", PREDECESSOR_EDGE_STYLE.color),
)


class DijkVisApp:
    """Interfața grafică și controlul pașilor pentru DijkVis."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)

        self.graph = None
        self.source_node = None
        self.result = None
        self.positions = None
        self.current_step_index = 0

        self._build_ui()
        self.load_graph()

    def _build_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, pady=10)

        input_frame = tk.Frame(self.main_frame)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Graf:").pack(side="left")
        self.graph_entry = tk.Entry(input_frame, width=80)
        self.graph_entry.pack(side="left", padx=5)
        self.graph_entry.insert(0, DEFAULT_GRAPH)

        tk.Label(input_frame, text="Sursă:").pack(side="left", padx=(15, 0))
        self.source_entry = tk.Entry(input_frame, width=4)
        self.source_entry.pack(side="left", padx=5)
        self.source_entry.insert(0, DEFAULT_SOURCE)

        self.draw_button = tk.Button(
            input_frame, text="Desenează", command=self.load_graph
        )
        self.draw_button.pack(side="left", padx=(15, 0))

        nav_frame = tk.Frame(self.main_frame)
        nav_frame.pack(pady=5)

        self.previous_button = tk.Button(
            nav_frame, text="◀ Anterior", command=self.show_previous_step
        )
        self.previous_button.pack(side="left")

        self.step_label = tk.Label(nav_frame, text="Pas 0 / 0")
        self.step_label.pack(side="left", padx=20)

        self.next_button = tk.Button(
            nav_frame, text="Următor ▶", command=self.show_next_step
        )
        self.next_button.pack(side="left")

        content_frame = tk.Frame(self.main_frame)
        content_frame.pack(pady=10)

        self.canvas = tk.Canvas(
            content_frame,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg="white",
        )
        self.canvas.pack(side="left")

        side_panel = tk.Frame(content_frame)
        side_panel.pack(side="left", padx=(20, 0), fill="y")

        self.message_label = tk.Label(
            side_panel,
            justify="left",
            anchor="nw",
            font=("Consolas", 12, "bold"),
        )
        self.message_label.pack(anchor="nw", fill="x")

        tk.Frame(side_panel, height=5).pack(fill="x", pady=10)
        tk.Label(
            side_panel, text="Legendă", font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        lg_font = ("Segoe UI", 10, "bold")
        for text, color in LEGEND_ITEMS:
            tk.Label(side_panel, text=text, fg=color, font=lg_font).pack(
                anchor="w"
            )

    def load_graph(self):
        try:
            graph_text = self.graph_entry.get().strip()
            if not graph_text:
                raise ValueError("Trebuie introdus un graf.")

            self.source_node = self.source_entry.get().strip().upper()
            self.graph = parse_graph(graph_text, undirected=True)
            self.result = DijkstraSimulator(self.graph).run(self.source_node)

            layout = compute_layout(self.graph)
            self.positions = transform_layout(
                layout,
                canvas_width=CANVAS_WIDTH,
                canvas_height=CANVAS_HEIGHT,
            )

            self.current_step_index = 0
            self.display_current_step()
        except Exception as exc:
            messagebox.showerror("Eroare", str(exc))

    def display_current_step(self):
        if not self.result.steps:
            return

        step = self.result.steps[self.current_step_index]
        draw_graph(
            canvas=self.canvas,
            graph=self.graph,
            positions=self.positions,
            source_node=self.source_node,
            step=step,
        )
        self.step_label.config(
            text=(
                f"Pas {self.current_step_index + 1} / "
                f"{len(self.result.steps)}"
            )
        )
        self.message_label.config(text=self._build_step_message(step))
        self.update_navigation_buttons()

    def _format_distance(self, value):
        return "∞" if value == float("inf") else str(value)

    def _build_step_message(self, step):
        dist_val = step.state_before.distances[step.current_node]
        dist_str = self._format_distance(dist_val)
        lines = [
            f"Pasul {step.step_number}",
            "",
            f"Nod curent: {step.current_node}, "
            f"d({step.current_node})={dist_str} (minim)",
            "",
        ]

        if not step.analyses:
            lines.append("Nu există vecini nevizitați.")
            return "\n".join(lines)

        for a in step.analyses:
            old = self._format_distance(a.old_neighbor_distance)
            cand = self._format_distance(a.candidate_distance)
            base = (
                f"{a.current_node}→{a.neighbor}: "
                f"{a.current_node_distance}+{a.edge_weight}={cand}"
            )
            if a.distance_updated:
                lines.append(f"{base} < {old} | {a.neighbor}: {old}→{cand}")
            else:
                lines.append(f"{base} >= {old} | {a.neighbor} rămâne {old}")

        return "\n".join(lines)

    def update_navigation_buttons(self):
        last_index = len(self.result.steps) - 1
        self.previous_button.config(
            state=tk.DISABLED if self.current_step_index == 0 else tk.NORMAL
        )
        self.next_button.config(
            state=(
                tk.DISABLED
                if self.current_step_index == last_index
                else tk.NORMAL
            )
        )

    def show_previous_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.display_current_step()

    def show_next_step(self):
        if self.current_step_index < len(self.result.steps) - 1:
            self.current_step_index += 1
            self.display_current_step()

    def run(self):
        self.root.mainloop()