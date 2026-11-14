from itertools import permutations
from studio import GOAL, blank_distance, solve


def solve_extension():
    results = [(state, solve(state)["moves"]) for state in permutations(range(4))]
    reachable = [(state, moves) for state, moves in results if moves is not None]
    return {"reachable": len(reachable), "unreachable": len(results) - len(reachable),
            "max_shortest_moves": max(moves for _, moves in reachable),
            "false_zero_scores": sum(state != GOAL and blank_distance(state) == 0 for state, _ in reachable)}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
