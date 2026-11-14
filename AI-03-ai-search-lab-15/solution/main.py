from heapq import heappop, heappush
from itertools import count
from math import isfinite

GRAPH = {"S": [("A", 2), ("B", 1)], "A": [("G", 2)], "B": [("G", 8)], "G": []}
ADMISSIBLE = {"S": 3, "A": 2, "B": 0, "G": 0}
BAD = {"S": 3, "A": 100, "B": 0, "G": 0}


def search(graph, start, goal, heuristic=None, mode="ucs"):
    if mode not in ("ucs", "astar", "greedy"):
        raise ValueError("Mode must be ucs, astar or greedy.")
    for edges in graph.values():
        for _, cost in edges:
            if not isfinite(cost) or cost < 0:
                raise ValueError("Edge costs must be finite and nonnegative.")
    heuristic = {} if heuristic is None else heuristic

    def h(node):
        value = heuristic.get(node, 0)
        if not isfinite(value) or value < 0:
            raise ValueError("Heuristics must be finite and nonnegative.")
        return value

    serial = count()

    def priority(g, estimate):
        return g if mode == "ucs" else estimate if mode == "greedy" else g + estimate

    queue = [(priority(0, h(start)), next(serial), start, 0, [start])]
    best = {start: 0}
    trace = []
    while queue:
        frontier = [
            {"node": entry[2], "g": entry[3], "h": h(entry[2]), "f": entry[3] + h(entry[2]), "priority": entry[0]}
            for entry in sorted(queue) if entry[3] == best.get(entry[2])
        ]
        score, _, node, cost, path = heappop(queue)
        if cost != best.get(node):
            continue
        estimate = h(node)
        trace.append({"node": node, "g": cost, "h": estimate, "f": cost + estimate, "priority": score, "frontier": frontier})
        if node == goal:
            return {"path": path, "cost": cost, "trace": trace}
        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            if new_cost < best.get(neighbor, float("inf")):
                best[neighbor] = new_cost
                heappush(queue, (priority(new_cost, h(neighbor)), next(serial), neighbor, new_cost, path + [neighbor]))
    return {"path": [], "cost": None, "trace": trace}

def main():
    for label, mode, heuristic in (("UCS", "ucs", ADMISSIBLE), ("A* admissible", "astar", ADMISSIBLE), ("A* bad", "astar", BAD)):
        print(label, search(GRAPH, "S", "G", heuristic, mode))


if __name__ == "__main__":
    main()
