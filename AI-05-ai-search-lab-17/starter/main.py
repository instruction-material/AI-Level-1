GOAL = (1, 2, 3, 0)


def neighbors(state):
    # TODO: yield states formed by sliding one adjacent tile into the blank (0).
    raise NotImplementedError("Generate legal puzzle moves.")


def misplaced(state):
    return sum(tile != 0 and tile != GOAL[i] for i, tile in enumerate(state))


def blank_distance(state):
    row, column = divmod(state.index(0), 2)
    return abs(row - 1) + abs(column - 1)


def solve(start, strategy="bfs", heuristic=misplaced):
    # TODO: compare FIFO BFS with greedy priority by heuristic; prevent cycles.
    # Return path, moves and decisions (state, score, candidate states/scores).
    raise NotImplementedError("Implement the puzzle comparison.")


def main():
    start = (1, 0, 3, 2)
    for strategy, heuristic in (("bfs", misplaced), ("greedy", misplaced), ("greedy", blank_distance)):
        print(strategy, solve(start, strategy, heuristic))


if __name__ == "__main__":
    main()
