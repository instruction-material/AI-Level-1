"""Independent reachable-within-limit checks for the original graph APIs."""
import ast
import contextlib
import io
from itertools import combinations
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent
FOLDERS = ("FAI9-Implement-DLS", "FAI9-Implement-IDS")


def classes(folder):
    path = ROOT / folder / "main.py"
    module = ast.parse(path.read_text())
    module.body = [node for node in module.body if isinstance(node, ast.ClassDef)]
    scope = {}
    exec(compile(module, str(path), "exec"), scope)
    return scope["Node"], scope["Graph"]


def graph_for(folder, keys, edges):
    node_class, graph_class = classes(folder)
    nodes = {key: node_class(key) for key in keys}
    graph = graph_class()
    for node in nodes.values():
        graph.add_node(node)
    for left, right in edges:
        graph.add_edge(nodes[left], nodes[right])
    return graph, nodes


def oracle(keys, edges, start, limit):
    adjacency = {key: [] for key in keys}
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    depths = {start: 0}
    queue = [start]
    for key in queue:
        if depths[key] >= limit:
            continue
        for neighbor in adjacency[key]:
            if neighbor not in depths:
                depths[neighbor] = depths[key] + 1
                queue.append(neighbor)
    return set(depths)


def output(graph, node, limit, method="dls"):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        getattr(graph, method)(node, limit)
    return stream.getvalue()


class LegacyDepthSearch(unittest.TestCase):
    def test_shallower_later_route_reaches_goal(self):
        keys = ["S", "A", "B", "C", "X", "G"]
        edges = [("S", "A"), ("S", "B"), ("B", "C"),
                 ("C", "X"), ("A", "X"), ("X", "G")]
        for folder in FOLDERS:
            graph, nodes = graph_for(folder, keys, edges)
            self.assertEqual(output(graph, nodes["S"], 3).split(),
                             ["S", "B", "C", "X", "A", "G"])
            if folder.endswith("IDS"):
                lines = output(graph, nodes["S"], 3, "ids").splitlines()
                self.assertEqual(len(lines), 4)
                for limit, line in enumerate(lines):
                    self.assertEqual(set(line.split()), oracle(keys, edges, "S", limit))

    def test_every_undirected_four_vertex_graph_at_each_limit(self):
        keys = ["a", "b", "c", "d"]
        possible = list(combinations(keys, 2))
        for mask in range(1 << len(possible)):
            edges = [edge for index, edge in enumerate(possible) if mask & (1 << index)]
            for folder in FOLDERS:
                graph, nodes = graph_for(folder, keys, edges)
                for start in keys:
                    for limit in range(4):
                        with self.subTest(mask=mask, folder=folder, start=start, limit=limit):
                            reached = output(graph, nodes[start], limit).split()
                            self.assertEqual(set(reached), oracle(keys, edges, start, limit))
                            self.assertEqual(len(reached), len(set(reached)))

    def test_cycles_disconnection_zero_and_negative_limits(self):
        keys = ["a", "b", "c", "isolated"]
        edges = [("a", "b"), ("b", "c"), ("c", "a")]
        for folder in FOLDERS:
            graph, nodes = graph_for(folder, keys, edges)
            self.assertEqual(output(graph, nodes["a"], 0).split(), ["a"])
            self.assertEqual(output(graph, nodes["a"], -1), "")
            reached = output(graph, nodes["a"], 100).split()
            self.assertEqual(set(reached), {"a", "b", "c"})
            self.assertEqual(len(reached), 3)

    def test_published_dls_demonstration_keeps_its_documented_order(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            runpy.run_path(str(ROOT / "FAI9-Implement-DLS/main.py"))
        self.assertEqual(stream.getvalue().splitlines(), [
            "a ", "a c b ", "a c d b e ", "a c d e b ", "a c d e b ",
        ])


if __name__ == "__main__":
    unittest.main()
