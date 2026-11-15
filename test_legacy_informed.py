"""Behavioral comparisons and a shortest-path oracle for the legacy APIs."""
import ast
import contextlib
import io
import itertools
import math
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent
FOLDERS = ("FAI10-Implement-A-Search", "FAI10-Implement-Greedy-Search")


def classes(folder):
    path = ROOT / folder / "main.py"
    module = ast.parse(path.read_text())
    module.body = [n for n in module.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.ClassDef))]
    scope = {}
    exec(compile(module, str(path), "exec"), scope)
    return scope["Node"], scope["Graph"]


def graph_for(folder, keys, edges, heuristics=None):
    Node, Graph = classes(folder)
    nodes = {key: Node(key, (heuristics or {}).get(key, 0)) for key in keys}
    graph = Graph()
    for node in nodes.values():
        graph.add_node(node)
    for left, right, weight in edges:
        graph.add_edge(nodes[left], nodes[right], weight)
    return graph, nodes


def search(folder, graph, start, goal=None):
    method = "a_star_search" if folder == FOLDERS[0] else "greedy_search"
    with contextlib.redirect_stdout(io.StringIO()):
        return getattr(graph, method)(start, goal)


def distances(keys, edges):
    result = {(a, b): (0 if a == b else math.inf) for a in keys for b in keys}
    for a, b, weight in edges:
        result[a, b] = result[b, a] = min(result[a, b], weight)
    for middle in keys:
        for a in keys:
            for b in keys:
                result[a, b] = min(result[a, b], result[a, middle] + result[middle, b])
    return result


