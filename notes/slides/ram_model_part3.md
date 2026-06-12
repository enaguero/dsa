---
title: "RAM Model & Asymptotic Analysis"
subtitle: "Part III — The Mechanics of Algorithm Analysis"
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

## 12. Best, Worst, and Average Case

### Three measures of running time

For algorithm $A$ on input $x$, let $T_A(x)$ = number of steps.

\vspace{0.5em}

\begin{block}{Definitions}
\begin{align*}
T_{\mathrm{worst}}(n) &= \max\{T_A(x) : |x| = n\} \\
T_{\mathrm{best}}(n)  &= \min\{T_A(x) : |x| = n\} \\
T_{\mathrm{avg}}(n)   &= \mathbb{E}[T_A(x)] \text{ for } x \sim \mathcal{D}_n
\end{align*}
\end{block}

### Why worst case is the default

1. **Guarantee.** No input exceeds $T_{\mathrm{worst}}(n)$ — what you promise to customers.
2. **Well-defined.** No distribution to choose.
3. **Adversarial settings.** Cryptography and security face inputs designed against you.
4. **Often the typical case.** Insertion sort is $\Theta(n^2)$ on most realistic inputs.

### When average case matters

- The worst case is unrealistically bad: **quicksort** worst is $\Theta(n^2)$, average is $\Theta(n \log n)$.
- Inputs really do come from a known distribution (e.g., bucket sort).

\vspace{0.5em}

The pitfall: *"average over what?"* — claims about average case must specify the input distribution.

### Expected vs. average — subtle distinction

\begin{block}{Two different averages}
\begin{itemize}
  \item \textbf{Average-case:} averaging over a distribution of \emph{inputs}.
  \item \textbf{Expected:} averaging over the algorithm's \emph{random choices}.
\end{itemize}
\end{block}

\vspace{0.5em}

Randomized quicksort's $\Theta(n \log n)$ is **expected**, not average:

> *For every fixed input, expected running time over random pivots is $\Theta(n \log n)$.*

Stronger than the deterministic average-case claim.

## 13. The Systematic Procedure

### Six steps for analyzing a piece of code

1. **Input size $n$** — array length, $|V|+|E|$, bit length…
2. **Dominant operation** — comparisons, accesses, arithmetic.
3. **Count operations** as a function of $n$.
4. **Closed-form** via summations or recurrence solutions.
5. **Asymptotic notation** — drop constants and lower-order terms.
6. **State the bound** — which case, $O$ vs $\Theta$ vs $\Omega$.

\vspace{0.5em}

With practice these fuse into one process. Worth doing **explicitly** at first.

### A trap in Step 1 — what counts as $n$?

Trial-division primality on integer $N$ does $O(\sqrt N)$ work.

The input size is the **bit length** $n = \log_2 N$, so $N = 2^n$ and the algorithm runs in

$$O(2^{n/2})$$

\vspace{0.5em}

— exponential in the input size. The choice of $n$ silently changed the conclusion.

### Worked example — binary search

```text
lo = 0; hi = n − 1
while lo ≤ hi:
    mid = (lo + hi) / 2
    if A[mid] == target: return mid
    else if A[mid] < target: lo = mid + 1
    else: hi = mid − 1
return -1
```

\vspace{0.4em}

\small
- **Step 1:** $n$ = array length.
- **Step 2:** comparison `A[mid] == target`.
- **Step 3:** Each iteration halves the interval. Loop runs while $2^k \le n$, so at most $\lfloor \log_2 n \rfloor + 1$ iterations.
- **Step 5:** $\lfloor \log_2 n \rfloor + 1 = \Theta(\log n)$.
- **Step 6:** $\boxed{\Theta(\log n)}$ worst case; $\Theta(1)$ best case.

## 14. Analyzing Loops

### 14.1–14.2 Simple and nested

```text
for i = 1 to n:                 # Θ(n)
    constant-time work

for i = 1 to n:                 # Θ(n²)
    for j = 1 to n:
        constant-time work
```

