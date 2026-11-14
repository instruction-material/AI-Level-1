import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("game_reference", Path(__file__).parent / "solution" / "main.py")
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)


class TicTacToeContract(unittest.TestCase):
    def test_win_block_fork_draw_and_invalid_moves(self):
        self.assertEqual(game.best_move(tuple("XX--O----")), 2)
        scores = game.candidate_scores(tuple("XX--O----"))
        self.assertEqual([c["move"] for c in scores if c["score"] == 0], [2])
        self.assertEqual(game.best_move(tuple("XX-OO-X--")), 5)
        self.assertEqual(game.best_move(tuple("X---O---X")), 1)
        self.assertEqual(game.minimax(game.EMPTY), 0)
        self.assertIsNone(game.best_move(tuple("XOXOOXXXO")))
        self.assertIsNone(game.best_move(tuple("XXXOO----")))
        for index in (-1, 9, True, 0.5):
            with self.assertRaises(ValueError):
                game.play(game.EMPTY, index)
        with self.assertRaises(ValueError):
            game.play(tuple("X--------"), 0)
        with self.assertRaises(ValueError):
            game.best_move(tuple("XX-------"))

    def test_ai_never_loses_against_any_human_x_play(self):
        seen = set()
        def all_human_choices(board):
            if board in seen:
                return
            seen.add(board)
            self.assertNotEqual(game.winner(board), "X")
            if game.winner(board) or "-" not in board:
                return
            if board.count("X") == board.count("O"):
                for i, cell in enumerate(board):
                    if cell == "-":
                        all_human_choices(board[:i] + ("X",) + board[i+1:])
            else:
                move = game.best_move(board)
                self.assertEqual(board[move], "-")
                all_human_choices(board[:move] + ("O",) + board[move+1:])
        all_human_choices(game.EMPTY)
        self.assertGreater(len(seen), 100)

    def test_seeded_baseline_and_independent_legacy_constructor(self):
        from random import Random
        self.assertEqual(game.baseline_move(game.EMPTY, Random(7)), 5)
        self.assertEqual(game.baseline_move(game.EMPTY, Random(7)), 5)
        import ast, contextlib, io
        root = Path(__file__).parent.parent
        for folder in ("FAI7-Unbeatable-Tic-Tac-Toe-AI", "FAI7-Unbeatable-Tic-Tac-Toe-AI-1"):
            source = ast.parse((root / folder / "main.py").read_text())
            definitions = ast.Module(body=[n for n in source.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.ClassDef, ast.FunctionDef))], type_ignores=[])
            scope = {}
            exec(compile(definitions, folder, "exec"), scope)
            node = scope["TreeNode"]([list("XXX"), list("OO-"), list("---")], "O")
            with contextlib.redirect_stdout(io.StringIO()):
                tree = scope["Tree"](node)
            self.assertIs(tree.root, node)

    def test_legacy_console_reprompts_for_noninteger_input(self):
        from unittest.mock import patch
        import contextlib, io
        for folder in ('FAI7-Unbeatable-Tic-Tac-Toe-AI', 'FAI7-Unbeatable-Tic-Tac-Toe-AI-1'):
            path = Path(__file__).parent.parent / folder / "main.py"
            spec = importlib.util.spec_from_file_location("legacy_game", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            with contextlib.redirect_stdout(io.StringIO()):
                tree = module.Tree(module.TreeNode([list("XX-"), list("OO-"), list("---")], "X"))
                with patch("builtins.input", side_effect=["", "bad", "0", "2"]):
                    tree.play_game()


if __name__ == "__main__":
    unittest.main()
