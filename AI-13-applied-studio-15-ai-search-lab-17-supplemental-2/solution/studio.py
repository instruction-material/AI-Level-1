from collections import deque
from heapq import heappop, heappush
from itertools import count

GOAL = (1, 2, 3, 0)


def neighbors(state):
    blank = state.index(0)
    row, column = divmod(blank, 2)
    for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        nr, nc = row + dr, column + dc
        if 0 <= nr < 2 and 0 <= nc < 2:
            target = 2 * nr + nc
            board = list(state)
            board[blank], board[target] = board[target], board[blank]
            yield tuple(board)


def misplaced(state):
    return sum(tile != 0 and tile != GOAL[i] for i, tile in enumerate(state))


def blank_distance(state):
    row, column = divmod(state.index(0), 2)
    return abs(row - 1) + abs(column - 1)


def solve(start, strategy="bfs", heuristic=misplaced):
    if len(start) != 4 or set(start) != {0, 1, 2, 3}:
        raise ValueError("Use each of 0, 1, 2 and 3 exactly once.")
    start = tuple(start)
    if strategy not in ("bfs", "greedy"):
        raise ValueError("Use bfs or greedy.")
    serial = count()
    queue = deque([(start, [start])])
    heap = [(heuristic(start), next(serial), start, [start])]
    visited = set()
    decisions = []
    while queue if strategy == "bfs" else heap:
        if strategy == "bfs":
            state, path = queue.popleft()
        else:
            _, _, state, path = heappop(heap)
        if state in visited:
            continue
        visited.add(state)
        candidates = [{"state": child, "score": heuristic(child)} for child in neighbors(state)]
        decisions.append({"state": state, "score": heuristic(state), "candidates": candidates})
        if state == GOAL:
            return {"path": path, "moves": len(path) - 1, "decisions": decisions}
        for child in neighbors(state):
            if child not in visited:
                if strategy == "bfs":
                    queue.append((child, path + [child]))
                else:
                    heappush(heap, (heuristic(child), next(serial), child, path + [child]))
    return {"path": [], "moves": None, "decisions": decisions}


def main():
    start = (1, 0, 3, 2)
    for label, strategy, heuristic in (
        ("BFS baseline", "bfs", misplaced),
        ("Greedy misplaced", "greedy", misplaced),
        ("Greedy blank-distance", "greedy", blank_distance),
    ):
        result = solve(start, strategy, heuristic)
        print(label, "moves:", result["moves"])
        for decision in result["decisions"]:
            print(decision)


if __name__ == "__main__":
    main()
