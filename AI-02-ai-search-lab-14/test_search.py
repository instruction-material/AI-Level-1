import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("studio_reference", Path(__file__).parent / "solution" / "main.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class DepthContract(unittest.TestCase):
    def test_limit_boundary_and_repeated_work(self):
        results = [lab.depth_limited_search(lab.GRAPH, "S", "G", n) for n in range(5)]
        self.assertEqual([r["status"] for r in results], ["cutoff"] * 3 + ["found"] * 2)
        result = lab.iterative_deepening(lab.GRAPH, "S", "G", 9)
        self.assertEqual([a["limit"] for a in result["attempts"]], [0, 1, 2, 3])
        self.assertEqual(result["path"], ["S", "A", "C", "G"])
        self.assertEqual(sum(v["node"] == "S" for a in result["attempts"] for v in a["visits"]), 4)

    def test_shallower_second_path_and_cycles(self):
        graph = {"S": ["A", "B"], "A": ["X"], "X": ["C"], "B": ["C"], "C": ["G"]}
        self.assertEqual(lab.depth_limited_search(graph, "S", "G", 3)["path"], ["S", "B", "C", "G"])
        cycle = {"S": ["A"], "A": ["S"]}
        result = lab.iterative_deepening(cycle, "S", "G", 50)
        self.assertEqual(result["status"], "failure")
        self.assertEqual(len(result["attempts"]), 2)
        self.assertEqual(lab.depth_limited_search(cycle, "S", "S", 0)["path"], ["S"])
        for limit in (-1, 0.5, True):
            with self.assertRaises(ValueError):
                lab.depth_limited_search(cycle, "S", "G", limit)


if __name__ == "__main__":
    unittest.main()
