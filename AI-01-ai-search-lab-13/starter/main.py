GRAPH = {"A": ["B", "C"], "B": ["D"], "C": ["E", "F"], "D": [], "E": [], "F": []}


def breadth_first_search(graph, start, goal):
    # TODO: use a FIFO frontier, discover each state once, and preserve parent links.
    # Return path, expanded order and a trace of node/frontier/visited/parents.
    raise NotImplementedError("Implement the instrumented BFS.")


def breadth_first_path(start, goal):
    return breadth_first_search(GRAPH, start, goal)["path"]


def main():
    print(breadth_first_search(GRAPH, "A", "F"))


if __name__ == "__main__":
    main()
