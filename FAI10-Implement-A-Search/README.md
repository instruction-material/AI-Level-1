# A* Search

Run `python3 main.py`. The two references use the same undirected graph:

| Edge | Cost |
| --- | ---: |
| S-A | 1 |
| A-G | 20 |
| S-B | 5 |
| B-G | 1 |

The state estimates are `h(S)=0, h(A)=0, h(B)=1, h(G)=0`. Each is a lower bound on the actual remaining cost. An estimate belongs to a state and a chosen goal; an incoming edge's weight is a step cost.

A* prioritizes `f(n)=g(n)+h(n)`. Here `g` is the cheapest cost discovered from S, and `h` estimates the remaining cost to G. Expected expansion: `S A B G`. Expected path: `S -> B -> G`, cost **6**.

A newly cheaper route updates the parent and reopens the state. Old queue entries are skipped. With nonnegative edge costs, an admissible heuristic and zero at the goal, the first popped goal has minimum path cost, including with an inconsistent heuristic when reopening is allowed. The code checks finite nonnegative costs and estimates; admissibility is a property to justify for the particular problem. Set every estimate to zero to obtain uniform-cost search.

The original `Node(key)` and one-argument search calls remain supported: estimates default to zero, and omitting a goal explores all reachable states. A two-argument call returns the expansion `order`, `path`, `cost` and best-known or first-discovery `costs`. An unreachable goal returns an empty path and `None` cost. Equal priorities use node keys to break ties. These are completed reference examples; create a separate working copy to implement and compare the two algorithms.
