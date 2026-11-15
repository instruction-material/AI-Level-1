import math
import queue


class Node:
    """A state and its estimated remaining cost to a chosen goal."""

    def __init__(self, key, heuristic=0):
        if (not isinstance(heuristic, (int, float))
                or not math.isfinite(heuristic) or heuristic < 0):
            raise ValueError("Heuristics must be finite nonnegative numbers")
        self.key = key
        self.heuristic = heuristic
        self.neighbors = {}

    def add_neighbor(self, node, weight):
        self.neighbors[node.key] = weight

    def __str__(self):
        neighbors = "  ".join(key + ":" + str(cost) for key, cost in self.neighbors.items())
        return "ID: " + self.key + "\nNeighbors: " + neighbors

    def __lt__(self, other):
        return self.key < other.key


class Graph:
    """An undirected graph with finite nonnegative edge costs."""

    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        self.graph[node.key] = node

    def get_node(self, key):
        return self.graph.get(key)

    def get_nodes(self):
        return list(self.graph)

    def add_edge(self, node1, node2, weight):
        self._require_node(node1)
        self._require_node(node2)
        if (not isinstance(weight, (int, float))
                or not math.isfinite(weight) or weight < 0):
            raise ValueError("Edge costs must be finite nonnegative numbers")
        node1.add_neighbor(node2, weight)
        node2.add_neighbor(node1, weight)

    def _require_node(self, node):
        if self.graph.get(node.key) is not node:
            raise ValueError("Add this node to the graph before searching or adding edges")

    def __str__(self):
        return "\n\n".join(str(node) for node in self.graph.values())

    @staticmethod
    def _path(parents, goal_key):
        path = []
        while goal_key is not None:
            path.append(goal_key)
            goal_key = parents[goal_key]
        return path[::-1]

    def a_star_search(self, start_node, goal_node=None):
        """Use f = g + h; a cheaper route may reopen an expanded state."""
        self._require_node(start_node)
        if goal_node is not None:
            self._require_node(goal_node)
            if goal_node.heuristic != 0:
                raise ValueError("A* requires a zero heuristic at the goal")
        frontier = queue.PriorityQueue()
        frontier.put((start_node.heuristic, 0, start_node))
        best_cost = {start_node.key: 0}
        parents = {start_node.key: None}
        order = []

        while not frontier.empty():
            _, cost, node = frontier.get()
            if cost != best_cost[node.key]:
                continue  # A better route superseded this queued entry.
            order.append(node.key)
            print(node.key, end=" ")
            if node is goal_node:
                return {"order": order, "path": self._path(parents, node.key),
                        "cost": cost, "costs": best_cost}
            for key, weight in node.neighbors.items():
                candidate = cost + weight
                if candidate < best_cost.get(key, math.inf):
                    best_cost[key] = candidate
                    parents[key] = node.key
                    neighbor = self.graph[key]
                    frontier.put((candidate + neighbor.heuristic, candidate, neighbor))

        return {"order": order, "path": [], "cost": None, "costs": best_cost}


# Both search references use this same graph and admissible state estimates.
# The zero estimate at A makes it tempting despite its expensive route to G.
g = Graph()
nodes = {key: Node(key, heuristic) for key, heuristic in
         [("S", 0), ("A", 0), ("B", 1), ("G", 0)]}
for node in nodes.values():
    g.add_node(node)
for left, right, weight in [("S", "A", 1), ("A", "G", 20),
                             ("S", "B", 5), ("B", "G", 1)]:
    g.add_edge(nodes[left], nodes[right], weight)

result = g.a_star_search(nodes["S"], nodes["G"])
print()
print("Path:", " -> ".join(result["path"]))
print("Cost:", result["cost"])
