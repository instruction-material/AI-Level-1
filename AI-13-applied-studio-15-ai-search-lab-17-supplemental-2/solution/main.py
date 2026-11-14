from studio import solve


def solve_extension():
    states = [(3, 1, 0, 2), (0, 1, 3, 2), (1, 0, 3, 2), (1, 3, 2, 0)]
    return {"moves": [solve(state)["moves"] for state in states]}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
