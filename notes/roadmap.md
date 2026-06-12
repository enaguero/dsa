# DSA Roadmap

Following the NeetCode 150 dependency order. Each topic lists the theoretical concepts to study before tackling the practice problems.

---

## Phase 1 — Foundation

### 1. Arrays & Hashing
**Theory**
- [ ] Static vs dynamic arrays, memory layout, cache locality
- [ ] Hash functions: how they work, collision strategies (chaining, open addressing)
- [ ] Hash maps and hash sets: average O(1) insert/lookup, worst-case O(n)
- [ ] Amortized analysis (dynamic array resizing)

**Practice** → `neetcode/neetcode_150/01_arrays_and_hashing/`

---

## Phase 2 — Core Techniques

### 2. Two Pointers
**Theory**
- [ ] Opposite-end vs same-direction pointers
- [ ] When to apply: sorted arrays, palindromes, pair-sum problems
- [ ] Why it reduces O(n²) brute force to O(n)

**Practice** → `neetcode/neetcode_150/02_two_pointers/`

### 3. Stack
**Theory**
- [ ] LIFO principle, stack operations (push/pop/peek) in O(1)
- [ ] Monotonic stack: increasing vs decreasing, when to use
- [ ] Applications: balanced parentheses, next greater element, expression evaluation

**Practice** → `neetcode/neetcode_150/04_stack/`

---

## Phase 3 — Search & Windows

### 4. Binary Search
**Theory**
- [ ] Classic binary search and loop invariants
- [ ] Left-boundary and right-boundary variants
- [ ] Searching on the answer space (not just sorted arrays)
- [ ] O(log n) complexity proof

**Practice** → `neetcode/neetcode_150/05_binary_search/`

### 5. Sliding Window
**Theory**
- [ ] Fixed-size vs variable-size windows
- [ ] Expand/shrink pattern with two pointers
- [ ] Maintaining window state efficiently (frequency maps, running sums)

**Practice** → `neetcode/neetcode_150/03_sliding_window/`

