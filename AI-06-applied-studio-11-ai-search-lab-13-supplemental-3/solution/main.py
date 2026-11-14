from studio import breadth_first_search


def solve_extension():
    graph = {"S": ["A", "B", "C"], "A": ["D", "E"], "B": ["F"], "C": ["G"]}
    result = breadth_first_search(graph, "S", "G")
    return {"peak_frontier": max(len(row["frontier"]) for row in result["trace"]),
            "expanded": len(result["expanded"])}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
