from functools import lru_cache

EMPTY = ("-",) * 9
LINES = ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))


def winner(board):
    for a, b, c in LINES:
        if board[a] != "-" and board[a] == board[b] == board[c]:
            return board[a]
    return None


def validate(board):
    if len(board) != 9 or any(cell not in ("-", "X", "O") for cell in board):
        raise ValueError("Use nine cells containing X, O or -.")
    x, o = board.count("X"), board.count("O")
    wins = {board[a] for a, b, c in LINES if board[a] != "-" and board[a] == board[b] == board[c]}
    if x not in (o, o+1) or len(wins) > 1 or ("X" in wins and x != o+1) or ("O" in wins and x != o):
        raise ValueError("Board is inconsistent with X moving first.")
    return tuple(board)


def legal_moves(board):
    board = validate(board)
    return [] if winner(board) else [i for i, cell in enumerate(board) if cell == "-"]


def play(board, index):
    board = validate(board)
    if not isinstance(index, int) or isinstance(index, bool) or index not in legal_moves(board):
        raise ValueError("Choose an empty square in an unfinished game.")
    player = "X" if board.count("X") == board.count("O") else "O"
    return board[:index] + (player,) + board[index+1:]


@lru_cache(maxsize=None)
def minimax(board):
    won = winner(board)
    if won:
        return 1 if won == "O" else -1
    moves = [i for i, cell in enumerate(board) if cell == "-"]
    if not moves:
        return 0
    player = "X" if board.count("X") == board.count("O") else "O"
    values = [minimax(board[:i] + (player,) + board[i+1:]) for i in moves]
    return max(values) if player == "O" else min(values)


def candidate_scores(board):
    return [{"move": i, "score": minimax(play(board, i))} for i in legal_moves(board)]


def baseline_move(board, rng=None):
    from random import Random
    moves = legal_moves(board)
    return (rng or Random()).choice(moves) if moves else None


def best_move(board):
    board = validate(board)
    candidates = candidate_scores(board)
    if not candidates:
        return None
    target = max if board.count("X") > board.count("O") else min
    value = target(candidate["score"] for candidate in candidates)
    return next(candidate["move"] for candidate in candidates if candidate["score"] == value)


def display(board):
    for i in (0, 3, 6):
        print(" ".join(board[i:i+3]))


def main():
    board = EMPTY
    while legal_moves(board):
        display(board)
        if board.count("X") == board.count("O"):
            try:
                index = int(input("Square for X (1-9): ")) - 1
                board = play(board, index)
            except ValueError as error:
                print(error)
                continue
            except (EOFError, KeyboardInterrupt):
                print("Game ended.")
                return
        else:
            print("O candidates:", candidate_scores(board))
            board = play(board, best_move(board))
    display(board)
    print("Winner:", winner(board) or "draw")


if __name__ == "__main__":
    main()
