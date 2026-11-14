import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("unit_reference", Path(__file__).parent / "solution" / "main.py")
exercise = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exercise)


class UnitContract(unittest.TestCase):
    def test_worked_case(self):
        self.assertEqual(exercise.solve_extension(), {'overall': 0.5, 'groups': {'A': 0.25, 'B': 0.75}, 'positive_recall': 0.5})

    def test_boundaries(self):
        rows = [("A", 0, 0)] * 9 + [("A", 1, 0)]
        self.assertEqual(exercise.metrics(rows)["overall"], 0.9)
        self.assertEqual(exercise.metrics(rows)["positive_recall"], 0)
        self.assertIsNone(exercise.metrics([])["overall"])
        weighted = [("A", 0, 0)] * 3 + [("B", 1, 0)]
        self.assertEqual(exercise.metrics(weighted)["overall"], 0.75)


if __name__ == "__main__":
    unittest.main()
