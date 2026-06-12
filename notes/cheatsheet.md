# DSA Cheatsheet

---

## 1. Big O Notation

### Formal Definition

`f(n) = O(g(n))` iff ∃ constants `c > 0` and `n_0 >= 1` such that `f(n) ≤ c·g(n)` for all `n >= n_0`.

| Notation | Name                    | Meaning                            |
| -------- | ----------------------- | ---------------------------------- |
| `O(g)`   | Big-O (upper bound)     | f grows **at most** as fast as g   |
| `Ω(g)`   | Omega (lower bound)     | f grows **at least** as fast as g  |
| `Θ(g)`   | Theta (tight bound)     | f grows **exactly** as fast as g   |
| `o(g)`   | Little-o (strict upper) | f grows **strictly slower** than g |

### Growth Rate Hierarchy (slowest → fastest)

```
O(1) < O(log log n) < O(log n) < O(√n) < O(n) < O(n log n)
     < O(n²) < O(n³) < O(2ⁿ) < O(n!) < O(nⁿ)
```

### Common Complexities at n = 10⁶

| Complexity | Operations (approx) | Feasible?   |
| ---------- | ------------------- | ----------- |
| O(1)       | 1                   | Yes         |
| O(log n)   | ~20                 | Yes         |
| O(√n)      | ~1,000              | Yes         |
| O(n)       | 1,000,000           | Yes         |
| O(n log n) | ~20,000,000         | Yes (tight) |
| O(n²)      | 10¹²                | No          |
| O(2ⁿ)      | 2^1,000,000         | No          |

### Logarithm Rules (important for complexity)

```
log(a·b)   = log a + log b
log(a/b)   = log a − log b
log(aᵏ)   = k · log a
log_a(n)   = log(n) / log(a)     ← change of base
log(n!)   = Θ(n log n)           ← Stirling's approximation
```

### Master Theorem

For `T(n) = a·T(n/b) + f(n)` where `a ≥ 1`, `b > 1`:

| Case | Condition                                                 | Result                                      |
| ---- | --------------------------------------------------------- | ------------------------------------------- |
| 1    | $f(n) = O(n^{\log_b(a) - \varepsilon})$                   | $T(n) = \Theta(n^{\log_b(a)})$              |
| 2    | $f(n) = \Theta(n^{\log_b(a)})$                            | $T(n) = \Theta(n^{\log_b(a)} \cdot \log n)$ |
| 3    | $f(n) = \Omega(n^{\log_b(a) + \varepsilon})$ + regularity | $T(n) = \Theta(f(n))$                       |

**Common recurrences:**

| Recurrence              | Example          | Result       |
| ----------------------- | ---------------- | ------------ |
| `T(n) = T(n/2) + O(1)`  | Binary search    | `O(log n)`   |
| `T(n) = T(n/2) + O(n)`  | Quick-select avg | `O(n)`       |
| `T(n) = 2T(n/2) + O(n)` | Merge sort       | `O(n log n)` |
| `T(n) = 2T(n/2) + O(1)` | Tree traversal   | `O(n)`       |
| `T(n) = T(n−1) + O(n)`  | Insertion sort   | `O(n²)`      |
| `T(n) = 2T(n−1) + O(1)` | Naive Fibonacci  | `O(2ⁿ)`      |

---

## 2. Data Structures — Operation Complexity

### Linear Structures

| Structure          | Access | Search | Insert (any)   | Delete (any)    | Space |
| ------------------ | ------ | ------ | -------------- | --------------- | ----- |
| Array (static)     | O(1)   | O(n)   | O(n)           | O(n)            | O(n)  |
| Dynamic Array      | O(1)   | O(n)   | O(1)\* amort.  | O(n)            | O(n)  |
| Singly Linked List | O(n)   | O(n)   | O(1) head      | O(n)            | O(n)  |
| Doubly Linked List | O(n)   | O(n)   | O(1) head/tail | O(1) known node | O(n)  |
| Stack (array)      | O(n)   | O(n)   | O(1) top       | O(1) top        | O(n)  |
| Queue (array)      | O(n)   | O(n)   | O(1) tail      | O(1) head       | O(n)  |
| Deque              | O(n)   | O(n)   | O(1) ends      | O(1) ends       | O(n)  |

\*Dynamic array insert at end: O(1) amortized, O(n) worst case (resize).

### Hash-Based Structures

| Structure | Search   | Insert   | Delete   | Space | Notes                         |
| --------- | -------- | -------- | -------- | ----- | ----------------------------- |
| Hash Map  | O(1) avg | O(1) avg | O(1) avg | O(n)  | O(n) worst (all keys collide) |
| Hash Set  | O(1) avg | O(1) avg | O(1) avg | O(n)  | Same caveat                   |

### Tree Structures

| Structure        | Search   | Insert   | Delete   | Space    | Notes                        |
| ---------------- | -------- | -------- | -------- | -------- | ---------------------------- |
| BST (balanced)   | O(log n) | O(log n) | O(log n) | O(n)     | AVL, Red-Black               |
| BST (unbalanced) | O(n)     | O(n)     | O(n)     | O(n)     | Worst case: sorted input     |
| Heap (binary)    | O(n)     | O(log n) | O(log n) | O(n)     | Find-min/max: O(1)           |
| Trie             | O(m)     | O(m)     | O(m)     | O(Σ·m·n) | m = key length, Σ = alphabet |
| Segment Tree     | O(log n) | O(log n) | O(log n) | O(n)     | Range queries                |

---

## 3. Sorting Algorithms

