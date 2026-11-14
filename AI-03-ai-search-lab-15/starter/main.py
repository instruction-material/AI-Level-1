GRAPH = {"S": [("A", 2), ("B", 1)], "A": [("G", 2)], "B": [("G", 8)], "G": []}
ADMISSIBLE = {"S": 3, "A": 2, "B": 0, "G": 0}
BAD = {"S": 3, "A": 100, "B": 0, "G": 0}


def search(graph, start, goal, heuristic=None, mode="ucs"):
    # TODO: UCS orders by g; A* orders by g+h. Reject negative edge costs.
    # Reopen a state if its g improves; skip stale queue entries.
    # Return path, cost and a node/g/h/f/priority trace.
    raise NotImplementedError("Implement UCS and A*.")


def main():
    for mode, heuristic in (("ucs", ADMISSIBLE), ("astar", ADMISSIBLE), ("astar", BAD)):
        print(mode, search(GRAPH, "S", "G", heuristic, mode))


if __name__ == "__main__":
    main()
