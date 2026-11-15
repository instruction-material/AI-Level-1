# Maze Search Comparison

Run `python3 main.py` beside `maze.py`. The supplied directed graph represents the pictured maze; leaving quicksand costs 10, while other edges cost 1. BFS/IDS compare the number of moves, UCS compares total cost, and DFS follows its stack order.

DLS and IDS preserve the best depth reached for each cell. A later shallower arrival can re-expand a cell and reach a goal within the requested limit. The counterexample S-A, S-B, B-C, C-X, A-X, X-G has a three-move route S-A-X-G; a global visited set can miss it. DLS returns no path when the goal is unreachable within the limit. A negative limit retains the original empty-list result.