\vspace{0.5em}

The rectangular nested case is the prototype for any analysis where the cost **multiplies.**

### 14.3 Triangular nested

```text
for i = 1 to n:
    for j = i to n:
        constant-time work
```

\vspace{0.4em}

Total iterations:
$$\sum_{i=1}^{n} (n - i + 1) \;=\; \frac{n(n+1)}{2} \;=\; \Theta(n^2)$$

\vspace{0.4em}

Same asymptotic class as rectangular — only the **constant** halves.

### 14.4 Geometric loop

```text
i = 1
while i ≤ n:
    constant-time work
    i = i · 2
```

\vspace{0.4em}

$i$ takes values $1, 2, 4, 8, \ldots$ until $i > n$. Iterations: $\lfloor \log_2 n \rfloor + 1$.

\vspace{0.4em}

\textbf{Cost: } $\Theta(\log n)$. Same conclusion if $i$ is divided by any constant $b > 1$ — the base disappears.

### 14.5 The harmonic / outer×inner pattern

```text
for i = 1 to n:
    j = 1
    while j ≤ n:
        constant-time work
        j = j · 2
```

\vspace{0.4em}

Outer: $n$ iterations. Inner: $\Theta(\log n)$ each. Multiply.

$$\boxed{\Theta(n \log n)}$$

\vspace{0.5em}
This is the canonical pattern for $n \log n$ algorithms.

### 14.6 Variable-step loops need amortized analysis

```text
i = 1
while i ≤ n:
    constant-time work
    if condition: i = i + 1
    else:         i = i · 2
```

\vspace{0.4em}

Cost per iteration is **not uniform**. Direct counting fails.

\vspace{0.5em}

Right framework: **amortized analysis** (§19) — charge expensive iterations against many cheap ones.

## 15. Summation Formulas

### 15.1 Arithmetic series

$$\sum_{i=1}^{n} i \;=\; \frac{n(n+1)}{2} \;=\; \Theta(n^2)$$

$$\sum_{i=1}^{n} i^k \;=\; \Theta(n^{k+1}) \quad \text{for any constant } k \ge 0$$

\vspace{0.5em}

**Where it shows up:** insertion / selection sort inner-loop count, triangular nested loops, Bellman–Ford total edge relaxations.

### 15.2 Geometric series

For $r \ne 1$:

$$\sum_{i=0}^{n} r^i \;=\; \frac{r^{n+1} - 1}{r - 1}$$

\vspace{0.5em}

\begin{block}{The asymmetric rule}
\begin{itemize}
  \item $r > 1$: sum is $\Theta(r^n)$ — dominated by the \textbf{largest} term.
  \item $0 < r < 1$: sum converges, $\Theta(1)$ — dominated by the \textbf{first} term.
\end{itemize}
\end{block}

\vspace{0.4em}

**Where it shows up:** dynamic array doubling, Master Theorem Case 1 / Case 3 level-by-level cost.

### 15.3 Harmonic series

$$H_n \;=\; \sum_{i=1}^{n} \frac{1}{i} \;=\; \ln(n) + \gamma + O(1/n) \;=\; \Theta(\log n)$$

\vspace{0.3em}

with Euler–Mascheroni constant $\gamma \approx 0.5772$.

\vspace{0.6em}

The reason "do $1 + 1/2 + 1/3 + \cdots + 1/n$ work" gives $\Theta(n \log n)$.

\vspace{0.5em}

**Where it shows up:** expected comparisons in randomized quicksort; expected depth of a random BST — both via indicator-variable arguments.

### 15.4 Log-weighted sums; Stirling

\begin{block}{Stirling consequence}
$$\sum_{i=1}^{n} \log i \;=\; \log(n!) \;=\; \Theta(n \log n)$$
\end{block}

This is the $\Omega(n \log n)$ lower bound for comparison-based sorting.

\vspace{0.4em}

$$\sum_{i=1}^{n} i \log i \;=\; \Theta(n^2 \log n)$$

