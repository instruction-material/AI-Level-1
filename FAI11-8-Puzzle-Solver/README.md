# Sliding 8-Puzzle

Run `python3 main.py` with the Python standard library. The default board is `123/456/ 78`: both BFS and A* reach `123/456/78 ` in **2 moves**. Output counts moves as the number of transitions, one less than the number of displayed states.

Boards contain each of 1 through 8 and one space on a 3-by-3 grid. A move swaps the space with one orthogonal neighbor. The Manhattan estimate sums numbered-tile distances and excludes the space, so each action can reduce the estimate by at most one. A* records the cheapest arrival and discards stale frontier entries; every sibling has parent cost plus one.

On this odd-width board, an odd inversion count cannot reach the goal. Both searches detect it before expansion. The example `865/142/7 3` has 19 inversions and is unsolvable. Replace the default with another valid board to compare search effort; harder boards expand more states.
