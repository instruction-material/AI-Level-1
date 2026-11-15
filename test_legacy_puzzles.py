"""Independent small-puzzle state-space and water-action oracles."""
import ast
from collections import deque
import contextlib
import io
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent
PUZZLES = ("FAI-Puzzle", "FAI11-8-Puzzle-Solver")
GOAL = "12345678 "


def scope_for(folder):
    path = ROOT / folder / "main.py"
    tree = ast.parse(path.read_text())
    tree.body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.ClassDef))]
    scope = {}
    exec(compile(tree, str(path), "exec"), scope)
    return scope


def boards_after(board):
    blank = board.index(" ")
    row, column = divmod(blank, 3)
    result = set()
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r, c = row + dr, column + dc
        if 0 <= r < 3 and 0 <= c < 3:
            target = r * 3 + c
            copy = list(board)
            copy[blank], copy[target] = copy[target], copy[blank]
            result.add("".join(copy))
    return result


def nearby():
    depths = {GOAL: 0}
    queue = deque([GOAL])
    while queue:
        board = queue.popleft()
        if depths[board] == 8:
            continue
        for child in boards_after(board):
            if child not in depths:
                depths[child] = depths[board] + 1
                queue.append(child)
    return depths


def node_for(scope, board):
    return scope["Node"]([list(board[i:i + 3]) for i in range(0, 9, 3)])


def jug_actions(state):
    a, b = state
    move_to_five = min(a, 5 - b)
    move_to_three = min(b, 3 - a)
    return {(a - move_to_five, b + move_to_five),
            (a + move_to_three, b - move_to_three), (a, 5), (3, b), (a, 0), (0, b)}


def jug_distance(start):
    seen = {start}
    queue = deque([(start, 0)])
    while queue:
        state, depth = queue.popleft()
        if state[1] == 4:
            return depth
        for child in jug_actions(state) - seen:
            seen.add(child)
            queue.append((child, depth + 1))


class LegacyPuzzleSearch(unittest.TestCase):
    def test_numbered_tile_estimate_is_admissible_and_consistent_near_goal(self):
        oracle = nearby()
        self.assertEqual(len(oracle), 268)
        for folder in PUZZLES:
            scope = scope_for(folder)
            method = "heuristic" if folder == PUZZLES[0] else "get_heuristic"
            for board, depth in oracle.items():
                node = node_for(scope, board)
                estimate = getattr(node, method)()
                self.assertLessEqual(estimate, depth)
                for child in boards_after(board):
                    self.assertLessEqual(estimate, 1 + getattr(node_for(scope, child), method)())
            self.assertEqual(getattr(node_for(scope, "1234567 8"), method)(), 1)

    def test_both_astar_variants_match_all_268_shortest_path_lengths(self):
        for folder in PUZZLES:
            scope = scope_for(folder)
            for board, depth in nearby().items():
                graph = scope["PuzzleGraph"](node_for(scope, board))
                result = graph.astarsearch() if folder == PUZZLES[0] else graph.a_star_solve()
                path = result if folder == PUZZLES[0] else result[0]
                flat = ["".join("".join(row) for row in node.board) for node in path]
                with self.subTest(folder=folder, board=board):
                    self.assertEqual(flat[0], board)
                    self.assertEqual(flat[-1], GOAL)
                    self.assertEqual(len(path) - 1, depth)
                    for a, b in zip(flat, flat[1:]):
                        self.assertIn(b, boards_after(a))

    def test_unsolvable_supplied_board_and_single_swapped_tiles_stop_before_expansion(self):
        for folder in PUZZLES:
            scope = scope_for(folder)
            for board in ["8651427 3", "21345678 "]:
                node = node_for(scope, board)
                self.assertFalse(node.is_solvable())
                # A solvability guard finishes without asking for any neighbors.
                node.generate_neighbors = lambda: self.fail("Unsolvable board expanded")
                graph = scope["PuzzleGraph"](node)
                if folder == PUZZLES[0]:
                    self.assertEqual(graph.astarsearch(), "didn't work")
                    self.assertIsNone(graph.bfs())
                else:
                    self.assertIsNone(graph.a_star_solve())
                    self.assertIsNone(graph.bfs_solve())

    def test_default_puzzle_demonstrations_run_and_count_moves(self):
        for folder in PUZZLES:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                runpy.run_path(str(ROOT / folder / "main.py"))
            self.assertEqual(output.getvalue().count("Moves: 2"), 2)

    def test_water_astar_is_optimal_from_all_24_integer_volume_states(self):
        scope = scope_for("FAI10-Water-Jug-Riddle")
        for a in range(4):
            for b in range(6):
                start = scope["Node"](a, b)
                best = jug_distance((a, b))
                self.assertLessEqual(start.get_admissible_heuristic(), best)
                path, count = scope["Graph"](start).a_star_solve()
                states = [node.state for node in path]
                self.assertEqual(states[0], (a, b))
                self.assertEqual(states[-1][1], 4)
                self.assertEqual(len(path) - 1, best)
                self.assertGreater(count, 0)
                for current, child in zip(states, states[1:]):
                    self.assertIn(child, jug_actions(current))
        self.assertEqual(jug_distance((0, 0)), 6)

    def test_water_greedy_legal_paths_and_documented_nonadmissible_hint(self):
        scope = scope_for("FAI10-Water-Jug-Riddle")
        self.assertEqual(scope["Node"](2, 5).get_heuristic(), 3)
        self.assertEqual(jug_distance((2, 5)), 1)
        for a in range(4):
            for b in range(6):
                path, count = scope["Graph"](scope["Node"](a, b)).greedy_solve()
                states = [node.state for node in path]
                self.assertEqual(states[0], (a, b))
                self.assertEqual(states[-1][1], 4)
                for current, child in zip(states, states[1:]):
                    self.assertIn(child, jug_actions(current))


if __name__ == "__main__":
    unittest.main()
