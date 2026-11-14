import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("studio_reference", Path(__file__).parent / "solution" / "main.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class WeightedContract(unittest.TestCase):
    def test_weighted_example_and_bad_heuristic(self):
        for mode in ("ucs", "astar"):
            result = lab.search(lab.GRAPH, "S", "G", lab.ADMISSIBLE, mode)
            self.assertEqual((result["path"], result["cost"]), (["S", "A", "G"], 4))
            self.assertEqual([r["node"] for r in result["trace"]], ["S", "B", "A", "G"])
        self.assertEqual(lab.search(lab.GRAPH, "S", "G", lab.BAD, "astar")["cost"], 9)

    def test_reopen_with_inconsistent_admissible_estimates(self):
        graph = {"S": [("A", 3), ("B", 1)], "B": [("A", 1)], "A": [("G", 2)], "G": []}
        result = lab.search(graph, "S", "G", {"S": 0, "A": 0, "B": 3, "G": 0}, "astar")
        self.assertEqual(result["cost"], 4)
        self.assertEqual([s["node"] for s in result["trace"]].count("A"), 2)

    def test_zero_cycle_unreachable_and_invalid_costs(self):
        graph = {"S": [("A", 0)], "A": [("S", 0)]}
        self.assertIsNone(lab.search(graph, "S", "G")["cost"])
        self.assertEqual(lab.search(graph, "S", "S")["cost"], 0)
        for cost in (-1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                lab.search({"S": [("G", cost)]}, "S", "G")


if __name__ == "__main__":
    unittest.main()
