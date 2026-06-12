---
title: "RAM Model & Asymptotic Analysis"
subtitle: "Part IV — Practical Catalog"
author: "Erwin Aguero"
date: "\\today"
theme: metropolis
colortheme: metropolis
fonttheme: professionalfonts
aspectratio: 169
fontsize: 11pt
mainfont: "TeX Gyre Pagella"
mathfont: "TeX Gyre Pagella Math"
monofont: "Menlo"
header-includes: |
  \usepackage{amsmath, amssymb, mathtools}
  \usepackage{microtype}
  \metroset{numbering=fraction, progressbar=foot, block=fill}
---

## 23. Search Algorithms

### 23.1 Linear search

```text
for i = 0 to n-1:
    if A[i] == target: return i
return -1
```

\vspace{0.5em}

- Worst case: $\Theta(n)$. Best case: $\Theta(1)$.
- No assumption on input — works on unsorted arrays.

\vspace{0.5em}

The prototype for any "scan and check" algorithm.

### 23.2 Binary search

```text
lo = 0; hi = n − 1
while lo ≤ hi:
    mid = (lo + hi) / 2
    if A[mid] == target: return mid
    elif A[mid] < target: lo = mid + 1
    else:                 hi = mid − 1
return -1
```

\vspace{0.4em}

Search interval halves each step. Recurrence:
$$T(n) = T(n/2) + \Theta(1)$$

Master Theorem ($a=1, b=2, c^*=0$, Case 2): $\boxed{T(n) = \Theta(\log n)}$.

### 23.3 Hash-table lookup

| Case | Cost |
|---|---|
| **Average** (good hash, load factor $O(1)$) | $\Theta(1)$ |
| **Worst** (chained, all keys collide) | $\Theta(n)$ |

\vspace{0.5em}

Two assumptions buy the average-case bound:

1. A hash function that distributes keys uniformly.
2. A bounded load factor (resize when full).

\vspace{0.4em}

Both are practical conditions, not theorems.

## 24. Sorting Algorithms

### The big table

\small

| Algorithm | Worst | Average | Best | Space | Stable |
|---|---|---|---|---|---|
| Insertion | $\Theta(n^2)$ | $\Theta(n^2)$ | $\Theta(n)$ | $\Theta(1)$ | yes |
| Selection | $\Theta(n^2)$ | $\Theta(n^2)$ | $\Theta(n^2)$ | $\Theta(1)$ | no |
| Bubble    | $\Theta(n^2)$ | $\Theta(n^2)$ | $\Theta(n)$ | $\Theta(1)$ | yes |
| Mergesort | $\Theta(n\log n)$ | $\Theta(n\log n)$ | $\Theta(n\log n)$ | $\Theta(n)$ | yes |
| Heapsort  | $\Theta(n\log n)$ | $\Theta(n\log n)$ | $\Theta(n\log n)$ | $\Theta(1)$ | no |
| Quicksort | $\Theta(n^2)$ | $\Theta(n\log n)$ | $\Theta(n\log n)$ | $\Theta(\log n)$ exp. | no |
| Counting  | $\Theta(n+k)$ | $\Theta(n+k)$ | $\Theta(n+k)$ | $\Theta(n+k)$ | yes |
| Radix     | $\Theta(d(n+k))$ | $\Theta(d(n+k))$ | $\Theta(d(n+k))$ | $\Theta(n+k)$ | yes |

\normalsize
\vspace{0.4em}

Counting and radix beat $n\log n$ by **not being comparison-based.**

### 24.1 Why comparison sorting is $\Omega(n \log n)$

A comparison sort decides between $n!$ permutations using only $a < b$ tests. Each comparison reveals **one bit**. To distinguish $n!$ outcomes:

$$\log_2(n!) \;=\; \Theta(n \log n) \text{ bits}$$

\vspace{0.4em}

**Decision tree view:** any comparison sort is a binary tree with $\ge n!$ leaves.

A binary tree with $L$ leaves has depth $\ge \lceil \log_2 L \rceil$.

