GRAPH = {"S": ["A", "B"], "A": ["C"], "B": [], "C": ["G"], "G": []}


def depth_limited_search(graph, start, goal, limit):
    # TODO: check the goal before the cutoff and avoid cycles on the current path.
    # Return status (found/cutoff/failure), path and node/depth visits.
    raise NotImplementedError("Implement depth-limited search.")


def iterative_deepening(graph, start, goal, maximum_depth):
    # TODO: restart DLS at depths 0..maximum_depth; retain each attempt.
    # Stop on found or failure; only cutoff justifies another depth.
    raise NotImplementedError("Implement iterative deepening.")


def main():
    print(iterative_deepening(GRAPH, "S", "G", 4))


if __name__ == "__main__":
    main()
