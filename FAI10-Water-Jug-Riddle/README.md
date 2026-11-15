# Water Jug Riddle

Run `python3 main.py`. Each action fills, empties or pours between the 3-liter and 5-liter jugs. The goal is 4 liters in the 5-liter jug. From (0,0), a shortest route takes **6 actions**.

Greedy search retains the volume-difference hint. It can overestimate: (2,5) reaches (3,4) in one pour even though its hint is 3. Its route is legal and does not carry a minimum-step guarantee.

A* instead uses the admissible estimate zero at a goal and one elsewhere. Each unit-cost action advances g by one; cheaper arrivals update the path, and stale entries are skipped. The regression oracle checks shortest routes from all 24 integer-volume states with 0 through 3 liters and 0 through 5 liters. This small estimate favors a clear correctness argument over aggressive pruning.
