GRAPH = {"S": ["A", "B"], "A": ["C"], "B": [], "C": ["G"], "G": []}


def depth_limited_search(graph, start, goal, limit):
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise ValueError("Depth limit must be a nonnegative integer.")
    visits = []

    def visit(path, remaining):
        node = path[-1]
        visits.append({"node": node, "depth": len(path) - 1})
        if node == goal:
            return "found", path
        children = [n for n in graph.get(node, []) if n not in path]
        if not children:
            return "failure", []
        if remaining == 0:
            return "cutoff", []
        cut_off = False
        for neighbor in children:
            status, answer = visit(path + [neighbor], remaining - 1)
            if status == "found":
                return status, answer
            cut_off = cut_off or status == "cutoff"
        return ("cutoff" if cut_off else "failure"), []

    status, path = visit([start], limit)
    return {"status": status, "path": path, "visits": visits}


def iterative_deepening(graph, start, goal, maximum_depth):
    if not isinstance(maximum_depth, int) or isinstance(maximum_depth, bool) or maximum_depth < 0:
        raise ValueError("Maximum depth must be a nonnegative integer.")
    attempts = []
    for limit in range(maximum_depth + 1):
        result = depth_limited_search(graph, start, goal, limit)
        attempts.append({"limit": limit, **result})
        if result["status"] != "cutoff":
            return {**result, "attempts": attempts}
    return {**result, "attempts": attempts}


def main():
    for limit in (0, 2, 3, 4):
        print("DLS", limit, depth_limited_search(GRAPH, "S", "G", limit))
    print("IDS", iterative_deepening(GRAPH, "S", "G", 4))


if __name__ == "__main__":
    main()
