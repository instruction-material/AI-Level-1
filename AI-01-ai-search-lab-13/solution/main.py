from collections import deque

GRAPH = {
    "A": ["B", "C"], "B": ["D"], "C": ["E", "F"],
    "D": [], "E": [], "F": [],
}


def breadth_first_search(graph, start, goal):
    queue = deque([start])
    parents = {start: None}
    expanded = []
    trace = []
    while queue:
        node = queue.popleft()
        expanded.append(node)
        if node != goal:
            for neighbor in graph.get(node, []):
                if neighbor not in parents:
                    parents[neighbor] = node
                    queue.append(neighbor)
        trace.append({
            "node": node, "frontier": list(queue),
            "visited": list(parents), "parents": dict(parents),
        })
        if node == goal:
            path = []
            cursor = goal
            while cursor is not None:
                path.append(cursor)
                cursor = parents[cursor]
            return {"path": path[::-1], "expanded": expanded, "trace": trace}
    return {"path": [], "expanded": expanded, "trace": trace}


def breadth_first_path(start, goal):
    return breadth_first_search(GRAPH, start, goal)["path"]


def main():
    result = breadth_first_search(GRAPH, "A", "F")
    for step in result["trace"]:
        print(step)
    print("Path:", result["path"])


if __name__ == "__main__":
    main()
