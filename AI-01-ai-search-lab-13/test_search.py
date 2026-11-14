import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("studio_reference", Path(__file__).parent / "solution" / "main.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class SearchContract(unittest.TestCase):
    def test_trace_and_parent_snapshots(self):
        result = lab.breadth_first_search(lab.GRAPH, "A", "F")
        self.assertEqual(result["path"], ["A", "C", "F"])
        self.assertEqual(result["expanded"], list("ABCDEF"))
        self.assertEqual(result["trace"][0]["frontier"], ["B", "C"])
        self.assertEqual(result["trace"][0]["parents"], {"A": None, "B": "A", "C": "A"})
        self.assertEqual(result["trace"][-1]["parents"]["F"], "C")

    def test_cycles_unreachable_and_start_goal(self):
        graph = {"S": ["A", "S"], "A": ["S"]}
        self.assertEqual(lab.breadth_first_search(graph, "S", "G")["expanded"], ["S", "A"])
        self.assertEqual(lab.breadth_first_search(graph, "S", "G")["path"], [])
        self.assertEqual(lab.breadth_first_search(graph, "S", "S")["path"], ["S"])


if __name__ == "__main__":
    unittest.main()
