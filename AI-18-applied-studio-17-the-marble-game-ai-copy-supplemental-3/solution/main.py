from random import Random
from studio import baseline_move, best_move, take


def solve_extension():
    rng = Random(7)
    result = {"games": 12, "AI_wins": 0, "opponent_wins": 0, "forced_start_wins": 0}
    for initial in range(1, 13):
        pile, ai_turn = initial, True
        while pile:
            move = best_move(pile) if ai_turn else baseline_move(pile, rng)
            pile = take(pile, move)
            if pile == 0:
                result["AI_wins" if ai_turn else "opponent_wins"] += 1
                if ai_turn and initial % 4:
                    result["forced_start_wins"] += 1
                break
            ai_turn = not ai_turn
    return result

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
