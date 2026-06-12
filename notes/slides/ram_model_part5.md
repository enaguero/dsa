---
title: "RAM Model & Asymptotic Analysis"
subtitle: "Part V — Beyond the Basic RAM Model"
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

## 28. Limitations of the RAM Model

### Three classes of deviation

The RAM model is excellent but not perfect.

\vspace{0.5em}

1. **Non-uniform operation costs** — add ≠ mul ≠ div.
2. **The memory hierarchy** — cache, RAM, disk are not all "one cycle."
3. **Word size** — assumes every value fits in a word.

\vspace{0.5em}

These rarely change the asymptotic conclusion. They often change **practice** by an order of magnitude.

### 28.1 Real per-operation costs

| Operation | Cycles |
|---|---|
| Integer add, bitwise | 1 |
| Integer multiply | 3–5 |
| Integer divide | 20–40 |
| Float ops | 3–10 |

\vspace{0.5em}

The RAM model charges all of these the same.

\vspace{0.5em}

Affects constants, not Big O. But a tight loop full of `div` can be 20× slower than the "$\Theta$" suggests.

### 28.2 The memory hierarchy — six orders of magnitude

| Storage level | Latency |
|---|---|
| Register | $< 1$ ns |
| L1 cache | $1$ ns |
| L2 cache | $4$ ns |
| L3 cache | $12$ ns |
| Main memory | $100$ ns |
| SSD | $100$ μs |
| Disk | $10$ ms |

\vspace{0.4em}

Naive vs. cache-blocked matrix multiply: both $\Theta(n^3)$, latter is many times faster at large $n$.

\vspace{0.4em}

\textbf{Cache locality is invisible to Big O.}

### 28.3 Word size

Uniform cost implicitly assumes every value fits in a machine word.

\vspace{0.5em}

For cryptography, number theory, computer algebra — false.

\vspace{0.5em}

The fix: switch to the **logarithmic cost criterion** (Part I §4.2), or count operations explicitly in bit complexity.

## 29. The External Memory Model

### The setup

\textbf{Aggarwal–Vitter, 1988.}

\vspace{0.4em}

When data doesn't fit in RAM, **I/O dominates**.

\vspace{0.5em}

\begin{block}{Model parameters}
\begin{itemize}
  \item Fast internal memory of size $M$.
  \item Slow external memory of unbounded size.
  \item Data moves in \textbf{blocks of size $B$}.
  \item Cost = number of \textbf{block transfers}. CPU on cached data is free.
\end{itemize}
\end{block}

### Sample bounds

| Operation | I/Os |
|---|---|
| Scan $N$ elements | $\Theta(N/B)$ |
| External mergesort | $\Theta\!\left((N/B) \log_{M/B}(N/B)\right)$ |
| B-tree search | $\Theta(\log_B N)$ |

\vspace{0.5em}

These bounds **explain** why:

- Databases use B-trees, not balanced BSTs.
- Large-scale data processing uses external sort.
- The constants in $\log_B$ matter — fewer levels, fewer I/Os.

## 30. Cache-Oblivious Analysis

### Optimal cache use *without* knowing the cache

\textbf{Frigo–Leiserson–Prokop–Ramachandran, 1999.}

\vspace{0.4em}

Same two-level model — but the algorithm **does not know** $M$ or $B$.

\vspace{0.5em}

\begin{block}{The remarkable claim}
You can achieve optimal cache performance across \emph{all} memory hierarchies simultaneously, without ever reading the parameters.
\end{block}

\vspace{0.5em}

Canonical examples:

- Recursive matrix transpose and multiply.
- Funnelsort.
- Cache-oblivious B-trees.

\vspace{0.4em}

The technique is mostly: **divide recursively until you fit**, and let the recursion pick the right granularity by accident.

## 31. Parallel Models

### 31.1 The PRAM

Multiple processors share one memory and execute in **lockstep**.

\vspace{0.4em}

Variants by concurrent-access rules:

- **EREW** — Exclusive Read, Exclusive Write
- **CREW** — Concurrent Read, Exclusive Write
- **CRCW** — Concurrent Read, Concurrent Write

\vspace{0.5em}

Theoretically clean. **Operationally awkward** — real hardware does not synchronize on every step.

### 31.2 Work–Span

A more flexible model that captures *dynamic* parallelism.

\vspace{0.4em}

- **Work** $W(n)$ = total operations.
- **Span** $S(n)$ = length of the longest dependency chain (critical path).

\vspace{0.4em}

