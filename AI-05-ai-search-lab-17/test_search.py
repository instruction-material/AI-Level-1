import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("studio_reference", Path(__file__).parent / "solution" / "main.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class PuzzleContract(unittest.TestCase):
    def test_all_boards_against_independent_distance_table(self):
        from itertools import permutations
        boards = list(permutations(range(4)))
        # Construct the state graph from the four physical board edges, then
        # use Floyd-Warshall to obtain distances without the search under test.
        infinity = 99
        distances = {(a, b): (0 if a == b else infinity) for a in boards for b in boards}
        edges = ((0, 1), (0, 2), (1, 3), (2, 3))
        for state in boards:
            for a, b in edges:
                if state[a] == 0 or state[b] == 0:
                    other = list(state)
                    other[a], other[b] = other[b], other[a]
                    distances[state, tuple(other)] = 1
        for via in boards:
            for start in boards:
                for goal in boards:
                    distances[start, goal] = min(distances[start, goal], distances[start, via] + distances[via, goal])
        reachable = 0
        for state in boards:
            expected = distances[state, lab.GOAL]
            baseline = lab.solve(state)
            self.assertEqual(baseline["moves"], None if expected == infinity else expected)
            if expected != infinity:
                reachable += 1
            for score in (lab.misplaced, lab.blank_distance):
                result = lab.solve(state, "greedy", score)
                self.assertEqual(bool(result["path"]), expected != infinity)
                for a, b in zip(result["path"], result["path"][1:]):
                    self.assertEqual(distances[a, b], 1)
                self.assertLessEqual(len(result["decisions"]), 12)
        self.assertEqual(reachable, 12)

    def test_zero_score_is_not_a_goal_test(self):
        state = (2, 3, 1, 0)
        self.assertEqual(lab.blank_distance(state), 0)
        self.assertEqual(lab.solve(state)["moves"], 4)
        self.assertEqual(lab.solve(state, "greedy", lab.blank_distance)["moves"], 4)
        with self.assertRaises(ValueError):
            lab.solve((1, 1, 3, 0))


if __name__ == "__main__":
    unittest.main()