### 15.5 Telescoping

A sum $\sum (a_i - a_{i-1})$ **collapses** to $a_n - a_0$.

\vspace{0.4em}

Example — partial fractions:
$$\sum_{i=1}^{n} \frac{1}{i(i+1)} \;=\; \sum_{i=1}^{n} \!\left(\frac{1}{i} - \frac{1}{i+1}\right) \;=\; 1 - \frac{1}{n+1} \;=\; \Theta(1)$$

\vspace{0.5em}

**Where it shows up:** the $\Theta(n)$ `build-heap` bound; potential-method analyses where $\Delta\Phi$ telescopes to $\Phi_{\text{final}} - \Phi_{\text{initial}}$.

## 16. Solving Recurrences

### A recursive algorithm satisfies a recurrence

Mergesort: divides input in half, recurses, merges in linear time:

$$T(n) \;=\; 2 \, T(n/2) + \Theta(n), \qquad T(1) = \Theta(1)$$

\vspace{0.5em}

Three standard methods to solve such recurrences:

1. **Substitution method** — guess and verify by induction.
2. **Recursion tree** — sum work level by level.
3. **Master Theorem** — pattern-match against the general form.

### 16.1 Substitution method

Guess a closed form; verify by induction.

\vspace{0.4em}

Solve $T(n) = 2T(n/2) + n$, $T(1) = 1$.

- **Guess:** $T(n) \le c \, n \log_2 n$.
- **Verify:** assume $T(n/2) \le c (n/2) \log_2(n/2)$. Then
  $$T(n) \le c n \log_2(n/2) + n = c n \log_2 n - cn + n$$
  $\le c n \log_2 n$ provided $c \ge 1$. ✓
- **Base case:** $T(1) = 1 \not\le c \log_2 1 = 0$. Verify at $T(2) = 4 \le 2c$ instead.

$\Rightarrow T(n) = O(n \log n)$.

### 16.1 Substitution — strengthening the hypothesis

When the obvious guess leaks a constant per step, **subtract** a lower-order term.

\vspace{0.4em}

Solve $T(n) = T(\lfloor n/2 \rfloor) + T(\lceil n/2 \rceil) + 1$, $T(1) = 1$.

- Guess $T(n) \le c n$ fails: $T(n) \le c n + 1 \not\le c n$.
- Strengthen: guess $T(n) \le c n - d$. Then
  $$T(n) \;\le\; (c\lfloor n/2 \rfloor - d) + (c \lceil n/2 \rceil - d) + 1 \;=\; cn - 2d + 1$$
  $\le c n - d$ iff $d \ge 1$. ✓

$\Rightarrow T(n) = O(n)$. **Strengthen, don't relax.**

### 16.2 Recursion tree

Draw the tree; sum work at each level.

```text
Level 0:                       n
                             /   \
Level 1:                  n/2     n/2          sum: n
                         /   \   /   \
Level 2:              n/4   n/4 n/4   n/4      sum: n
                        ...
Level log₂ n:    n leaves of size 1             sum: n
```

\vspace{0.4em}

Every level contributes $n$; $\log_2 n + 1$ levels. Total: $\Theta(n \log n)$.

\vspace{0.3em}

Excellent for intuition about **where** the cost lives.

## 17. The Master Theorem

### 17.0 The setup

For recurrences of the form
$$T(n) \;=\; a \cdot T(n/b) + f(n)$$
with $a \ge 1$, $b > 1$, $T(1) = \Theta(1)$.

\vspace{0.4em}

- $a$ — number of subproblems per level.
- $b$ — size shrinkage factor.
- $f(n)$ — divide-and-combine cost.

\vspace{0.5em}

**Critical exponent:**
$$c^* \;=\; \log_b a$$

The recurrence's behavior depends on how $f(n)$ compares to $n^{c^*}$.

### 17.1 The three cases

\begin{block}{Case 1 — leaves dominate}
If $f(n) = O(n^{c^* - \varepsilon})$ for some $\varepsilon > 0$:
$$T(n) = \Theta(n^{c^*})$$
\end{block}

