# AI Level 1

Canonical source layout in this repo is folder-first: each project should live in
its own directory with any local assets beside it.

Generated Replit/Poetry files and old flat-layout export duplicates have been
removed. Keep starter and solution material in the project directory that owns
it; do not re-add root-level standalone copies or legacy archive folders.

- Course catalog entry: `/Users/jacobanderson/Sites/classes.jacobdanderson.net/front-end/src/stores/courses/ai-level-1.ts`
- GitHub repo clone: `/Users/jacobanderson/Documents/Work/Juni/AI Level 1`
- Legacy Dropbox source: `/Users/jacobanderson/Documents/Work/Juni/AI Level 1/dropbox-source`

## Search and game studios

Labs 13–17 have separate starter and solution folders for BFS instrumentation, depth limits, weighted search, greedy/A* comparison and puzzle evaluation. The Tic-Tac-Toe AI 1 and Marble Game AI Copy folders also provide separate starter/solution packs; their root scripts preserve the earlier tree-based variants. Each project README supplies worked inputs, expected behavior and boundaries.

Run ./verify-course-source.sh to check source readiness and all seven studio regression suites. The suites use only the Python standard library.

The eighteen optional projects each contain a worked case, expected result or outcome invariant, and a project-local regression check. Their starters isolate the new exercise; the studio options include their completed parent engine so extending the lesson does not require reimplementing the parent search or game.

## Earlier depth-limited traversal references

FAI9-Implement-DLS and FAI9-Implement-IDS retain their original graph classes and printed demonstrations. A later shallower route now re-expands a vertex so reachable descendants stay within the requested limit. Their READMEs supply the six-vertex counterexample. The source gate includes four independent regression checks, including all 64 undirected four-vertex graphs at each start and limits zero through three.
