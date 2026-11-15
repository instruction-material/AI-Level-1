"""Bounded directed-path oracles for the original Maze graph API."""
import ast
from collections import deque
import contextlib
import io
import itertools
from pathlib import Path
import runpy
import sys
import unittest

ROOT = Path(__file__).resolve().parent


def classes():
    path = ROOT / "FAI9-Maze-Solver/main.py"
    tree = ast.parse(path.read_text())
    tree.body = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    scope = {"queue": __import__("queue")}
    exec(compile(tree, str(path), "exec"), scope)
    return scope["Node"], scope["Graph"]


def graph_for(keys, edges):
    Node, Graph = classes()
    graph = Graph()
    nodes = {key: Node(key) for key in keys}
    for node in nodes.values():
        graph.add_node(node)
    for a, b in edges:
        graph.add_edge(nodes[a], nodes[b], 1)
    return graph, nodes


def minimum_moves(keys, edges, start, goal):
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        key, depth = queue.popleft()
        if key == goal:
            return depth
        for a, b in edges:
            if a == key and b not in seen:
                seen.add(b)
                queue.append((b, depth + 1))
    return float("inf")


class LegacyMazeDepth(unittest.TestCase):
    def test_later_shallower_arrival_finds_the_three_move_route(self):
        edges = [("S", "A"), ("S", "B"), ("B", "C"), ("C", "X"),
                 ("A", "X"), ("X", "G")]
        graph, nodes = graph_for(["S", "A", "B", "C", "X", "G"], edges)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(graph.get_dls_path(nodes["S"], nodes["G"], 3), ["S", "A", "X", "G"])
            self.assertEqual(graph.get_ids_path(nodes["S"], nodes["G"], 3), ["S", "A", "X", "G"])

    def test_all_directed_three_vertex_graphs_at_every_start_goal_and_limit(self):
        keys = ["a", "b", "c"]
        possible = list(itertools.permutations(keys, 2))
        cases = 0
        for mask in range(64):
            edges = [edge for i, edge in enumerate(possible) if mask & (1 << i)]
            graph, nodes = graph_for(keys, edges)
            for start, goal in itertools.product(keys, repeat=2):
                distance = minimum_moves(keys, edges, start, goal)
                for limit in range(4):
                    with contextlib.redirect_stdout(io.StringIO()):
                        path = graph.get_dls_path(nodes[start], nodes[goal], limit)
                        ids = graph.get_ids_path(nodes[start], nodes[goal], limit)
                    for method, result in [("dls", path), ("ids", ids)]:
                        with self.subTest(mask=mask, start=start, goal=goal, limit=limit, method=method):
                            if distance > limit:
                                self.assertIsNone(result)
                            else:
                                self.assertEqual(result[0], start)
                                self.assertEqual(result[-1], goal)
                                self.assertLessEqual(len(result) - 1, limit)
                                if method == "ids":
                                    self.assertEqual(len(result) - 1, distance)
                                for a, b in zip(result, result[1:]):
                                    self.assertIn((a, b), edges)
                    cases += 1
        self.assertEqual(cases, 2304)

    def test_negative_limit_and_zero_length_route(self):
        graph, nodes = graph_for(["a", "b"], [])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(graph.get_dls_path(nodes["a"], nodes["b"], -1), [])
            self.assertEqual(graph.get_dls_path(nodes["a"], nodes["a"], 0), ["a"])
            self.assertIsNone(graph.get_ids_path(nodes["a"], nodes["b"], 8))

    def test_original_maze_demonstration_runs_with_all_four_route_outputs(self):
        folder = ROOT / "FAI9-Maze-Solver"
        prior = sys.modules.pop("maze", None)
        sys.path.insert(0, str(folder))
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                runpy.run_path(str(folder / "main.py"))
        finally:
            sys.path.pop(0)
            sys.modules.pop("maze", None)
            if prior is not None:
                sys.modules["maze"] = prior
        self.assertEqual(output.getvalue().count("Path Cost:"), 4)
        self.assertEqual(output.getvalue().count("Traversing Path..."), 4)


if __name__ == "__main__":
    unittest.main()