\begin{block}{Case 2 — every level equal}
If $f(n) = \Theta(n^{c^*})$:
$$T(n) = \Theta(n^{c^*} \log n)$$
\end{block}

\begin{block}{Case 3 — root dominates}
If $f(n) = \Omega(n^{c^* + \varepsilon})$ \emph{and} regularity holds $a f(n/b) \le k f(n)$ for some $k < 1$:
$$T(n) = \Theta(f(n))$$
\end{block}

### 17.2 Why these three — geometric series at every level

At level $k$: $a^k$ subproblems of size $n/b^k$.

Level cost: $a^k \cdot f(n/b^k)$. Total over the tree is a **geometric series** in the ratio $a / b^{c^* \pm \varepsilon}$.

\vspace{0.4em}

\begin{tabular}{lll}
\textbf{Case} & \textbf{Series ratio} & \textbf{Dominated by} \\
1 ($f \prec n^{c^*}$) & $> 1$ & the leaves \\
2 ($f \asymp n^{c^*}$) & $= 1$ & every level equally \\
3 ($f \succ n^{c^*}$) & $< 1$ & the root \\
\end{tabular}

\vspace{0.5em}

**Memorize this, not the three cases.**

### 17.3 Master Theorem in practice

\small

| Recurrence | $c^*$ | $f(n)$ | Case | $T(n)$ |
|---|---|---|---|---|
| $2T(n/2) + n$ | 1 | $\Theta(n)$ | 2 | $\Theta(n \log n)$ |
| $2T(n/2) + n^2$ | 1 | $\Theta(n^2)$ | 3 | $\Theta(n^2)$ |
| $2T(n/2) + 1$ | 1 | $\Theta(1)$ | 1 | $\Theta(n)$ |
| $4T(n/2) + n^2$ | 2 | $\Theta(n^2)$ | 2 | $\Theta(n^2 \log n)$ |
| $T(n/2) + 1$ | 0 | $\Theta(1)$ | 2 | $\Theta(\log n)$ |
| $T(n/2) + n$ | 0 | $\Theta(n)$ | 3 | $\Theta(n)$ |
| $7T(n/2) + n^2$ | $\log_2 7$ | $\Theta(n^2)$ | 1 | $\Theta(n^{\log_2 7})$ |

\vspace{0.4em}
\normalsize
The last is **Strassen's matrix multiplication** $\approx \Theta(n^{2.807})$.

### 17.4 Where the Master Theorem fails

Three failure modes:

1. **$f$ in a gap between cases** — e.g. $T(n) = 2T(n/2) + n \log n$. Here $c^* = 1$, $f = n \log n$: larger than $n$ but not polynomially larger. Master is silent.
2. **Non-canonical form** — unequal subproblem sizes like $T(n) = T(n/3) + T(2n/3) + n$.
3. **$a$, $b$, or $f$ not constant.**

\vspace{0.5em}

Fall back to substitution, recursion tree, or **Akra–Bazzi**.

### 17.4 Gap case — recursion tree to the rescue

$T(n) = 2T(n/2) + n \log n$. At level $k$, $2^k$ subproblems of size $n/2^k$:

$$2^k \cdot (n/2^k) \cdot \log(n/2^k) \;=\; n(\log n - k)$$

\vspace{0.4em}

Summing across $\log n$ levels:

$$T(n) \;=\; \sum_{k=0}^{\log n - 1} n(\log n - k) \;=\; n \cdot \frac{(\log n)(\log n + 1)}{2} \;=\; \boxed{\Theta(n \log^2 n)}$$

\vspace{0.4em}
\small
Extended Case 2: $f = n^{c^*} \log^k n \Rightarrow T = n^{c^*} \log^{k+1} n$. Same answer in one line.

## 18. The Akra–Bazzi Method

### Generalization of the Master Theorem