### 6. Linked List
**Theory**
- [ ] Singly vs doubly linked list, node structure
- [ ] Fast & slow pointer (Floyd's cycle detection)
- [ ] In-place reversal pattern
- [ ] Sentinel/dummy head nodes

**Practice** → `neetcode/neetcode_150/06_linked_list/`

---

## Phase 4 — Trees

### 7. Trees
**Theory**
- [ ] Binary tree properties (height, depth, balance)
- [ ] Binary Search Tree (BST): insert, delete, search
- [ ] DFS traversals: inorder, preorder, postorder (recursive & iterative)
- [ ] BFS / level-order traversal with a queue
- [ ] Lowest Common Ancestor (LCA)

**Practice** → `neetcode/neetcode_150/07_trees/`

---

## Phase 5 — Tree Extensions

### 8. Tries
**Theory**
- [ ] Prefix tree structure (nodes with children map + end-of-word flag)
- [ ] Insert / search / startsWith in O(n) where n = word length
- [ ] Use cases: autocomplete, prefix matching, word dictionary

**Practice** → `neetcode/neetcode_150/08_tries/`

### 9. Backtracking
**Theory**
- [ ] Decision tree model: choices, constraints, goals
- [ ] Pruning: how and when to cut branches early
- [ ] Templates for: subsets, permutations, combinations, board problems
- [ ] Time complexity analysis (worst-case exponential)

**Practice** → `neetcode/neetcode_150/10_backtracking/`

---

## Phase 6 — Heap & Priority Queue

### 10. Heap / Priority Queue
**Theory**
- [ ] Binary heap: min-heap and max-heap properties
- [ ] Heapify up / heapify down operations
- [ ] O(log n) push/pop, O(1) peek, O(n) heapify (build from array)
- [ ] K-th largest/smallest pattern
- [ ] Two-heap pattern for median problems

**Practice** → `neetcode/neetcode_150/09_heap_priority_queue/`

---

## Phase 7 — Graphs & DP

### 11. Graphs
**Theory**
- [ ] Representations: adjacency list vs adjacency matrix
- [ ] DFS and BFS on graphs (handling visited set)
- [ ] Connected components, cycle detection
- [ ] Topological sort: DFS-based (post-order) and Kahn's algorithm (BFS)
- [ ] Union-Find (Disjoint Set Union): path compression + union by rank

**Practice** → `neetcode/neetcode_150/11_graphs/`

### 12. 1-D Dynamic Programming
**Theory**
- [ ] Overlapping subproblems and optimal substructure
- [ ] Top-down (memoization) vs bottom-up (tabulation)
- [ ] State definition and recurrence relation derivation
- [ ] Common patterns: Fibonacci, house robber, coin change, LIS

**Practice** → `neetcode/neetcode_150/13_1d_dynamic_programming/`

---

## Phase 8 — Advanced

### 13. Intervals
**Theory**
- [ ] Sorting intervals by start time
- [ ] Merge overlapping intervals
- [ ] Sweep line technique

**Practice** → `neetcode/neetcode_150/16_intervals/`

### 14. Greedy
**Theory**
- [ ] Greedy choice property: local optimum → global optimum
- [ ] Proving correctness (exchange argument)
- [ ] Common greedy patterns: interval scheduling, jump game, gas station

**Practice** → `neetcode/neetcode_150/15_greedy/`

### 15. Advanced Graphs
**Theory**
- [ ] Dijkstra's algorithm: single-source shortest path (non-negative weights)
- [ ] Bellman-Ford: handles negative weights, detects negative cycles
- [ ] Floyd-Warshall: all-pairs shortest paths
- [ ] Minimum Spanning Tree: Kruskal's (Union-Find) and Prim's (heap)
- [ ] Strongly connected components: Tarjan's or Kosaraju's

**Practice** → `neetcode/neetcode_150/12_advanced_graphs/`

### 16. 2-D Dynamic Programming
**Theory**
- [ ] Grid DP: path counting, min-cost paths
- [ ] String DP: longest common subsequence (LCS), edit distance
- [ ] State compression for 2-D → 1-D optimization
- [ ] Recognizing when a 2-D state space is needed

**Practice** → `neetcode/neetcode_150/14_2d_dynamic_programming/`

### 17. Bit Manipulation
**Theory**
- [ ] Binary representation: two's complement, signed vs unsigned
- [ ] Bitwise operators: AND, OR, XOR, NOT, left/right shift
- [ ] Common tricks: check/set/clear bit, isolate lowest set bit (`n & -n`), XOR for duplicate detection
- [ ] Bit masks for subset enumeration

**Practice** → `neetcode/neetcode_150/18_bit_manipulation/`

### 18. Math & Geometry
**Theory**
- [ ] Modular arithmetic: `(a + b) % m`, `(a * b) % m`, overflow prevention
- [ ] GCD (Euclidean algorithm) and LCM
- [ ] Prime sieves (Sieve of Eratosthenes)
- [ ] Fast exponentiation (binary exponentiation)
- [ ] 2-D geometry basics: area of polygons, point-in-polygon, rotation

**Practice** → `neetcode/neetcode_150/17_math_and_geometry/`

---

## Dependency Order (Quick Reference)

```
Arrays & Hashing
├── Two Pointers
│   ├── Binary Search
│   │   └── Trees ──────────────────────┐
│   └── Sliding Window                  │
└── Stack                               │
    └── Linked List ────────────────────┘
                                        Trees
                            ┌───────────┼───────────┐
                          Tries    (center)     Backtracking
                            │           │        ┌──┴──────┐
                     Heap/Priority    (feeds)  Graphs    1-D DP
                          Queue         │      ┌──┴──┐   ┌──┴──────┐
                        ┌──┴──┐     Adv.Graphs 2-D DP  Bit Manip.
                    Intervals Greedy             │
                                              Math & Geometry
```