\vspace{0.5em}

\begin{block}{Lower bound (information-theoretic)}
Worst-case comparisons $\ge \lceil \log_2(n!) \rceil = \Theta(n \log n)$ — for \emph{any} comparison-based sort.
\end{block}

### 24.2 Insertion sort

```text
for i = 1 to n−1:
    j = i
    while j > 0 and A[j−1] > A[j]:
        swap A[j−1], A[j]
        j = j − 1
```

\vspace{0.4em}

Inner loop runs 0 to $i$ times depending on input.

\vspace{0.5em}

| Input | Inner-loop cost | Total |
|---|---|---|
| Reverse-sorted | $i$ each | $\sum_{i=1}^{n-1} i = \Theta(n^2)$ |
| Already sorted | $0$ each | $\Theta(n)$ |
| Random | $\sim i/2$ on avg | $\Theta(n^2)$ |

### 24.3 Mergesort

```text
mergesort(A):
    if |A| ≤ 1: return A
    L = mergesort(A[0..n/2])
    R = mergesort(A[n/2..n])
    return merge(L, R)
```

\vspace{0.4em}

`merge` is $\Theta(n)$.

$$T(n) = 2 T(n/2) + \Theta(n)$$

\vspace{0.4em}

Master Theorem, Case 2: $\boxed{\Theta(n \log n)}$.

Space: $\Theta(n)$ for merge scratch.

### 24.4 Quicksort

```text
quicksort(A, lo, hi):
    if lo < hi:
        p = partition(A, lo, hi)
        quicksort(A, lo, p−1)
        quicksort(A, p+1, hi)
```

\vspace{0.5em}

| Case | Recurrence | Solution |
|---|---|---|
| Best (balanced) | $T(n) = 2T(n/2) + \Theta(n)$ | $\Theta(n \log n)$ |
| Worst (sorted in, first pivot) | $T(n) = T(n-1) + \Theta(n)$ | $\Theta(n^2)$ |
| Average (random pivot) | indicator-variable analysis | $\Theta(n \log n)$ |

\vspace{0.5em}

\textbf{Randomized quicksort:} expected $\Theta(n \log n)$ on \emph{every} input — bound over coin flips, not input distribution.

### 24.5 Heapsort

Build a max-heap ($\Theta(n)$), extract-max $n$ times ($\Theta(\log n)$ each).

$$\Theta(n) + \Theta(n \log n) \;=\; \Theta(n \log n)$$

\vspace{0.5em}

The non-obvious bit: \textbf{build-heap is $\Theta(n)$, not $\Theta(n \log n)$.}

Naive bound: $n$ sift-downs $\times O(\log n)$ each $= O(n \log n)$ — loose.

\vspace{0.4em}

Better: most nodes are near the leaves, where sift-down is cheap.

### 24.5 Why build-heap is $\Theta(n)$

At depth $d$ from the root: at most $n / 2^{d+1}$ nodes; sift-down does at most $h - d$ swaps.

\vspace{0.4em}

Total work:
$$\sum_{d=0}^{h} \frac{n}{2^{d+1}} (h - d) \;=\; \frac{n}{2} \sum_{j=0}^{h} \frac{j}{2^{h-j}} \;\le\; n \sum_{j=0}^{\infty} \frac{j}{2^{j}} \;=\; 2n$$

\vspace{0.4em}

(Using $\sum_{j \ge 0} j/2^j = 2$.)

\vspace{0.4em}

\begin{block}{The key point}
Nodes at depth $d$ are \textbf{exponentially numerous} in $d$ but cost only \textbf{linear} in $h-d$. The exponential beats the linear; the $h$ cancels.

$\Rightarrow \boxed{\Theta(n)}$.
\end{block}

## 25. Graph Algorithms

### 25.1 BFS / DFS — $\Theta(n + m)$

With an adjacency-list representation:

- Each vertex is enqueued / pushed once: $\Theta(n)$.
- Each edge is examined twice (undirected) or once (directed): $\Theta(m)$.

