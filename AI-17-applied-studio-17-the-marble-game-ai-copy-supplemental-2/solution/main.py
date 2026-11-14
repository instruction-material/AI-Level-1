from studio import best_move, candidate_scores


def solve_extension():
    return {str(pile): {"take": best_move(pile), "winning_take_exists": any(not c["opponent_winning"] for c in candidate_scores(pile))}
            for pile in range(9, 13)}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
