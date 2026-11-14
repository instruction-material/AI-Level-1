import importlib.util
from pathlib import Path
import sys
import unittest

root = Path(__file__).parent
sys.path.insert(0, str(root / "solution"))
spec = importlib.util.spec_from_file_location("optional_reference", root / "solution" / "main.py")
exercise = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exercise)


class OptionalContract(unittest.TestCase):
    def test_worked_case_and_repeatability(self):
        result = exercise.solve_extension()
        self.assertEqual(result, {'9': {'take': 1, 'winning_take_exists': True}, '10': {'take': 2, 'winning_take_exists': True}, '11': {'take': 3, 'winning_take_exists': True}, '12': {'take': 1, 'winning_take_exists': False}})
        self.assertEqual(exercise.solve_extension(), result)


if __name__ == "__main__":
    unittest.main()
