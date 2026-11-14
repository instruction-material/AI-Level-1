import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("unit_reference", Path(__file__).parent / "solution" / "main.py")
exercise = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exercise)


class UnitContract(unittest.TestCase):
    def test_worked_case(self):
        self.assertEqual(exercise.solve_extension(), {'stack': ['S', 'B', 'D', 'A', 'C', 'G'], 'queue': ['S', 'A', 'B', 'C', 'D', 'G']})

    def test_boundaries(self):
        self.assertEqual(len(set(exercise.traversal("stack"))), 6)
        with self.assertRaises(ValueError):
            exercise.traversal("random")


if __name__ == "__main__":
    unittest.main()
