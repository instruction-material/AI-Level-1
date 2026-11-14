GRAPH = {"S": [("A", 2), ("B", 1)], "A": [("G", 2)], "B": [("G", 8)], "G": []}
ADMISSIBLE = {"S": 3, "A": 2, "B": 0, "G": 0}


def search(graph, start, goal, heuristic=None, mode="greedy"):
    # TODO: greedy orders by h; A* orders by g+h.
    # Keep g separately from priority, and log both candidate costs and scores.
    # Return path, cost and a node/g/h/f/priority trace.
    raise NotImplementedError("Compare greedy search and A*.")


def main():
    for mode in ("greedy", "astar"):
        print(mode, search(GRAPH, "S", "G", ADMISSIBLE, mode))


if __name__ == "__main__":
    main()
