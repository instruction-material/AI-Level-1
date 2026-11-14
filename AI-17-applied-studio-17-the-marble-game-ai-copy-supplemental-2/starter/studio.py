def validate(pile):
    if not isinstance(pile, int) or isinstance(pile, bool) or not 0 <= pile <= 100:
        raise ValueError("Use an integer pile from 0 to 100.")
    return pile


def legal_moves(pile):
    return list(range(1, min(3, validate(pile)) + 1))


def take(pile, move):
    if not isinstance(move, int) or isinstance(move, bool) or move not in legal_moves(pile):
        raise ValueError("Take 1, 2 or 3, without exceeding the pile.")
    return pile - move


def winning_positions(pile):
    validate(pile)
    winning = [False]
    for current in range(1, pile + 1):
        winning.append(any(not winning[current - move] for move in legal_moves(current)))
    return winning


def candidate_scores(pile):
    winning = winning_positions(pile)
    return [{"move": move, "remaining": pile-move, "opponent_winning": winning[pile-move]} for move in legal_moves(pile)]


def baseline_move(pile, rng=None):
    from random import Random
    moves = legal_moves(pile)
    return (rng or Random()).choice(moves) if moves else None


def best_move(pile):
    candidates = candidate_scores(pile)
    if not candidates:
        return None
    return next((c["move"] for c in candidates if not c["opponent_winning"]), candidates[0]["move"])


def main():
    pile = 5
    human = True
    while pile:
        print("Marbles:", pile)
        if human:
            try:
                move = int(input("Take 1, 2 or 3: "))
                next_pile = take(pile, move)
            except ValueError as error:
                print(error)
                continue
            except (EOFError, KeyboardInterrupt):
                print("Game ended.")
                return
        else:
            print("AI candidates:", candidate_scores(pile))
            move = best_move(pile)
            next_pile = take(pile, move)
            print("AI takes:", move)
        pile = next_pile
        if pile == 0:
            print("Winner:", "human" if human else "AI")
            return
        human = not human


if __name__ == "__main__":
    main()