| Algorithm      | Best       | Average    | Worst      | Space    | Stable? | Notes                   |
| -------------- | ---------- | ---------- | ---------- | -------- | ------- | ----------------------- |
| Bubble Sort    | O(n)       | O(n²)      | O(n²)      | O(1)     | Y       | Adaptive                |
| Selection Sort | O(n²)      | O(n²)      | O(n²)      | O(1)     | N       |                         |
| Insertion Sort | O(n)       | O(n²)      | O(n²)      | O(1)     | Y       | Good for nearly sorted  |
| Merge Sort     | O(n log n) | O(n log n) | O(n log n) | O(n)     | Y       | Divide & conquer        |
| Quick Sort     | O(n log n) | O(n log n) | O(n²)      | O(log n) | N       | Worst on sorted/reverse |
| Heap Sort      | O(n log n) | O(n log n) | O(n log n) | O(1)     | N       | In-place                |
| Counting Sort  | O(n+k)     | O(n+k)     | O(n+k)     | O(k)     | Y       | k = value range         |
| Radix Sort     | O(d·n)     | O(d·n)     | O(d·n)     | O(n+k)   | Y       | d = digits              |
| Tim Sort       | O(n)       | O(n log n) | O(n log n) | O(n)     | Y       | Python's `sorted()`     |

---

## 4. Graph Algorithms

| Algorithm                 | Time           | Space | Use Case                                         |
| ------------------------- | -------------- | ----- | ------------------------------------------------ |
| BFS                       | O(V+E)         | O(V)  | Shortest path (unweighted), level order          |
| DFS                       | O(V+E)         | O(V)  | Connected components, cycle detection, topo sort |
| Topological Sort (Kahn's) | O(V+E)         | O(V)  | DAG ordering                                     |
| Dijkstra (binary heap)    | O((V+E) log V) | O(V)  | Shortest path, non-negative weights              |
| Bellman-Ford              | O(VE)          | O(V)  | Shortest path, negative weights                  |
| Floyd-Warshall            | O(V³)          | O(V²) | All-pairs shortest path                          |
| Kruskal's MST             | O(E log E)     | O(V)  | Minimum spanning tree                            |
| Prim's MST (heap)         | O((V+E) log V) | O(V)  | Minimum spanning tree                            |
| Union-Find                | O(α(n)) amort. | O(V)  | Connected components, MST                        |

### When to use which shortest-path algorithm:

```
No weights / BFS weights=1      → BFS                    O(V+E)
Non-negative weights            → Dijkstra               O((V+E) log V)
Negative weights, no neg cycle  → Bellman-Ford           O(VE)
All-pairs, dense graph          → Floyd-Warshall         O(V³)
```

---

## 5. Dynamic Programming Patterns

| Pattern              | State Size | Example                      |
| -------------------- | ---------- | ---------------------------- |
| Linear sequence      | O(n)       | Fibonacci, climbing stairs   |
| Two-sequence         | O(m·n)     | LCS, edit distance           |
| Grid                 | O(m·n)     | Unique paths, min path sum   |
| Interval             | O(n²)      | Burst balloons, matrix chain |
| Knapsack (0/1)       | O(n·W)     | Partition equal subset       |
| Knapsack (unbounded) | O(n·W)     | Coin change                  |
| Bitmask DP           | O(2ⁿ·n)    | TSP, covering subsets        |
| Tree DP              | O(n)       | House robber on tree         |

---

## 6. Recursion & Backtracking

| Problem Type        | Time Complexity | Space (call stack) |
| ------------------- | --------------- | ------------------ |
| Subsets             | O(2ⁿ)           | O(n)               |
| Permutations        | O(n!)           | O(n)               |
| Combinations C(n,k) | O(C(n,k)·k)     | O(k)               |
| N-Queens            | O(n!)           | O(n)               |

---

## 7. Bit Manipulation Quick Reference

| Operation              | Expression                   | Notes           |
| ---------------------- | ---------------------------- | --------------- |
| Check bit k            | `(n >> k) & 1`               | Returns 0 or 1  |
| Set bit k              | `n \| (1 << k)`              |                 |
| Clear bit k            | `n & ~(1 << k)`              |                 |
| Toggle bit k           | `n ^ (1 << k)`               |                 |
| Clear lowest set bit   | `n & (n - 1)`                | Kernighan trick |
| Isolate lowest set bit | `n & (-n)`                   |                 |
| Check power of 2       | `n > 0 and (n & (n-1)) == 0` |                 |
| Count set bits         | loop `n &= n-1`              | O(popcount)     |
| XOR swap               | `a ^= b; b ^= a; a ^= b`     | No temp var     |

### Two's Complement

- Negate: flip all bits, add 1 → `-n = ~n + 1`
- Range for k-bit signed: `[-2^(k-1), 2^(k-1) - 1]`
- Python: arbitrary precision, use `n & 0xFFFFFFFF` to simulate 32-bit

---

## 8. Complexity Quick Reference Card

```
Technique          | Time         | Space
-------------------|--------------|--------
Array scan         | O(n)         | O(1)
Binary search      | O(log n)     | O(1)
Two pointers       | O(n)         | O(1)
Sliding window     | O(n)         | O(1)–O(k)
Hash map/set       | O(n) build   | O(n)
Sorting            | O(n log n)   | O(1)–O(n)
BFS / DFS          | O(V+E)       | O(V)
Heap push/pop      | O(log n)     | O(n)
DP (1-D)           | O(n)         | O(n) or O(1)
DP (2-D)           | O(m·n)       | O(m·n) or O(n)
Backtracking       | O(b^d)       | O(d)
```

`b` = branching factor, `d` = depth of search tree
