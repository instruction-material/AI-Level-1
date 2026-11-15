# Deck of Cards

Run `python3 main.py`. The deck contains 52 distinct cards: values 1 through 13 in Spades, Hearts, Clubs and Diamonds. Drawing removes the front card; drawing from an empty deck prints a message and returns `None`.

The Fisher-Yates shuffle walks backward. At index `i`, choose uniformly from 0 through `i`, swap, and leave that final position fixed. For a three-card deck there are 3 times 2 equally likely choice sequences and each produces a different permutation. Repeatedly choosing from the entire deck gives some permutations higher probability.
