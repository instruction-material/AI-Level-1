# Depth-limited graph traversal

Run python3 main.py to see the supplied undirected graph at successive limits. The printed order follows the stack and lists each reached vertex once.

A depth limit applies to the route from the start. Record the best depth seen for each vertex. If a later branch reaches that vertex more shallowly, expand it again: its descendants may now fit within the limit. Printing each vertex once is a display choice; it does not replace the depth comparison.

Counterexample: S connects to A and B, B to C, C to X, A to X, and X to G. Insert those edges in that order. With limit 3, the stack first reaches X through S,B,C,X at depth 3. The later route S,A,X reaches X at depth 2 and must discover G at depth 3. One global visited set would miss G. Expected unique first-visit output: S B C X A G.

A negative limit prints nothing. A cycle cannot cause indefinite work because another expansion requires a strictly smaller nonnegative depth. Disconnected vertices stay absent. Existing sample outputs remain unchanged.

Iterative deepening calls the same depth-limited traversal at limits 0 through the chosen maximum. Each call starts its own depth map. Compare its repeated work at each limit; the limit 3 line in this counterexample must include G.
