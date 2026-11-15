import time
from queue import PriorityQueue


# Node stores state of the game (board)
class Node:

    def __init__(self, board):
        self.board = board
        self.neighbors = []

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.board == other.board

    def __lt__(self, other):
        return self.board < other.board

    def __str__(self):
        ret = ''
        for row in self.board:
            for space in row:
                ret += space + ' '
            ret += '\n'
        return ret

    # board's hash code is it's sequence of values from
    # top left to bottom right as an int (empty space is 0)
    def __hash__(self):
        total = ''
        for row in self.board:
            for space in row:
                if space != ' ':
                    total += space
                else:
                    total += '0'
        return int(total)

    # returns True if board is solved, False otherwise
    def is_solved(self):
        correct = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', ' '],
        ]
        return self.board == correct

    # calculate the heuristic for the A* search
    # heuristic is the sum of the manhattan distances of each tile from its correct positions
    def get_heuristic(self):
        total = 0
        correct = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', ' '],
        ]

        # maps each value in correct to its coordinate
        correct_coords = {}
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                correct_coords[correct[i][j]] = (i, j)

        # calculate distance of each tile from the
        # correct position and add it to total
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                num = self.board[i][j]
                if num == " ":
                    continue
                x_dist = abs(i - correct_coords[num][0])
                y_dist = abs(j - correct_coords[num][1])
                total += x_dist + y_dist

        return total

    # generates all neighbors of a node by expanding it
    def is_solvable(self):
        # A valid 3-by-3 board reaches the goal exactly when inversion parity is even.
        values = [tile for row in self.board for tile in row if tile != " "]
        inversions = sum(left > right for i, left in enumerate(values)
                         for right in values[i + 1:])
        return inversions % 2 == 0

    def generate_neighbors(self):
        neighbors = []

        # find and store coordinates of empty space in the board
        row = -1
        col = -1
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == ' ':
                    row = i
                    col = j
                    break

        # list of possible directions space can move
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        # loop through each possible movement
        for r, c in dirs:
            new_row = row + r
            new_col = col + c

            # if move is valid (new row and column are within bounds of the board), create and add child node to children
            if 0 <= new_row <= 2 and 0 <= new_col <= 2:

                # make copy of board
                new_board = []
                for line in self.board:
                    board_row = []
                    for space in line:
                        board_row.append(space)
                    new_board.append(board_row)

                # switch space to new location and switch number to space's old location
                new_board[new_row][new_col] = ' '
                new_board[row][col] = self.board[new_row][new_col]

                # create and add child to neighbors
                node = Node(new_board)
                neighbors.append(node)

        self.neighbors = neighbors


# stores the start node of the puzzle and methods to solve it
class PuzzleGraph:

    def __init__(self, start_node):
        self.start_node = start_node

    # solve puzzle with BFS
    def bfs_solve(self):
        if not self.start_node.is_solvable():
            return None
        from collections import deque
        frontier = deque([(self.start_node, [self.start_node])])
        visited = {self.start_node}
        count = 0
        while frontier:
            node, path = frontier.popleft()
            count += 1
            if node.is_solved():
                return path, count
            node.generate_neighbors()
            for neighbor in node.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    frontier.append((neighbor, path + [neighbor]))
        return None


    # solve puzzle with A* Search
    def a_star_solve(self):
        if not self.start_node.is_solvable():
            return None
        frontier = PriorityQueue()
        frontier.put((self.start_node.get_heuristic(), 0, self.start_node,
                      [self.start_node]))
        best_cost = {self.start_node: 0}
        count = 0
        while not frontier.empty():
            _, cost, node, path = frontier.get()
            if cost != best_cost[node]:
                continue
            count += 1
            if node.is_solved():
                return path, count
            node.generate_neighbors()
            for neighbor in node.neighbors:
                next_cost = cost + 1
                if next_cost < best_cost.get(neighbor, float("inf")):
                    best_cost[neighbor] = next_cost
                    frontier.put((next_cost + neighbor.get_heuristic(), next_cost,
                                  neighbor, path + [neighbor]))
        return None



start_board = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    [' ', '7', '8'],
]
graph = PuzzleGraph(Node(start_board))
for name, solve in [("BFS", graph.bfs_solve), ("A*", graph.a_star_solve)]:
    print("Running " + name + "...")
    started = time.time()
    result = solve()
    print("Time:", time.time() - started)
    if result is None:
        print("Unsolvable starting board")
        continue
    path, count = result
    print("Number of States Searched:", count)
    print("Moves:", len(path) - 1)
    for node in path:
        print(node)
