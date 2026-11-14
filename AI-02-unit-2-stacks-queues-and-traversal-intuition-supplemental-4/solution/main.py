from collections import deque

GRAPH = {"S": ["A", "B"], "A": ["C"], "B": ["D", "S"], "C": ["G"], "D": [], "G": []}


def traversal(policy):
    if policy not in ("stack", "queue"):
        raise ValueError("Use stack or queue.")
    frontier = deque(["S"])
    visited, order = set(), []
    while frontier:
        node = frontier.pop() if policy == "stack" else frontier.popleft()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in GRAPH.get(node, []):
            if neighbor not in visited:
                frontier.append(neighbor)
    return order


def solve_extension():
    return {policy: traversal(policy) for policy in ("stack", "queue")}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
