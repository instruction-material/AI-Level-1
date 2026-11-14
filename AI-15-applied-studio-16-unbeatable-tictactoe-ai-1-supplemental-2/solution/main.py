from studio import best_move


def solve_extension():
    original = tuple("XX--O----")
    rotated = tuple(original[(2-column)*3+row] for row in range(3) for column in range(3))
    return {"board": "".join(rotated), "block": best_move(rotated)}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
