from studio import search


def solve_extension():
    graph = {"S": [("A", 3), ("B", 1)], "B": [("A", 1)], "A": [("G", 2)], "G": []}
    estimates = {"S": 0, "A": 0, "B": 3, "G": 0}
    result = search(graph, "S", "G", estimates, "astar")
    return {"cost": result["cost"], "A_pops": sum(row["node"] == "A" for row in result["trace"])}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