\vspace{0.5em}

Total: $\Theta(n + m)$.

\vspace{0.5em}

\begin{alertblock}{The handshake argument}
Summing $\deg(v)$ over all $v$ gives $2m$ in undirected graphs. Loop bodies that "do constant work per neighbor" cost $\Theta(m)$ in total, not $\Theta(nm)$.
\end{alertblock}

### 25.2 Dijkstra — non-negative weights

Single-source shortest paths.

\vspace{0.4em}

| Data structure | Cost |
|---|---|
| Binary heap | $\Theta((n + m) \log n)$ |
| Fibonacci heap | $\Theta(m + n \log n)$ |

\vspace{0.5em}

Fibonacci heap wins for **dense** graphs ($m = \omega(n)$) — fewer $\log n$ factors on the edge work.

\vspace{0.4em}

In practice, binary heap is faster: smaller constants and cache-friendlier.

### 25.3 Bellman–Ford — negative edges allowed

Single-source shortest paths with negative edges (no negative cycles).

$$\boxed{\Theta(n \cdot m)}$$

\vspace{0.5em}

Worth $n$ times more than Dijkstra. Buy it when:

- Edge weights can be negative.
- You need to detect negative cycles.

\vspace{0.5em}

Can be viewed as a DP over (vertex, hop count) — see §26.

### 25.4–25.6 The rest in one slide

\small

| Problem | Algorithm | Time |
|---|---|---|
| All-pairs shortest paths | Floyd–Warshall | $\Theta(n^3)$ |
| Minimum spanning tree | Kruskal | $\Theta(m \log n)$ |
| Minimum spanning tree | Prim (binary heap) | $\Theta((n+m) \log n)$ |
| Minimum spanning tree | Prim (Fibonacci heap) | $\Theta(m + n \log n)$ |
| Topological sort | DFS / Kahn | $\Theta(n + m)$ |

\vspace{0.4em}
\normalsize
Floyd–Warshall: three nested vertex loops. Concise, easy to remember, but $\Theta(n^3)$ — not for huge graphs.

## 26. Dynamic Programming

### The DP complexity formula

