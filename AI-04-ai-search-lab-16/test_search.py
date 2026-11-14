import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("studio_reference", Path(__file__).parent / "solution" / "main.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class ComparisonContract(unittest.TestCase):
    def test_same_inputs_different_priorities(self):
        greedy = lab.search(lab.GRAPH, "S", "G", lab.ADMISSIBLE, "greedy")
        astar = lab.search(lab.GRAPH, "S", "G", lab.ADMISSIBLE, "astar")
        self.assertEqual((greedy["path"], greedy["cost"]), (["S", "B", "G"], 9))
        self.assertEqual((astar["path"], astar["cost"]), (["S", "A", "G"], 4))
        self.assertEqual(greedy["trace"][-1]["priority"], 0)
        self.assertEqual(astar["trace"][-1]["priority"], 4)

    def test_equal_scores_cycles_and_unreachable_goal(self):
        self.assertEqual(lab.search(lab.GRAPH, "S", "G", {}, "astar")["cost"], 4)
        graph = {"S": [("A", 0)], "A": [("S", 0)]}
        self.assertEqual(lab.search(graph, "S", "G", {}, "greedy")["path"], [])
        self.assertEqual(lab.search(graph, "S", "S", {}, "greedy")["cost"], 0)


if __name__ == "__main__":
    unittest.main()
