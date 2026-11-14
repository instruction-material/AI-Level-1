import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("unit_reference", Path(__file__).parent / "solution" / "main.py")
exercise = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exercise)


class UnitContract(unittest.TestCase):
    def test_worked_case(self):
        self.assertEqual(exercise.solve_extension(), {'from_start': [(0, 1)], 'from_goal': [(0, 1)]})

    def test_boundaries(self):
        self.assertEqual(exercise.legal_next((0, 1)), [(0, 0), (1, 1)])
        for position in ((-1, 0), (1, 0), (2, 0)):
            with self.assertRaises(ValueError):
                exercise.legal_next(position)


if __name__ == "__main__":
    unittest.main()
