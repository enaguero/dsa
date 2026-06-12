# Graphs — Theory Notes

---

## 1. Definitions

A **graph** G = (V, E) consists of a set of vertices V and edges E ⊆ V × V.
- **Directed (digraph):** edges have direction (u → v ≠ v → u).
- **Undirected:** edges are unordered pairs {u, v}.
- **Weighted:** each edge has an associated cost `w(u, v)`.
- **Degree:** number of edges incident to a vertex. In-degree (directed), out-degree.

### Representations

| Representation | Space | Edge lookup | Neighbour iteration |
|----------------|-------|-------------|---------------------|
| Adjacency list | O(V+E) | O(degree) | O(degree) |
| Adjacency matrix | O(V²) | O(1) | O(V) |
| Edge list | O(E) | O(E) | O(E) |

**When to use adjacency matrix:** dense graphs (E ≈ V²), need O(1) edge existence check.
**When to use adjacency list:** sparse graphs (E << V²), need to iterate neighbours efficiently.

---

## 2. BFS — O(V + E)

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**Complexity proof:** Each vertex enqueued at most once (guarded by `visited`): O(V) enqueue ops. Each edge examined at most twice (once from each endpoint in undirected, once in directed): O(E) total edge checks. Total: **O(V + E)**. ✓

**Key property:** BFS visits nodes in non-decreasing order of shortest-path distance from `start` (in unweighted graphs).

---

## 3. DFS — O(V + E)

```python
def dfs(graph, start, visited=None):
    if visited is None: visited = set()
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

Same argument as BFS: each vertex and edge processed at most once. **O(V + E)**. ✓

**Space:** O(V) for visited set + O(V) recursion stack in the worst case (path graph). Iterative DFS avoids stack overflow.

---

## 4. Topological Sort

Only defined for **DAGs** (Directed Acyclic Graphs).

### Kahn's Algorithm (BFS-based)
1. Compute in-degrees for all vertices.
2. Initialise queue with all vertices of in-degree 0.
3. While queue non-empty: pop vertex, append to result, decrement neighbours' in-degrees; enqueue any that reach 0.
4. If `len(result) < V` → cycle detected (some vertices never reached in-degree 0).

**Complexity:** O(V + E) — each vertex and edge processed once.

### DFS-based
Post-order DFS: append vertex to result stack **after** all its descendants are visited. Reverse the stack.

**Why post-order gives topological order:** In a DAG, if there is an edge u→v, then `v` finishes DFS before `u`. So `v` appears before `u` in the stack, and after reversal `u` appears before `v`. ✓

---

## 5. Union-Find (Disjoint Set Union)

Tracks connected components. Supports two operations:
- `find(x)`: return the representative of x's component.
- `union(x, y)`: merge the components of x and y.

### Implementation with Path Compression + Union by Rank

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
        return True
```

**Path compression:** During `find`, make every visited node point directly to the root → future finds are O(1).

**Union by rank:** Always attach the smaller-rank tree under the larger → tree height stays O(log n).

**Combined amortized complexity:** O(α(n)) per operation, where α is the **inverse Ackermann function** — effectively O(1) for all practical n (α(n) ≤ 4 for n < 10^600). ✓

---

## 6. Cycle Detection

| Graph type | Method | Complexity |
|------------|--------|------------|
| Undirected | DFS with parent tracking | O(V+E) |
| Undirected | Union-Find | O(E · α(V)) |
| Directed | DFS with 3-colour marking (white/grey/black) | O(V+E) |
| Directed | Topological sort (Kahn's) | O(V+E) |

**DFS cycle detection (directed):** A back-edge (edge to a grey/in-progress node) indicates a cycle.

---

## 7. Multi-Source BFS

Instead of starting from one node, initialise the queue with all source nodes. All sources are at distance 0; their neighbours at distance 1, and so on. Used for: Rotting Oranges, Walls and Gates (01-matrix distance).

---

## 8. Pitfalls
- **Visited set:** mark a node visited **before** enqueuing (BFS) or before recursing (DFS) to avoid processing the same node twice.
- **Disconnected graphs:** if not all nodes are reachable from the start, iterate over all nodes and call BFS/DFS on unvisited ones.
- **Directed vs undirected:** in directed graphs, edge u→v doesn't mean there's an edge v→u. Build your adjacency list accordingly.
