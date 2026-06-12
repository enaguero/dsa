# Advanced Graphs — Theory Notes

---

## 1. Shortest Path Algorithms

### Dijkstra's Algorithm

**Problem:** Single-source shortest path (SSSP) in a weighted graph with **non-negative** edge weights.

**Algorithm:**
```python
import heapq

def dijkstra(graph, src):
    dist = {node: float('inf') for node in graph}
    dist[src] = 0
    heap = [(0, src)]   # (distance, node)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue   # stale entry
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist
```

**Complexity:** O((V + E) log V) with a binary heap.

**Correctness (greedy invariant):** Dijkstra maintains: *when a node u is popped from the heap, `dist[u]` is the true shortest distance.*

*Proof by induction:* Base case: `dist[src] = 0` is correct. Inductive step: Assume all previously popped nodes have correct distances. When u is popped with distance d, any alternative path to u must go through some not-yet-popped node x, which has `dist[x] ≥ d` (since the heap always pops the minimum, and all weights are non-negative). So the alternative path is no shorter. ✓

**Why non-negative weights required:** Negative weights can make a path look longer through the heap but be shorter in reality after relaxation — the invariant breaks.

---

### Bellman-Ford

**Problem:** SSSP allowing **negative** edge weights; detects negative cycles.

```python
def bellman_ford(n, edges, src):
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(n - 1):       # relax all edges V-1 times
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # Check for negative cycles
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None   # negative cycle reachable
    return dist
```

**Why V−1 iterations suffice:**

A shortest path in a graph with V nodes and no negative cycles has at most V−1 edges (otherwise it revisits a node → we can remove the loop). After `k` relaxation passes, `dist[v]` is the correct shortest distance using at most `k` edges. After V−1 passes, all paths of V−1 edges are correct → all shortest paths found. ✓

**Complexity:** O(VE). Space: O(V).

**Detecting negative cycles:** If any distance improves in the V-th pass, a negative cycle is reachable. ✓

---

### Floyd-Warshall

**Problem:** All-pairs shortest paths (APSP).

```python
def floyd_warshall(n, adj):
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n): dist[i][i] = 0
    for u, v, w in adj: dist[u][v] = w

    for k in range(n):           # intermediate vertex
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist
```

**Why it works:** `dist[i][j]` after considering intermediates `{0, …, k}` equals the shortest path from i to j using only `{0, …, k}` as intermediates. The recurrence `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])` correctly extends to include `k` as a potential intermediate. ✓

**Complexity:** O(V³) time, O(V²) space.

---

## 2. Minimum Spanning Tree (MST)

**Definition:** A spanning tree of a connected graph G = (V, E) is a subgraph that is a tree and includes every vertex. An MST is the spanning tree with minimum total edge weight.

**Cut Property (foundation of both algorithms):**
For any cut (S, V−S) of the graph, the minimum-weight edge crossing the cut is in **some** MST.

---

### Kruskal's Algorithm

Sort edges by weight. Greedily add the lightest edge that doesn't form a cycle (use Union-Find).

```python
def kruskal(n, edges):
    edges.sort(key=lambda e: e[2])  # sort by weight
    uf = UnionFind(n)
    mst_cost, mst_edges = 0, []
    for u, v, w in edges:
        if uf.union(u, v):
            mst_cost += w
            mst_edges.append((u, v, w))
    return mst_cost, mst_edges
```

**Complexity:** O(E log E) for sorting + O(E · α(V)) for Union-Find = **O(E log E)**. ✓

**Correctness:** Each added edge is the minimum crossing some cut (by the cut property). ✓

---

### Prim's Algorithm

Grow the MST from a start node using a min-heap of (weight, neighbor).

```python
def prim(graph, start):
    visited = set()
    heap = [(0, start)]
    total = 0
    while heap:
        cost, u = heapq.heappop(heap)
        if u in visited: continue
        visited.add(u)
        total += cost
        for v, w in graph[u]:
            if v not in visited:
                heapq.heappush(heap, (w, v))
    return total
```

**Complexity:** O((V + E) log V) with a binary heap. **O(E log V)** for connected graphs.

---

## 3. Eulerian Path (Hierholzer's Algorithm)

**Eulerian circuit:** A path that visits every **edge** exactly once and returns to the start.

**Existence conditions:**
- Undirected: every vertex has even degree.
- Directed: every vertex has `in-degree = out-degree`.

**Algorithm (Hierholzer):** DFS on edges, push a vertex to result **after** all its edges are explored (post-order on edges). This is O(V + E).

---

## 4. Algorithm Selection Guide

```
Single-source, non-negative weights  → Dijkstra   O((V+E) log V)
Single-source, negative weights      → Bellman-Ford  O(VE)
All-pairs, dense graph               → Floyd-Warshall O(V³)
MST (sparse)                         → Kruskal     O(E log E)
MST (dense)                          → Prim        O(E log V)
Every edge exactly once              → Hierholzer  O(V+E)
```

---

## 5. Pitfalls
- **Dijkstra with negative weights:** incorrect — use Bellman-Ford.
- **Stale entries in Dijkstra:** when a node is popped with `d > dist[node]`, skip it (the shorter path was already processed).
- **MST vs shortest path tree:** they are different. MST minimises total edge weight; shortest path tree minimises distance from a source.
- **Kruskal on disconnected graphs:** the result is a minimum spanning **forest**.