\begin{block}{Brent's theorem}
On $p$ processors:
$$T_p \;\ge\; \max\!\left(W/p,\; S\right)$$
and a good scheduler achieves this bound.
\end{block}

\vspace{0.4em}

**Parallelism** of the algorithm is $W/S$.

### Parallel mergesort — what good parallelism looks like

\begin{align*}
W(n) &= \Theta(n \log n)  & \text{(matches sequential)} \\
S(n) &= \Theta(\log^2 n)  & \text{(polylog critical path)} \\
\text{parallelism} &= W/S = \Theta\!\left(n/\log n\right)
\end{align*}

\vspace{0.4em}

Enough work-per-step to keep **many** processors busy.

\vspace{0.5em}

The design rule: keep work near sequential, drive span to polylog.

## 32. Lower Bounds

### Why lower bounds matter

Most of the document proves *upper* bounds — "this algorithm runs in $T(n)$."

\vspace{0.4em}

The complementary question — *"could there be a faster one?"* — needs different machinery.

\vspace{0.5em}

Two standard techniques:

1. **Information-theoretic / decision-tree** arguments.
2. **Adversary arguments.**

### 32.1 Information-theoretic lower bounds

If the algorithm uses operations from class $\mathcal{C}$ that yield at most $r$ outcomes per operation, and must distinguish $N$ outputs:

$$\text{worst-case op count} \;\ge\; \lceil \log_r N \rceil$$

\vspace{0.4em}

| Problem | Outputs $N$ | Lower bound |
|---|---|---|
| Sorting $n$ elements | $n!$ | $\Omega(n \log n)$ |
| Element distinctness | reduces to sort | $\Omega(n \log n)$ |
| 2-D Convex hull | reduces to sort | $\Omega(n \log n)$ |

\vspace{0.4em}

\small
**Limitation:** ignores witness complexity. Problems with small output (yes/no) get only $O(1)$ from this — need adversary arguments.

### 32.2 Adversary arguments

An **opponent** answers queries adaptively to keep as much input ambiguity as possible. The algorithm must drive ambiguity to zero.

\vspace{0.5em}

**Finding the minimum requires $\ge n - 1$ comparisons.**

\vspace{0.4em}

*Strategy:* mark all $n$ as candidates. When asked *"is $a < b$?"*, answer consistently with at least one ordering and mark the larger as eliminated.

\vspace{0.4em}

Each comparison eliminates $\le 1$ candidate. To pin a unique minimum, drive $n \to 1$:

$$\ge n - 1 \text{ comparisons.}$$

\vspace{0.4em}

\small
\textbf{Median lower bound:} $\lceil 3n/2 \rceil - 2$ comparisons via a more elaborate adversary.

### 32.3 When the gap is the interesting feature

Sometimes upper and lower bounds **don't match.**

\vspace{0.5em}

**Matrix multiplication:**

\begin{itemize}
  \item Trivial lower bound: $\Omega(n^2)$ (must touch each output entry).
  \item Best known upper: $O(n^{2.373})$ (Le Gall, 2014; lots of follow-ups).
  \item Open: does $\Omega(n^{2+\varepsilon})$ hold for some $\varepsilon > 0$?
\end{itemize}

\vspace{0.5em}

\begin{block}{Structural takeaway}
The gap between known upper and lower bounds is often the most interesting feature of a problem.
\end{block}

## 33. Online Algorithms

### Why standard worst-case isn't fair

An **online algorithm** sees input one item at a time and makes **irrevocable** decisions.

\vspace{0.5em}

Worst-case against arbitrary input is unfair — an *offline omniscient* algorithm always wins.

\vspace{0.5em}

Standard tool: the **competitive ratio**.

### 33.1 The competitive ratio

$A$ is **$c$-competitive** if there exists a constant $\alpha$ such that for every input $\sigma$:

$$A(\sigma) \;\le\; c \cdot \mathrm{OPT}(\sigma) + \alpha$$

\vspace{0.4em}

The smallest such $c$ is the **competitive ratio**.

\vspace{0.4em}

- $c = 1$: matches the offline optimum every input.
- $c > 1$: quantifies the **cost of not seeing the future**.

### 33.2 Ski-rental — the prototype

Each day: rent (cost 1) or buy (cost $B$, valid forever). You don't know how many days you'll ski.

\vspace{0.5em}

\textbf{Offline OPT:} buy iff total days $\ge B$.

\vspace{0.5em}

**Online break-even strategy:**

> *Rent for $B - 1$ days, then buy.*

\vspace{0.4em}

Achieves competitive ratio $2 - 1/B \to 2$. **Lower bound: $2 - o(1)$.**

\vspace{0.4em}

\small
Randomization: drop the deterministic 2 to $e/(e-1) \approx 1.582$.

### 33.2 Paging (LRU) and list update

**Paging.** Cache holds $k$ of $N$ pages; eviction costs 1.

\vspace{0.4em}

LRU is **$k$-competitive** against any offline strategy. Lower bound is $k$, so LRU is optimal up to constants.

\vspace{0.6em}

**List update.** Linked list under access requests; access cost = position.

\vspace{0.4em}

Move-To-Front is **$2$-competitive** — accessing then moving costs at most twice the offline optimum.

\vspace{0.4em}

\small
Randomized paging: $\Theta(\log k)$-competitive via the marking algorithm.

### 33.4 When competitive analysis lies

It compares against an offline optimum that has seen **the entire future** — pessimistic.

\vspace{0.4em}

For structured inputs, alternatives give more realistic bounds:

\vspace{0.5em}

| Alternative | What it does |
|---|---|
| **Resource augmentation** | Give online a bigger cache than offline |
| **Stochastic input** | Assume i.i.d. or Markovian requests |
| **Smoothed analysis** | Adversarial input + small perturbation |

\vspace{0.4em}

These produced more practical bounds for caching, online matching, scheduling.

### Recap — and end of reference

\begin{itemize}
  \item RAM is excellent but blind to operation costs, memory hierarchy, big numbers.
  \item \textbf{External memory model:} cost = block transfers; B-trees and external sort live here.
  \item \textbf{Cache-oblivious:} optimal cache use without knowing the parameters.
  \item \textbf{Work–span:} $W$ matches sequential, $S$ polylogarithmic = scalable parallel.
  \item \textbf{Lower bounds:} information-theoretic (output diversity) and adversary (witness).
  \item \textbf{Competitive analysis:} cost of not seeing the future. Use alternatives when the offline optimum is too strong a baseline.
\end{itemize}

\vspace{0.4em}

\begin{center}
\Large \emph{End of reference.}
\end{center}
