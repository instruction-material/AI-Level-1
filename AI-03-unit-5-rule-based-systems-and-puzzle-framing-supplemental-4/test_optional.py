import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("unit_reference", Path(__file__).parent / "solution" / "main.py")
exercise = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exercise)


class UnitContract(unittest.TestCase):
    def test_worked_case(self):
        self.assertEqual(exercise.solve_extension(), [{'route': 'connection', 'reason': 'offline rule takes priority'}, {'route': 'queue', 'reason': 'backlog is at least three'}, {'route': 'monitor', 'reason': 'online with backlog below three'}])

    def test_boundaries(self):
        self.assertEqual(exercise.route({"offline": False, "backlog": 2})["route"], "monitor")
        self.assertEqual(exercise.route({"offline": False, "backlog": 3})["route"], "queue")
        with self.assertRaises(ValueError):
            exercise.route({"offline": False, "backlog": -1})


if __name__ == "__main__":
    unittest.main()
