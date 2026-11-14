from studio import search


def solve_extension():
    graph = {"S": [("X", 1), ("Y", 2)], "X": [("G", 20)], "Y": [("G", 2)], "G": []}
    estimates = {"S": 2, "X": 0, "Y": 2, "G": 0}
    return {mode: search(graph, "S", "G", estimates, mode)["cost"] for mode in ("greedy", "astar")}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
