import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("game_reference", Path(__file__).parent / "solution" / "main.py")
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)


class MarbleContract(unittest.TestCase):
    def test_legal_terminal_and_strategy_cases(self):
        self.assertEqual(game.legal_moves(0), [])
        self.assertIsNone(game.best_move(0))
        self.assertEqual([game.best_move(n) for n in (1, 4, 5, 7)], [1, 1, 1, 3])
        for n in range(1, 101):
            self.assertEqual(game.winning_positions(n)[n], n % 4 != 0)
            move = game.best_move(n)
            self.assertIn(move, game.legal_moves(n))
            if n % 4:
                self.assertEqual(game.take(n, move) % 4, 0)
        for pile, move in ((5, 0), (5, 4), (1, 2), (5, True), (5, 1.5)):
            with self.assertRaises(ValueError):
                game.take(pile, move)
        for pile in (-1, 101, True):
            with self.assertRaises(ValueError):
                game.legal_moves(pile)

    def test_seeded_baseline_and_independent_legacy_constructor(self):
        from random import Random
        self.assertEqual(game.baseline_move(5, Random(7)), 2)
        import ast
        root = Path(__file__).parent.parent
        for folder in ("FAI8-The-Marble-Game-AI", "FAI8-The-Marble-Game-AI-Copy"):
            source = ast.parse((root / folder / "main.py").read_text())
            definitions = ast.Module(body=[n for n in source.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.ClassDef, ast.FunctionDef))], type_ignores=[])
            scope = {}
            exec(compile(definitions, folder, "exec"), scope)
            node = scope["TreeNode"](0, False)
            self.assertIs(scope["Tree"](node).root, node)

    def test_legacy_console_reprompts_for_noninteger_input(self):
        from unittest.mock import patch
        import contextlib, io
        for folder in ('FAI8-The-Marble-Game-AI', 'FAI8-The-Marble-Game-AI-Copy'):
            path = Path(__file__).parent.parent / folder / "main.py"
            spec = importlib.util.spec_from_file_location("legacy_game", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            with contextlib.redirect_stdout(io.StringIO()):
                tree = module.Tree(module.TreeNode(1, False))
                with patch("builtins.input", side_effect=["", "bad", "1"]):
                    tree.play_game()


if __name__ == "__main__":
    unittest.main()
