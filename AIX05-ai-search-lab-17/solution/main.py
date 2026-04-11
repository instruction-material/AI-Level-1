from collections import deque

GRAPH = {
	"A": ["B", "C"],
	"B": ["D"],
	"C": ["E", "F"],
	"D": [],
	"E": [],
	"F": [],
}


def breadth_first_path(start: str, goal: str) -> list[str]:
	queue: deque[list[str]] = deque([[start]])
	visited = {start}
	while queue:
		path = queue.popleft()
		node = path[-1]
		if node == goal:
			return path
		for neighbor in GRAPH[node]:
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append([*path, neighbor])
	return []


def main() -> None:
	print(breadth_first_path("A", "F"))


if __name__ == "__main__":
	main()