For
$$T(n) \;=\; \sum_{i=1}^{k} a_i \, T(b_i n + h_i(n)) + g(n)$$
with $a_i > 0$, $0 < b_i < 1$, $h_i(n) = O(n / \log^2 n)$.

\vspace{0.4em}

Define $p$ as the unique real solution to
$$\sum_{i=1}^{k} a_i b_i^p \;=\; 1$$

Then
$$T(n) \;=\; \Theta\!\left(n^p \left(1 + \int_1^n \frac{g(u)}{u^{p+1}} \, du\right)\right)$$

### Akra–Bazzi example

Median-of-medians selection: $T(n) = T(n/3) + T(2n/3) + n$.

\vspace{0.4em}

Exponent equation: $(1/3)^p + (2/3)^p = 1 \;\Rightarrow\; p = 1$ (since $1/3 + 2/3 = 1$).

\vspace{0.4em}

$$T(n) \;=\; \Theta\!\left(n\!\left(1 + \int_1^n \frac{u}{u^2}\, du\right)\right) \;=\; \Theta(n(1 + \log n)) \;=\; \Theta(n \log n)$$

\vspace{0.4em}

(Tighter analysis improves this to $\Theta(n)$ for median-of-medians.)

## 19. Amortized Analysis

### What it is — and isn't

\begin{block}{Amortized analysis}
Worst-case bound on the \textbf{average} cost of an operation over a worst-case \emph{sequence} of operations.
\end{block}

\vspace{0.4em}

Three methods:

1. **Aggregate** — bound the total cost of $m$ operations; divide by $m$.
2. **Accounting** — charge "credits" to cheap ops; spend them on expensive ones.
3. **Potential** — define $\Phi$ reflecting stored work; amortized $=$ actual $+ \Delta\Phi$.

\vspace{0.4em}

Not the same as average-case (which assumes an input distribution).

### 19.2 Dynamic array — aggregate method

Doubling on overflow. Single push: up to $\Theta(n)$. **Amortized:** $\Theta(1)$.

\vspace{0.5em}

\small
- Of $n$ pushes, only $\lceil \log_2 n \rceil$ trigger reallocations.
- Reallocations cost $1 + 2 + 4 + \cdots + n = 2n - 1 = \Theta(n)$.
- Plus $n$ unit-cost pushes $\Rightarrow$ total $\Theta(n)$.
- Per operation: $\boxed{\Theta(1)}$ amortized.

\normalsize
\vspace{0.5em}

This is why `list.append` (Python), `ArrayList.add` (Java), `vector::push_back` (C++) are efficient in practice.

### 19.3 Stack with multipop — accounting method

Stack ops: **push**, **pop**, **multipop($k$)** (cost $\Theta(\min(k, s))$).

\vspace{0.5em}

**Credit assignment:**

- Each **push**: charge 2 credits — 1 for itself, 1 stored on the pushed element.
- Each **pop** / **multipop step**: charge 0 — the stored credit pays.

\vspace{0.4em}

Invariant holds (every element has its stored credit). Over $m$ operations, total credits $\le 2m$.

\vspace{0.4em}

$$\text{Amortized cost per op} \;=\; O(1)$$

### 19.4 Binary counter — potential method

Increment flips bits LSB-up until it hits a 0.

\vspace{0.4em}

**Potential:** $\Phi$ = number of $1$-bits in the counter.

\vspace{0.4em}

Suppose an increment flips $t$ bits from $1 \to 0$ and one bit from $0 \to 1$.

\begin{align*}
\text{actual cost} &= t + 1 \\
\Delta\Phi &= 1 - t \\
\text{amortized cost} &= (t + 1) + (1 - t) \;=\; 2
\end{align*}

\vspace{0.4em}

$\Phi \ge 0$, $\Phi_0 = 0 \Rightarrow$ total actual $\le$ total amortized. **$O(1)$ amortized per increment.**

## 20. Space Complexity

### What to count

- **Auxiliary space:** memory beyond the input (in-place convention).
- **Call stack depth:** $O(d)$ for recursion of depth $d$ with $O(1)$ locals per frame.

