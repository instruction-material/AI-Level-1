"""Directed adventure choices keep invalid input at the current state."""
import ast
import contextlib
import io
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent


class AdventureChoices(unittest.TestCase):
    def graph(self):
        path = ROOT / "FAI2-Adventure-Game/main.py"
        tree = ast.parse(path.read_text())
        tree.body = [n for n in tree.body if isinstance(n, ast.ClassDef)]
        scope = {}
        exec(compile(tree, str(path), "exec"), scope)
        Node, Graph = scope["Node"], scope["AdventureGraph"]
        graph = Graph()
        nodes = {key: Node(key, key + "?") for key in ["start", "explore", "leave", "hidden"]}
        for node in nodes.values():
            graph.add_node(node)
        graph.add_edge(nodes["start"], nodes["explore"])
        graph.add_edge(nodes["start"], nodes["leave"])
        graph.add_edge(nodes["explore"], nodes["hidden"])
        return graph, nodes

    def test_unknown_choice_reprompts_without_changing_state(self):
        graph, nodes = self.graph()
        output = io.StringIO()
        with patch("builtins.input", side_effect=["typo", "leave"]) as prompt:
            with contextlib.redirect_stdout(output):
                graph.start_adventure(nodes["start"])
        self.assertEqual([call.args[0] for call in prompt.call_args_list], ["start?", "start?"])
        self.assertIn("Choose: explore, leave", output.getvalue())
        self.assertEqual(output.getvalue().splitlines()[-1], "leave?")

    def test_known_non_neighbor_cannot_skip_the_directed_route(self):
        graph, nodes = self.graph()
        output = io.StringIO()
        with patch("builtins.input", side_effect=["hidden", " ExPloRe ", "HIDDEN"]) as prompt:
            with contextlib.redirect_stdout(output):
                graph.start_adventure(nodes["start"])
        self.assertEqual([call.args[0] for call in prompt.call_args_list],
                         ["start?", "start?", "explore?"])
        self.assertEqual(output.getvalue().splitlines()[-1], "hidden?")

    def test_all_three_original_adventure_routes_finish(self):
        for answers, ending in [(["leave"], "leave the park and go home"),
                                (["explore", "run away"], "go home"),
                                (["explore", "check it out"], "cat")]:
            output = io.StringIO()
            with patch("builtins.input", side_effect=answers):
                with contextlib.redirect_stdout(output):
                    runpy.run_path(str(ROOT / "FAI2-Adventure-Game/main.py"))
            self.assertIn(ending, output.getvalue())


class AirportChoices(unittest.TestCase):
    def classes(self):
        path = ROOT / "FAI3-Airports-Problem/main.py"
        tree = ast.parse(path.read_text())
        tree.body = [n for n in tree.body if isinstance(n, ast.ClassDef)]
        scope = {}
        exec(compile(tree, str(path), "exec"), scope)
        return scope["Node"], scope["StateSpaceGraph"]

    def test_unknown_and_known_non_neighbor_keep_location_and_cost(self):
        Node, Graph = self.classes()
        graph = Graph()
        nodes = {key: Node(key, key) for key in ["S", "A", "G"]}
        for node in nodes.values():
            graph.add_node(node)
        graph.add_edge(nodes["S"], nodes["A"], 2)
        graph.add_edge(nodes["A"], nodes["G"], 3)
        output = io.StringIO()
        with patch("builtins.input", side_effect=["missing", "g", " A ", "G"]) as prompt:
            with contextlib.redirect_stdout(output):
                graph.manual_search(nodes["S"], nodes["G"])
        self.assertEqual(prompt.call_count, 4)
        self.assertIn("It took you 5 hours", output.getvalue())

    def test_both_original_boston_to_los_angeles_routes(self):
        for answers, cost in [(["ny", "sf", "la"], 8), (["dc", "s", "sf", "la"], 13)]:
            output = io.StringIO()
            with patch("builtins.input", side_effect=answers):
                with contextlib.redirect_stdout(output):
                    runpy.run_path(str(ROOT / "FAI3-Airports-Problem/main.py"))
            self.assertIn("It took you " + str(cost) + " hours", output.getvalue())

    def test_dead_end_finishes_without_prompting_for_an_impossible_flight(self):
        Node, Graph = self.classes()
        graph = Graph()
        a, b = Node("a", "A"), Node("b", "B")
        graph.add_node(a)
        graph.add_node(b)
        output = io.StringIO()
        with patch("builtins.input", side_effect=[]) as prompt:
            with contextlib.redirect_stdout(output):
                graph.manual_search(a, b)
        prompt.assert_not_called()
        self.assertIn("No flights available from A", output.getvalue())


if __name__ == "__main__":
    unittest.main()
