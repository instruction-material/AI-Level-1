from collections import deque

GRAPH = {"S": ["A", "B"], "A": ["C"], "B": ["D", "S"], "C": ["G"], "D": [], "G": []}


def traversal(policy):
    # TODO: implement the README contract.
    raise NotImplementedError("Implement traversal.")


def solve_extension():
    # TODO: implement the README contract.
    raise NotImplementedError("Implement solve_extension.")


if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