\vspace{0.5em}

\small
| Algorithm | Time | Aux. space | Why |
|---|---|---|---|
| Iterative binary search | $\Theta(\log n)$ | $\Theta(1)$ | 3 variables |
| Recursive binary search | $\Theta(\log n)$ | $\Theta(\log n)$ | call stack |
| Mergesort | $\Theta(n \log n)$ | $\Theta(n)$ | merge scratch |
| Quicksort (avg) | $\Theta(n \log n)$ | $\Theta(\log n)$ exp. | stack depth |
| BFS / DFS | $\Theta(n + m)$ | $\Theta(n)$ | queue / stack |
| 2-D DP | $\Theta(nm)$ | $\Theta(nm)$ | full table |

### Recursion depth — only one branch is active

For $T(n) = a T(n/b) + f(n)$, the space recurrence is

$$S(n) \;=\; S(n/b) + g(n)$$

— only **one** branch is live on the call stack at a time.

\vspace{0.5em}

Mergesort: deepest level $\Theta(1)$, level above $\Theta(n/2)$, …, root $\Theta(n)$. Root dominates.

$$\boxed{S(n) = \Theta(n)}$$

### Space–time tradeoffs

\begin{itemize}
  \item \textbf{Memoization} turns exponential-time recursion into polynomial, at the cost of a subproblem table.
  \item \textbf{Row compression in DP:} when row $i$ depends only on row $i-1$, store two rows instead of all of them. LCS / edit distance: $\Theta(nm)$ time but $\Theta(\min(n,m))$ space.
\end{itemize}

\vspace{0.5em}

The asymptotic class of time stays the same; the constant in memory drops dramatically.

## 21. Randomized Analysis

### Indicator random variables + linearity of expectation

For an event $A$:
$$X_A = \begin{cases} 1 & \text{if } A \text{ occurs} \\ 0 & \text{otherwise} \end{cases}
\qquad \mathbb{E}[X_A] = \Pr[A]$$

\vspace{0.4em}

\begin{block}{Linearity (independence not required)}
$$\mathbb{E}[X_1 + \cdots + X_k] \;=\; \mathbb{E}[X_1] + \cdots + \mathbb{E}[X_k]$$
\end{block}

\vspace{0.3em}

Decompose a complex global quantity into pairwise indicators, take expectations one by one, sum.

### Expected comparisons in randomized quicksort

Let $z_1 < z_2 < \cdots < z_n$ be the sorted input. Define
$$X_{ij} = \mathbf{1}[z_i \text{ and } z_j \text{ ever directly compared}]$$

\vspace{0.4em}

Total comparisons $X = \sum_{i<j} X_{ij}$. By linearity:
$$\mathbb{E}[X] \;=\; \sum_{i<j} \Pr[z_i, z_j \text{ compared}]$$

\vspace{0.4em}

$z_i, z_j$ compared $\iff$ one of them is the first pivot from $\{z_i, \ldots, z_j\}$:
$$\Pr[\cdot] \;=\; \frac{2}{j - i + 1}$$

### Summing — harmonic series strikes again

$$\mathbb{E}[X] \;=\; \sum_{i=1}^{n-1} \sum_{k=1}^{n-i} \frac{2}{k+1} \;\le\; 2(n-1) H_n \;=\; \Theta(n \log n)$$

\vspace{0.4em}

\begin{alertblock}{The key point}
This is a bound on \emph{every input} taken over the algorithm's coin flips — not an average over input distributions.
\end{alertblock}

\vspace{0.3em}

Randomized quicksort makes $\boxed{\Theta(n \log n)}$ comparisons in expectation on every input.

### Las Vegas vs. Monte Carlo

:::::: {.columns}
::: {.column width="50%"}
**Las Vegas**

- Always correct.
- Running time is random.
- Example: randomized quicksort.
- Bound the expected running time.

\vspace{0.3em}
*"Surgical robot"*
:::
::: {.column width="50%"}
**Monte Carlo**