class LegacyInformedSearch(unittest.TestCase):
    def assert_path_cost(self, result, edges, expected):
        if math.isinf(expected):
            self.assertEqual(result["path"], [])
            self.assertIsNone(result["cost"])
            return
        costs = {(a, b): w for a, b, w in edges}
        costs.update({(b, a): w for a, b, w in edges})
        measured = sum(costs[a, b] for a, b in zip(result["path"], result["path"][1:]))
        self.assertEqual(measured, expected)
        self.assertEqual(result["cost"], expected)

    def test_depth_based_priority_original_counterexample(self):
        edges = [("S", "A", 1), ("A", "B", 1), ("B", "D", 1),
                 ("D", "C", 3), ("S", "C", 5), ("C", "G", 1)]
        graph, nodes = graph_for(FOLDERS[0], ["S", "A", "B", "C", "D", "G"], edges)
        result = search(FOLDERS[0], graph, nodes["S"], nodes["G"])
        self.assertEqual(result["path"], ["S", "C", "G"])
        self.assert_path_cost(result, edges, 6)

    def test_same_graph_distinguishes_greedy_h_from_astar_g_plus_h(self):
        edges = [("S", "A", 1), ("A", "G", 20), ("S", "B", 5), ("B", "G", 1)]
        heuristics = {"S": 0, "A": 0, "B": 1, "G": 0}
        results = []
        for folder in FOLDERS:
            graph, nodes = graph_for(folder, ["S", "A", "B", "G"], edges, heuristics)
            results.append(search(folder, graph, nodes["S"], nodes["G"]))
        self.assertEqual(results[0]["order"], ["S", "A", "B", "G"])
        self.assertEqual(results[1]["order"], ["S", "A", "G"])
        self.assert_path_cost(results[0], edges, 6)
        self.assert_path_cost(results[1], edges, 21)

    def test_all_three_vertex_nonnegative_graphs_against_floyd_warshall(self):
        keys = ["a", "b", "c"]
        pairs = list(itertools.combinations(keys, 2))
        cases = 0
        for weights in itertools.product([None, 0, 1, 3], repeat=3):
            edges = [(a, b, w) for (a, b), w in zip(pairs, weights) if w is not None]
            oracle = distances(keys, edges)
            for start, goal in itertools.product(keys, repeat=2):
                for exact_estimate in (False, True):
                    heuristics = {key: (oracle[key, goal] if exact_estimate and
                                        math.isfinite(oracle[key, goal]) else 0) for key in keys}
                    graph, nodes = graph_for(FOLDERS[0], keys, edges, heuristics)
                    result = search(FOLDERS[0], graph, nodes[start], nodes[goal])
                    with self.subTest(weights=weights, start=start, goal=goal, exact=exact_estimate):
                        self.assert_path_cost(result, edges, oracle[start, goal])
                        if result["path"]:
                            self.assertEqual(result["path"][0], start)
                            self.assertEqual(result["path"][-1], goal)
                    cases += 1
        self.assertEqual(cases, 1152)

    def test_admissible_inconsistent_estimate_reopens_expanded_state(self):
        edges = [("S", "A", 2), ("S", "B", 1), ("B", "A", 0.5),
                 ("A", "G", 2), ("B", "G", 100)]
        graph, nodes = graph_for(FOLDERS[0], ["S", "A", "B", "G"], edges,
                                 {"S": 0, "A": 0, "B": 2.5, "G": 0})
        result = search(FOLDERS[0], graph, nodes["S"], nodes["G"])
        self.assertEqual(result["order"], ["S", "A", "B", "A", "G"])
        self.assertEqual(result["path"], ["S", "B", "A", "G"])
        self.assert_path_cost(result, edges, 3.5)

    def test_stale_queued_routes_are_skipped(self):
        edges = [("S", "A", 5), ("S", "B", 1), ("B", "A", 1),
                 ("A", "G", 10), ("B", "G", 50)]
        graph, nodes = graph_for(FOLDERS[0], ["S", "A", "B", "G"], edges)
        result = search(FOLDERS[0], graph, nodes["S"], nodes["G"])
        self.assertEqual(result["order"], ["S", "B", "A", "G"])
        self.assert_path_cost(result, edges, 12)

    def test_zero_cycles_unreachable_goal_and_start_equal_goal(self):
        edges = [("S", "A", 0), ("A", "B", 0), ("B", "S", 0)]
        for folder in FOLDERS:
            graph, nodes = graph_for(folder, ["S", "A", "B", "G"], edges)
            self.assert_path_cost(search(folder, graph, nodes["S"], nodes["G"]), edges, math.inf)
            result = search(folder, graph, nodes["S"], nodes["S"])
            self.assertEqual(result["order"], ["S"])
            self.assertEqual(result["path"], ["S"])
            self.assert_path_cost(result, edges, 0)

    def test_original_one_argument_calls_still_traverse_reachable_states(self):
        for folder in FOLDERS:
            Node, Graph = classes(folder)
            graph = Graph()
            a, b, c = Node("a"), Node("b"), Node("c")
            for node in [a, b, c]:
                graph.add_node(node)
            graph.add_edge(a, b, 1)
            result = search(folder, graph, a)
            self.assertEqual(result["order"], ["a", "b"])
            self.assertIsNone(result["cost"])

    def test_finite_nonnegative_cost_and_estimate_contract(self):
        for folder in FOLDERS:
            Node, Graph = classes(folder)
            for invalid in [-1, math.inf, math.nan, "1"]:
                with self.assertRaises(ValueError):
                    Node("bad", invalid)
                graph = Graph()
                a, b = Node("a"), Node("b")
                graph.add_node(a)
                graph.add_node(b)
                with self.assertRaises(ValueError):
                    graph.add_edge(a, b, invalid)

    def test_registered_nodes_and_zero_goal_estimate(self):
        for folder in FOLDERS:
            Node, Graph = classes(folder)
            with self.assertRaises(ValueError):
                search(folder, Graph(), Node("unknown"))
        graph, nodes = graph_for(FOLDERS[0], ["S", "G"], [("S", "G", 1)], {"G": 1})
        with self.assertRaises(ValueError):
            search(FOLDERS[0], graph, nodes["S"], nodes["G"])

    def test_complete_demonstrations_match_their_documented_outputs(self):
        for folder, order, path, cost in [
            (FOLDERS[0], "S A B G", "S -> B -> G", 6),
            (FOLDERS[1], "S A G", "S -> A -> G", 21),
        ]:
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                runpy.run_path(str(ROOT / folder / "main.py"))
            self.assertEqual(stream.getvalue().splitlines(),
                             [order + " ", "Path: " + path, "Cost: " + str(cost)])


if __name__ == "__main__":
    unittest.main()
