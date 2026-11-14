from random import Random
from studio import EMPTY, baseline_move, best_move, legal_moves, play, winner


def solve_extension():
    rng = Random(7)
    outcomes = {"games": 20, "X_wins": 0, "O_wins": 0, "draws": 0}
    for _ in range(20):
        board = EMPTY
        while legal_moves(board):
            move = baseline_move(board, rng) if board.count("X") == board.count("O") else best_move(board)
            board = play(board, move)
        won = winner(board)
        outcomes["draws" if won is None else won + "_wins"] += 1
    return outcomes

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
