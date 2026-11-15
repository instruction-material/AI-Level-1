# Greedy Best-First Search

Run `python3 main.py`. The two references use the same undirected graph:

| Edge | Cost |
| --- | ---: |
| S-A | 1 |
| A-G | 20 |
| S-B | 5 |
| B-G | 1 |

The state estimates are `h(S)=0, h(A)=0, h(B)=1, h(G)=0`. Each is a lower bound on the actual remaining cost. An estimate belongs to a state and a chosen goal; an incoming edge's weight is a step cost.

Greedy best-first search prioritizes `h(n)` alone. Expected expansion: `S A G`. Expected path: `S -> A -> G`, cost **21**. A looks promising, and the goal's zero estimate then brings it to the front, despite the expensive step from A. The A* companion finds a cost-6 route on this same graph.

Each state is discovered once. Its parent and accumulated route cost are recorded for reporting, while priority uses only its remaining-cost estimate. The algorithm stops at the goal and does not promise a cheapest path.

The original `Node(key)` and one-argument search calls remain supported: estimates default to zero, and omitting a goal explores all reachable states. A two-argument call returns the expansion `order`, `path`, `cost` and best-known or first-discovery `costs`. An unreachable goal returns an empty path and `None` cost. Equal priorities use node keys to break ties. These are completed reference examples; create a separate working copy to implement and compare the two algorithms.
