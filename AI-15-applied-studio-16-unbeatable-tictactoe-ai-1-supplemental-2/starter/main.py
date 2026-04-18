GRAPH = {
	"A": ["B", "C"],
	"B": ["D"],
	"C": ["E", "F"],
	"D": [],
	"E": [],
	"F": [],
}


def breadth_first_path(start: str, goal: str) -> list[str]:
	# TODO: return one path from start to goal.
	return []


def main() -> None:
	print(breadth_first_path("A", "F"))


if __name__ == "__main__":
	main()