$$\boxed{\text{time} \;=\; (\#\text{ distinct subproblems}) \;\times\; (\text{work per subproblem})}$$

\vspace{0.4em}

Assuming each subproblem is solved **once** and stored.

\vspace{0.5em}

The whole template: identify the state space, bound the per-state work, multiply.

\vspace{0.5em}

The hard part is finding the **right** subproblem.

### 26.1 Fibonacci — three flavors

| Approach | Time | Space |
|---|---|---|
| Naive recursion | $\Theta(\varphi^n)$ | $\Theta(n)$ stack |
| Memoized | $\Theta(n)$ | $\Theta(n)$ |
| Bottom-up, two variables | $\Theta(n)$ | $\Theta(1)$ |

\vspace{0.5em}

Naive cost satisfies $T(n) = T(n-1) + T(n-2) + \Theta(1)$ — exact same recurrence as Fibonacci itself.

\vspace{0.4em}

Solution: $\Theta(\varphi^n)$ with $\varphi = (1 + \sqrt{5})/2 \approx 1.618$.

### 26.2 Longest Common Subsequence

\begin{block}{Recurrence}
$$\mathrm{LCS}[i][j] = \begin{cases}
0 & \text{if } i = 0 \text{ or } j = 0 \\
\mathrm{LCS}[i-1][j-1] + 1 & \text{if } x_i = y_j \\
\max(\mathrm{LCS}[i-1][j],\, \mathrm{LCS}[i][j-1]) & \text{otherwise}
\end{cases}$$
\end{block}

\vspace{0.4em}

- **Subproblems:** $(n+1)(m+1) = \Theta(nm)$.
- **Work each:** read 3 cells, one comparison/max — $\Theta(1)$.
- **Total:** $\boxed{\Theta(nm)}$.

\vspace{0.4em}

\small
Space: $\Theta(nm)$ for the table, but row $i$ only depends on row $i-1$ — compressible to $\Theta(\min(n, m))$ if you only need the **length**, not the sequence.

### 26.3 The DP catalog

| Problem | Subproblems | Work each | Total |
|---|---|---|---|
| Fibonacci (memoized) | $n$ | $O(1)$ | $\Theta(n)$ |
| LCS | $nm$ | $O(1)$ | $\Theta(nm)$ |
| Edit distance | $nm$ | $O(1)$ | $\Theta(nm)$ |
| Matrix-chain | $n^2$ | $O(n)$ | $\Theta(n^3)$ |
| 0/1 Knapsack | $nW$ | $O(1)$ | $\Theta(nW)$ |
| Bellman–Ford (as DP) | $n \cdot n$ | $\Theta(\deg v)$ | $\Theta(nm)$ |

\vspace{0.4em}

Every entry follows the same template — only the state space and per-state work change.

### 0/1 Knapsack — the pseudo-polynomial trap

$$\Theta(nW)$$

\vspace{0.4em}

Polynomial in $n$ and in the *value* $W$.

\vspace{0.4em}

But the **input size** includes $W$ in **binary** — bit length $\log W$. So $W$ can be exponential in the input size:

$$\Theta(nW) \;=\; \Theta(n \cdot 2^{\log W})$$

\vspace{0.5em}

This is why 0/1 knapsack remains **NP-hard** despite its "polynomial-looking" DP.

\vspace{0.4em}

The same trap fires for trial-division primality (Part III, §13).

## 27. Catalog of Recurrences

### The recurrences worth memorizing

\small

| Recurrence | Solution | Example |
|---|---|---|
| $T(n) = T(n-1) + \Theta(1)$ | $\Theta(n)$ | Linear scan |
| $T(n) = T(n-1) + \Theta(n)$ | $\Theta(n^2)$ | Selection sort |
| $T(n) = T(n/2) + \Theta(1)$ | $\Theta(\log n)$ | Binary search |
| $T(n) = T(\sqrt n) + \Theta(1)$ | $\Theta(\log \log n)$ | van Emde Boas |
| $T(n) = T(n/2) + \Theta(n)$ | $\Theta(n)$ | Linear selection |
| $T(n) = 2T(n/2) + \Theta(1)$ | $\Theta(n)$ | Tree traversal |
| $T(n) = 2T(n/2) + \Theta(n)$ | $\Theta(n \log n)$ | Mergesort |
| $T(n) = 2T(n/2) + \Theta(n^2)$ | $\Theta(n^2)$ | Root-dominated DAC |
| $T(n) = T(n/2) + T(n/4) + \Theta(n)$ | $\Theta(n)$ | Akra–Bazzi, $p<1$ |
| $T(n) = 2T(n-1) + \Theta(1)$ | $\Theta(2^n)$ | Tower of Hanoi |
| $T(n) = T(n-1) + T(n-2) + \Theta(1)$ | $\Theta(\varphi^n)$ | Naive Fibonacci |
| $T(n) = 7T(n/2) + \Theta(n^2)$ | $\Theta(n^{\log_2 7})$ | Strassen |

### Recap

\begin{itemize}
  \item Search: linear $\Theta(n)$, binary $\Theta(\log n)$, hash $\Theta(1)$ amortized.
  \item Sorting: $\Omega(n \log n)$ for comparison-based — broken only by exploiting key structure.
  \item Build-heap is $\Theta(n)$; the naive bound is loose.
  \item Graphs: BFS/DFS / topological / MST family all $\Theta(n + m)$ or $(n+m)\log n$.
  \item DP: $\text{time} = (\#\text{subproblems}) \times (\text{work per subproblem})$.
  \item Watch for pseudo-polynomial bounds (0/1 knapsack, Bellman–Ford on weights).
\end{itemize}

\vspace{0.4em}

Next: where the RAM model itself stops being adequate — \textbf{Part V, Beyond the Basic RAM.}
