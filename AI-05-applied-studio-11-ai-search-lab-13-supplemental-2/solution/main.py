from studio import breadth_first_search


def solve_extension():
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["A", "G"], "D": ["G"], "G": []}
    result = breadth_first_search(graph, "A", "G")
    return {"path": result["path"], "expanded": result["expanded"]}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
