from collections import deque

#################
#   CONSTANTS   #
#################

GRAPH: dict[str, list[str]] = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["E", "F"],
    "D": [],
    "E": [],
    "F": [],
}
START_NODE = "A"
GOAL_NODE = "F"


#################
#   FUNCTIONS   #
#################


def breadth_first_path(start: str, goal: str) -> list[str]:
    """Find a path from start to goal using breadth-first search"""
    queue: deque[list[str]] = deque([[start]])
    visited = {start}

    # Explore queued paths in order so shorter paths are checked first
    while queue:
        path = queue.popleft()
        node = path[-1]

        # Stop as soon as the goal node is reached
        if node == goal:
            return path

        # Add each unvisited neighbor as a new candidate path
        for neighbor in GRAPH[node]:
            # Visit each graph node at most once
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append([*path, neighbor])

    return []


def main() -> None:
    """Print the sample breadth-first path"""
    print(breadth_first_path(START_NODE, GOAL_NODE))


if __name__ == "__main__":
    main()
