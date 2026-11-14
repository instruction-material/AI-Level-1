EMPTY = ("-",) * 9
LINES = ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))


def winner(board):
    # TODO: return X or O for a winning line, otherwise None.
    raise NotImplementedError("Check all eight winning lines.")


def legal_moves(board):
    # TODO: validate the board; return empty squares, or [] after a win.
    raise NotImplementedError("Generate legal moves.")


def play(board, index):
    # TODO: validate the move; derive the current player from X/O counts.
    # Return a new tuple so sibling search branches do not share mutations.
    raise NotImplementedError("Apply one legal move.")


def candidate_scores(board):
    # TODO: evaluate legal successors with minimax: O win +1, X win -1, draw 0.
    raise NotImplementedError("Score candidate moves.")


def best_move(board):
    # TODO: O maximizes, X minimizes; tie-break by lowest square index.
    # Return None if the game is over.
    raise NotImplementedError("Choose a move from the scores.")


def main():
    board = ("X", "X", "-", "-", "O", "-", "-", "-", "-")
    print("Forced block for O:", best_move(board))


if __name__ == "__main__":
    main()
