"""Bounded endgame oracles and independent game-tree root checks."""
import ast
import contextlib
from functools import lru_cache
import io
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent
TTT = ("FAI7-Unbeatable-Tic-Tac-Toe-AI", "FAI7-Unbeatable-Tic-Tac-Toe-AI-1",
       "FAI7-Updated-Tic-Tac-Toe-AI")
LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def scope_for(folder):
    path = ROOT / folder / "main.py"
    tree = ast.parse(path.read_text())
    tree.body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.ClassDef))]
    scope = {}
    exec(compile(tree, str(path), "exec"), scope)
    return scope


def terminal(board):
    for a, b, c in LINES:
        if board[a] != "-" and board[a] == board[b] == board[c]:
            return 10 if board[a] == "O" else -10
    return None if "-" in board else 0


@lru_cache(None)
def value(board, player):
    end = terminal(board)
    if end is not None:
        return end
    values = [value(board[:i] + player + board[i + 1:], "O" if player == "X" else "X")
              for i, cell in enumerate(board) if cell == "-"]
    return max(values) if player == "O" else min(values)


def reachable():
    result = set()
    def visit(board, player):
        if (board, player) in result:
            return
        result.add((board, player))
        if terminal(board) is not None:
            return
        for i, cell in enumerate(board):
            if cell == "-":
                visit(board[:i] + player + board[i + 1:], "O" if player == "X" else "X")
    visit("-" * 9, "X")
    return result


def node_for(scope, folder, board, player):
    empty = " " if "Updated" in folder else "-"
    rows = [list(board[i:i + 3].replace("-", empty)) for i in range(0, 9, 3)]
    return scope["TreeNode"](rows, player)


class LegacyGameRoots(unittest.TestCase):
    def test_updated_tree_scores_its_supplied_root_instead_of_a_global(self):
        folder = TTT[-1]
        scope = scope_for(folder)
        scope["root"] = node_for(scope, folder, "XXXOO----", "O")
        root = node_for(scope, folder, "XX--O----", "O")
        with contextlib.redirect_stdout(io.StringIO()):
            scope["Tree"](root)
        self.assertIsNotNone(root.best_child)
        self.assertEqual(root.best_child.board[0][2], "O")
        self.assertEqual(root.score, 0)

    def test_two_player_marble_tree_expands_its_supplied_root(self):
        scope = scope_for("FAI8-2-Player-Marble-Game")
        scope["root"] = scope["TreeNode"](1)
        root = scope["TreeNode"](3)
        scope["Tree"](root)
        self.assertEqual([child.num_marbles for child in root.children], [2, 1, 0])
        self.assertEqual(scope["root"].children, [])

    def test_three_minimax_variants_match_every_reachable_small_endgame(self):
        states = sorted((board, player) for board, player in reachable()
                        if board.count("-") <= 4 and terminal(board) is None)
        self.assertGreater(len(states), 1000)
        for folder in TTT:
            scope = scope_for(folder)
            # A terminal unrelated global catches accidental free-variable use.
            scope["root"] = node_for(scope, folder, "XXXOO----", "O")
            for board, player in states:
                root = node_for(scope, folder, board, player)
                with contextlib.redirect_stdout(io.StringIO()):
                    scope["Tree"](root)
                with self.subTest(folder=folder, board=board, player=player):
                    self.assertEqual(root.score, value(board, player))
                    child = root.best_child
                    self.assertIsNotNone(child)
                    chosen = "".join("".join(row) for row in child.board).replace(" ", "-")
                    edits = [i for i in range(9) if chosen[i] != board[i]]
                    self.assertEqual(len(edits), 1)
                    self.assertEqual(board[edits[0]], "-")
                    self.assertEqual(chosen[edits[0]], player)
                    self.assertEqual(value(chosen, "O" if player == "X" else "X"), root.score)

    def test_both_marble_ai_variants_match_last_take_wins_positions(self):
        for folder in ("FAI8-The-Marble-Game-AI", "FAI8-The-Marble-Game-AI-Copy"):
            scope = scope_for(folder)
            for count in range(11):
                for ai_turn in (False, True):
                    root = scope["TreeNode"](count, ai_turn)
                    scope["Tree"](root)
                    # Scores are from the human's perspective.
                    ai_wins = (count % 4 != 0) if ai_turn else (count % 4 == 0)
                    expected = -10 if ai_wins else 10
                    with self.subTest(folder=folder, count=count, ai_turn=ai_turn):
                        self.assertEqual(root.score, expected)
                        if count:
                            self.assertIn(count - root.best_child.num_marbles, [1, 2, 3])
                            self.assertEqual(root.best_child.score, expected)


if __name__ == "__main__":
    unittest.main()