- Bounded running time.
- Bounded probability of wrong answer.
- Example: Miller–Rabin primality.
- Bound runtime **and** error.

\vspace{0.3em}
*"Bloom filter"*
:::
::::::

\vspace{0.5em}

Interconvertible by time-cutoff (LV $\to$ MC) or verify-and-retry (MC $\to$ LV when verifying is easy).

## 22. Common Pitfalls

### 22.1–22.2 Notation and what counts as $n$

**Confusing $O$ with $\Theta$.**
Mergesort is $O(n^2)$ — technically true, useless. Use $\Theta$ when you can prove it.
Mirror error: claiming $\Theta$ when only $O$ is justified (worst case of randomized quicksort is $\Theta(n^2)$, not $\Theta(n \log n)$).

\vspace{0.6em}

**Hidden inputs change "the" input size.**
0/1 knapsack runs in $\Theta(nW)$ — polynomial in $W$ the *value*, exponential in $\log W$ the *bit length*.
Always specify what $n$ counts.

### 22.5 Don't treat $\log$ as a constant

For "all reasonable inputs" $\log n \le 64$, so it feels constant.

It is not.

\vspace{0.4em}

An $n^2 \log n$ algorithm is **not** $O(n^2)$.

\vspace{0.4em}

At scale, the $\log n$ factor decides which of two candidates runs out of time first.

\vspace{0.5em}

The shortcut is fine for back-of-envelope runtime estimates. Not for asymptotic claims.

### 22.7 Master Theorem misapplications

**1. Forgetting Case 3's regularity condition.**
$T(n) = T(n/2) + n / \log n$: $f$ is asymptotically larger than $n^{c^*} = 1$ but **not** $\Omega(n^\varepsilon)$ for any $\varepsilon > 0$. Case 3 does not apply.

\vspace{0.5em}

**2. Treating non-canonical recurrences as canonical.**
$T(n) = 2 T(n-1) + 1$ is *not* of the form $a T(n/b) + f(n)$ — subproblem size is $n - 1$, not $n/b$. (Answer is $\Theta(2^n)$ by inspection.)

### 22.8 The four "average" terms are different

| Term | Averages over… |
|---|---|
| **Worst case** | inputs (max) |
| **Best case** | inputs (min) |
| **Average case** | a distribution on inputs |
| **Expected** | the algorithm's coin flips, per input |

\vspace{0.5em}

*"Quicksort is $O(n \log n)$ on average"* and *"randomized quicksort has expected time $O(n \log n)$"* are different claims. The second is **strictly stronger.**

### 22.9–22.10 Constants and base cases

**Ignore constants only when they're ignorable.**
$10^6 \cdot n$ is "linear" but slower than $\Theta(n^2)$ for $n \le 10^6$.

Galactic algorithms (e.g. $O(n^{2.373})$ matrix multiply) are asymptotically faster than Strassen but slower on every $n$ that fits in a galaxy.

\vspace{0.5em}

**Check the base case of recurrences.**
$T(n) = 2T(n/2) + n$ with $T(1) = 1$ solves to $\Theta(n \log n)$.
With $T(1) = n$ it does **not** — the base violates $T(1) = \Theta(1)$. Either factor base cost into the recurrence or fix the boundary.

### Recap

\begin{itemize}
  \item Six-step procedure; state \emph{which case} and \emph{which notation}.
  \item Loop patterns: simple, nested, triangular, geometric, harmonic, amortized.
  \item Recurrence solving: substitution, recursion tree, Master Theorem, Akra–Bazzi.
  \item Master Theorem cases come from one geometric-series calculation.
  \item Amortized $\ne$ average — three methods, all worst-case on the sequence.
  \item Indicator variables + linearity = the randomized analyst's main tool.
  \item Pitfalls: $\log$ is not a constant; specify what $n$ counts.
\end{itemize}

\vspace{0.4em}
Next: turning the analysis machinery on concrete algorithms — \textbf{Part IV.}
