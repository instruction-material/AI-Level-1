"""Independent amount-state and shuffle-distribution checks."""
import ast
import collections
import contextlib
import io
import itertools
import math
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent


def classes(folder):
    path = ROOT / folder / "main.py"
    tree = ast.parse(path.read_text())
    tree.body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.ClassDef))]
    scope = {}
    exec(compile(tree, str(path), "exec"), scope)
    return scope


class LegacyObjects(unittest.TestCase):
    def test_negative_or_nonfinite_amount_never_mutates_balance(self):
        Account = classes("FAI1-Bank-Account-Class")["BankAccount"]
        for method, amount in itertools.product(
                ["deposit", "withdraw"], [-1, -25, math.inf, -math.inf, math.nan, "5"]):
            account = Account("Example", 0.1)
            account.deposit(100)
            with self.assertRaises(ValueError):
                getattr(account, method)(amount)
            self.assertEqual(account.balance, 100)

    def test_supported_amounts_interest_and_overdraw_keep_original_behavior(self):
        account = classes("FAI1-Bank-Account-Class")["BankAccount"]("Example", 0.1)
        account.deposit(1000)
        account.calculate_interest()
        self.assertEqual(account.balance, 1100)
        account.withdraw(1000)
        self.assertEqual(account.balance, 100)
        for method in ["deposit", "withdraw"]:
            getattr(account, method)(0)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            account.withdraw(150)
        self.assertIn("Not enough balance", out.getvalue())
        self.assertEqual(account.balance, 100)

    def test_full_deck_preserves_all_distinct_cards_through_shuffle_and_draw(self):
        scope = classes("FAI1-Deck-of-Cards")
        deck = scope["Deck"]()
        expected = {(value, suit) for value in range(1, 14)
                    for suit in ["Spades", "Hearts", "Clubs", "Diamonds"]}
        self.assertEqual({(c.value, c.suit) for c in deck.deck}, expected)
        deck.shuffle()
        drawn = [deck.draw_card() for _ in range(52)]
        self.assertEqual({(c.value, c.suit) for c in drawn}, expected)
        self.assertEqual(len(deck.deck), 0)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(deck.draw_card())

    def test_all_three_card_shuffle_outcomes_have_equal_probability(self):
        scope = classes("FAI1-Deck-of-Cards")
        distribution = collections.Counter()
        for choices in itertools.product(range(3), range(2)):
            deck = scope["Deck"]()
            deck.deck = list("ABC")
            with patch.object(scope["random"], "randint", side_effect=choices):
                deck.shuffle()
            distribution[tuple(deck.deck)] += 1
        self.assertEqual(set(distribution), set(itertools.permutations("ABC")))
        self.assertEqual(set(distribution.values()), {1})

    def test_empty_and_single_card_shuffle_keep_their_contents(self):
        Deck = classes("FAI1-Deck-of-Cards")["Deck"]
        for cards in [[], ["only"]]:
            deck = Deck()
            deck.deck = cards.copy()
            deck.shuffle()
            self.assertEqual(deck.deck, cards)

    def test_complete_examples_run(self):
        for folder in ["FAI1-Bank-Account-Class", "FAI1-Deck-of-Cards"]:
            with contextlib.redirect_stdout(io.StringIO()):
                runpy.run_path(str(ROOT / folder / "main.py"))


if __name__ == "__main__":
    unittest.main()
