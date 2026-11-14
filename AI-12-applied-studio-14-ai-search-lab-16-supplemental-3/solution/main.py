from studio import GRAPH, search


def solve_extension():
    return {mode: search(GRAPH, "S", "G", {}, mode)["cost"] for mode in ("greedy", "astar")}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
