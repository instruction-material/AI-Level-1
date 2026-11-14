def legal_moves(pile):
    # TODO: validate 0..100 marbles; legal takes are 1..min(3,pile).
    raise NotImplementedError("Generate legal marble moves.")


def take(pile, move):
    # TODO: reject an illegal take and return the remaining pile.
    raise NotImplementedError("Apply one legal take.")


def candidate_scores(pile):
    # TODO: a zero pile loses for the player whose turn it is.
    # Score each move with remaining and opponent_winning.
    raise NotImplementedError("Evaluate the resulting positions.")


def best_move(pile):
    # TODO: prefer a move leaving a losing position for the opponent.
    # Tie-break with the lowest take; return None at pile zero.
    raise NotImplementedError("Choose a legal move.")


def main():
    for pile in (1, 4, 5, 7):
        print(pile, candidate_scores(pile), best_move(pile))


if __name__ == "__main__":
    main()
