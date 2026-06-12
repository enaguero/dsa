# Graphs

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Representations
- [ ] **Adjacency list**: `{node: [neighbors]}` — O(V+E) space, efficient for sparse graphs
- [ ] **Adjacency matrix**: `grid[i][j]` — O(V²) space, O(1) edge lookup
- [ ] Directed vs undirected; weighted vs unweighted

### Graph DFS
- [ ] Use a `visited` set to avoid infinite loops in cyclic graphs
- [ ] Iterative: explicit stack; recursive: call stack
- [ ] Use for: connected components, cycle detection, path existence

### Graph BFS
- [ ] Use a queue; marks nodes visited *before* enqueuing (not after)
- [ ] Finds **shortest path** in unweighted graphs
- [ ] Useful for: level-by-level expansion (rotting oranges, walls and gates)

### Union-Find (Disjoint Set Union)
- [ ] Tracks connected components; supports `union(a, b)` and `find(a)`
- [ ] **Path compression**: flatten tree during `find` → near O(1) amortized
- [ ] **Union by rank**: attach smaller tree under larger → keeps height low

### Topological Sort
- [ ] Only for Directed Acyclic Graphs (DAGs)
- [ ] **Kahn's algorithm (BFS)**: start with nodes of in-degree 0; decrement neighbors
- [ ] **DFS-based**: add node to result *after* visiting all its descendants (post-order)
- [ ] Cycle detection: if topological order doesn't include all nodes → cycle exists

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Medium | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | `exercises/number-of-islands.py` |
| [ ] | Medium | [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | `exercises/max-area-of-island.py` |
| [ ] | Medium | [Clone Graph](https://leetcode.com/problems/clone-graph/) | `exercises/clone-graph.py` |
| [ ] | Medium | [Walls and Gates](https://leetcode.com/problems/walls-and-gates/) | `exercises/walls-and-gates.py` |
| [ ] | Medium | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | `exercises/rotting-oranges.py` |
| [ ] | Medium | [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | `exercises/pacific-atlantic-water-flow.py` |
| [ ] | Medium | [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | `exercises/surrounded-regions.py` |
| [ ] | Medium | [Course Schedule](https://leetcode.com/problems/course-schedule/) | `exercises/course-schedule.py` |
| [ ] | Medium | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | `exercises/course-schedule-ii.py` |
| [ ] | Medium | [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) | `exercises/graph-valid-tree.py` |
| [ ] | Medium | [Number of Connected Components in an Undirected Graph](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | `exercises/number-of-connected-components-in-an-undirected-graph.py` |
| [ ] | Medium | [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | `exercises/redundant-connection.py` |
| [ ] | Hard   | [Word Ladder](https://leetcode.com/problems/word-ladder/) | `exercises/word-ladder.py` |
