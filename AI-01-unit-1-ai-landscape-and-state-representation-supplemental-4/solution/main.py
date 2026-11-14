WIDTH, HEIGHT = 2, 2
BLOCKED = {(1, 0)}


def legal_next(position):
    row, column = position
    if not (0 <= row < HEIGHT and 0 <= column < WIDTH) or position in BLOCKED:
        raise ValueError("Use an unblocked grid position.")
    return [(r, c) for r, c in ((row-1, column), (row, column-1), (row, column+1), (row+1, column))
            if 0 <= r < HEIGHT and 0 <= c < WIDTH and (r, c) not in BLOCKED]


def solve_extension():
    return {"from_start": legal_next((0, 0)), "from_goal": legal_next((1, 1))}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
