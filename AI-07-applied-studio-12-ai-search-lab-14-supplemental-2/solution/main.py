from studio import depth_limited_search


def solve_extension():
    graph = {"S": ["A", "B"], "A": ["X"], "X": ["C"], "B": ["C"], "C": ["G"]}
    return {str(limit): depth_limited_search(graph, "S", "G", limit)["status"] for limit in range(4)}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
