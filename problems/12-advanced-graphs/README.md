# Advanced Graphs

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Shortest Path Algorithms
- [ ] **Dijkstra's**: single-source, non-negative weights; min-heap of (cost, node); O((V+E) log V)
- [ ] **Bellman-Ford**: handles negative weights; relax all edges V-1 times; O(VE)
  - Extra iteration detects negative cycles
- [ ] **Floyd-Warshall**: all-pairs shortest paths; O(V³); `dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])`

### Minimum Spanning Tree (MST)
- [ ] **Kruskal's**: sort edges by weight, add edge if it connects two different components (Union-Find); O(E log E)
- [ ] **Prim's**: grow MST from a start node using a min-heap of (weight, neighbor); O((V+E) log V)

### Eulerian Path / Circuit
- [ ] Eulerian circuit: every node has even degree (undirected) or in-degree = out-degree (directed)
- [ ] Hierholzer's algorithm: DFS, push to result *after* backtracking (post-order on edges)

### Strongly Connected Components (SCC)
- [ ] **Kosaraju's**: two DFS passes — first on original graph (record finish order), second on reversed graph
- [ ] **Tarjan's**: single DFS with a stack; uses low-link values

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Medium | [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) | `exercises/min-cost-to-connect-all-points.py` |
| [ ] | Medium | [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | `exercises/network-delay-time.py` |
| [ ] | Medium | [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | `exercises/cheapest-flights-within-k-stops.py` |
| [ ] | Hard   | [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) | `exercises/reconstruct-itinerary.py` |
| [ ] | Hard   | [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) | `exercises/swim-in-rising-water.py` |
| [ ] | Hard   | [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | `exercises/alien-dictionary.py` |
