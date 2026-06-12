---
title: "RAM Model & Asymptotic Analysis"
subtitle: "Part II — Asymptotic Analysis"
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

## 6. Why We Need Asymptotic Notation

### The problem with exact counts

Counting operations gives expressions like:

$$T(n) = 4n^3 + 17 n^2 \log n + 100 n + 250$$

Technically correct, practically misleading. The constants depend on:

- How you choose to count.
- The compiler's optimizations.
- The CPU's per-instruction cycle counts.
- The memory hierarchy.

### What is robust

What does **not** depend on those accidents is the **growth rate** as $n \to \infty$.

The $4n^3$ term will eventually dwarf the rest. The coefficient $4$ varies by machine. The $n^3$ **stays invariant**.

\vspace{0.6em}
\begin{block}{The job of asymptotic notation}
Capture growth rates while ignoring constants and lower-order terms.

This is what makes algorithm analysis machine-independent and language-independent.
\end{block}

## 7. Big O, Big Omega, Big Theta

### 7.1 Big O — the upper bound

\begin{block}{Definition}
$f(n) = O(g(n))$ if there exist constants $c > 0$ and $n_0$ such that
$$0 \;\le\; f(n) \;\le\; c \cdot g(n) \qquad \text{for all } n \ge n_0.$$
\end{block}

$f$ is eventually bounded above by a constant multiple of $g$.

\vspace{0.5em}

\small
**Notation warning.** $O(g(n))$ is really a *set*. The conventional $f = O(g)$ reads "$f$ is in $O(g)$." It's asymmetric: $O(n) = O(n^2)$ is true; $O(n^2) = O(n)$ is **false.**

### 7.2 Big Omega — the lower bound

\begin{block}{Definition}
$f(n) = \Omega(g(n))$ if there exist constants $c > 0$ and $n_0$ such that
$$0 \;\le\; c \cdot g(n) \;\le\; f(n) \qquad \text{for all } n \ge n_0.$$
\end{block}

$f$ is eventually bounded below by a constant multiple of $g$.

\vspace{0.5em}

Dual to Big O:
$$f = \Omega(g) \;\iff\; g = O(f)$$

### 7.3 Big Theta — the tight bound

\begin{block}{Definition}
$f(n) = \Theta(g(n))$ if $f = O(g)$ \emph{and} $f = \Omega(g)$.
\end{block}

Equivalently, there exist $c_1, c_2, n_0$ such that

$$0 \;\le\; c_1 \cdot g(n) \;\le\; f(n) \;\le\; c_2 \cdot g(n) \qquad \text{for all } n \ge n_0.$$

\vspace{0.5em}

$f$ and $g$ grow at the **same rate** up to constants.

Theta is the strongest — use it when you can prove it.

### 7.4 Visual intuition

```text
                                  c₂·g(n)   ← upper bound (Big O)
                              .··
                        ___.··  f(n)
                  __.··  __··    ← actual function
              .·· _ . ··
          .··.···
       _.··                       c₁·g(n)   ← lower bound (Big Omega)
   _.··
.··
─────────────────────────────── n
        n₀
```

If $f$ is sandwiched between $c_1 g$ and $c_2 g$ for $n \ge n_0$, then $f = \Theta(g)$.

## 8. Little o and Little Omega

### 8.1 Little o — strict slow growth

\begin{block}{Definition}
$f(n) = o(g(n))$ if for \emph{every} $c > 0$ there exists $n_0$ such that
$$0 \;\le\; f(n) \;<\; c \cdot g(n) \qquad \text{for all } n \ge n_0.$$
\end{block}

$f$ grows **strictly slower** than $g$. Equivalently:

$$f(n) = o(g(n)) \;\iff\; \lim_{n \to \infty} \frac{f(n)}{g(n)} = 0$$

\vspace{0.3em}
Examples: $n = o(n^2)$, \; $n \log n = o(n^2)$, \; $n^2 = o(n^3)$.

### 8.2 Little omega — strict fast growth

\begin{block}{Definition}
$f(n) = \omega(g(n))$ if for \emph{every} $c > 0$ there exists $n_0$ such that
$$0 \;\le\; c \cdot g(n) \;<\; f(n) \qquad \text{for all } n \ge n_0.$$
\end{block}

$f$ grows **strictly faster** than $g$. Equivalently:

$$f(n) = \omega(g(n)) \;\iff\; \lim_{n \to \infty} \frac{f(n)}{g(n)} = \infty$$

### 8.3 The five-way summary

\small

| Notation | Meaning | Limit (when it exists) |
|---|---|---|
| $f = O(g)$ | no faster than | $\lim f/g < \infty$ |
| $f = \Omega(g)$ | no slower than | $\lim f/g > 0$ |
| $f = \Theta(g)$ | same rate | $0 < \lim f/g < \infty$ |
| $f = o(g)$ | strictly slower than | $\lim f/g = 0$ |
| $f = \omega(g)$ | strictly faster than | $\lim f/g = \infty$ |

\normalsize
\vspace{0.4em}

The big-letter family mirrors $\le, =, \ge$.
The little-letter family mirrors $<, >$.

## 9. Properties and Theorems

### 9.1–9.3  Reflexivity, symmetry, transitivity

- **Reflexive:** $f = O(f)$, $f = \Omega(f)$, $f = \Theta(f)$ for any $f$.
- **Symmetric** ($\Theta$ only): $f = \Theta(g) \iff g = \Theta(f)$.
- **Dual** (not symmetric): $f = O(g) \iff g = \Omega(f)$.
- **Transitive:** $f = O(g)$ and $g = O(h) \Rightarrow f = O(h)$. Same for $\Omega, \Theta, o, \omega$.

### 9.4 Constants are absorbed

\begin{block}{Rule}
For any constant $c > 0$:
$$c \cdot f(n) = \Theta(f(n))$$
\end{block}

\vspace{0.5em}

The leading coefficient of a polynomial is irrelevant inside Big O:

$$5n^2 \;=\; 100 n^2 \;=\; \Theta(n^2)$$

### 9.5 The sum rule — sequential composition

If $f_1 = O(g_1)$ and $f_2 = O(g_2)$, then

$$f_1(n) + f_2(n) \;=\; O\!\bigl(\max(g_1(n),\, g_2(n))\bigr)$$

\vspace{0.5em}

Two pieces of code executed sequentially: the **larger** of the two costs dominates.

\vspace{0.5em}
Corollary — same target $g$:
$$f_1 = O(g) \text{ and } f_2 = O(g) \;\Longrightarrow\; f_1 + f_2 = O(g)$$

### 9.6 The product rule — nested loops

If $f_1 = O(g_1)$ and $f_2 = O(g_2)$, then

$$f_1(n) \cdot f_2(n) \;=\; O\!\bigl(g_1(n) \cdot g_2(n)\bigr)$$

\vspace{0.5em}

When code is **nested**, the costs **multiply.**

\vspace{0.5em}

A loop of $O(n)$ iterations whose body is $O(\log n)$ gives $O(n \log n)$.

### 9.7 Polynomials collapse to leading term

For $p(n) = a_d n^d + a_{d-1} n^{d-1} + \cdots + a_0$ with $a_d > 0$:

$$p(n) \;=\; \Theta(n^d)$$

\vspace{0.5em}

Practical implication: when analyzing a polynomial cost, **drop everything except the highest-degree term and its coefficient** — and the coefficient too, once you switch to $\Theta$.

### 9.8 Logarithms — the base doesn't matter

For any constants $b, c > 1$:

$$\log_b(n) \;=\; \Theta(\log_c(n))$$

Reason: $\log_b n = \log_c n / \log_c b$, and the denominator is a constant.

\vspace{0.6em}

\begin{block}{Stirling's approximation}
$$n! \;=\; \sqrt{2 \pi n} \left(\frac{n}{e}\right)^{n} \!\bigl(1 + \Theta(1/n)\bigr)$$
so $\log(n!) = \Theta(n \log n)$ — the reason every comparison sort is $\Omega(n \log n)$.
\end{block}

### 9.8 Logarithms — the two dominance facts

\begin{block}{Polylog vs polynomial}
For any positive $a, b$:
$$(\log n)^a \;=\; o(n^b)$$
\emph{Every polynomial dominates every polylogarithm.}
\end{block}

\vspace{0.6em}

\begin{block}{Polynomial vs exponential}
For any positive $a$ and any $b > 1$:
$$n^a \;=\; o(b^n)$$
\emph{Every exponential dominates every polynomial.}
\end{block}

## 10. The Limit Method

### When a limit exists

\begin{block}{Theorem}
Suppose $\displaystyle L = \lim_{n \to \infty} \frac{f(n)}{g(n)}$ exists (allowing $L = \infty$).
\begin{itemize}
  \item $L = 0$ \quad $\Rightarrow$ \quad $f = o(g)$
  \item $0 < L < \infty$ \quad $\Rightarrow$ \quad $f = \Theta(g)$
  \item $L = \infty$ \quad $\Rightarrow$ \quad $f = \omega(g)$
\end{itemize}
\end{block}

Often the fastest way to settle an asymptotic question.

### Example — polynomials beat polylogs

To compare $n^a$ vs $(\log n)^b$ for positive $a, b$, apply L'Hôpital's rule:

$$\lim_{n \to \infty} \frac{(\log n)^b}{n^a} \;=\; 0$$

\vspace{0.5em}

Therefore $(\log n)^b = o(n^a)$ — polynomials always dominate polylogs.

\vspace{0.8em}

\small
\textbf{When the limit does not exist} (oscillating $f$): fall back to $\limsup$ and $\liminf$ via the definitions.

## 11. The Hierarchy of Growth Rates

### From smallest to largest growth

\small
| Class | Name | $n = 10^6$ |
|---|---|---|
| $1$ | Constant | $1$ |
| $\log \log n$ | Double-log | $\approx 4$ |
| $\log n$ | Logarithmic | $\approx 20$ |
| $(\log n)^k$ | Polylogarithmic | $\approx 20^k$ |
| $\sqrt{n}$ | Square root | $1\,000$ |
| $n / \log n$ | Just below linear | $\approx 50\,000$ |
| $n$ | Linear | $10^6$ |
| $n \log n$ | Linearithmic | $\approx 2 \cdot 10^7$ |
| $n^2$ | Quadratic | $10^{12}$ |
| $n^k$ | Polynomial | $10^{6k}$ |
| $n^{\log n}$ | Quasi-polynomial | astronomical |
| $2^n$ | Exponential | astronomical |
| $n!,\; n^n,\; 2^{2^n}$ | super-exponential | astronomical |

### 11.1 The polynomial vs. exponential dichotomy

The single most important distinction in algorithm analysis.

Suppose each step takes 1 ns. For **$n = 50$**:

\vspace{0.5em}

| Complexity | Wall-clock for $n = 50$ |
|---|---|
| $n$ | 50 ns |
| $n^2$ | 2.5 μs |
| $n^3$ | 125 μs |
| $2^n$ | $\approx$ **13 days** |
| $n!$ | $\approx 10^{52}$ **years** — longer than the universe |

\vspace{0.6em}

A faster computer doesn't save you: doubling speed adds **1** to the largest tractable $n$ for exponential algorithms.

### 11.2 Non-obvious orderings

- **$n / \log n$ sits just below linear.** For $n = 10^6$, $\log n \approx 20$, so $n / \log n \approx 50\,000$ — closer to $n$ than to $\sqrt n$.
- **$n^{\log n} = 2^{(\log n)^2}$** sits *between* polynomial and exponential. Beats every fixed polynomial once $n > 2^k$, but grows far slower than $2^n$.
- **$\log \log n$ is practically constant.** $\log_2 \log_2(10^{18}) \approx 6$. For van Emde Boas trees and cache-oblivious structures, this is essentially "constant time."

### 11.3 Practical thresholds (1 second budget)

\small

| Complexity | Max tractable $n$ |
|---|---|
| $O(n!)$ | $\approx 11$ |
| $O(2^n)$ | $\approx 25$ |
| $O(n^3)$ | $\approx 1\,000$ |
| $O(n^2)$ | $\approx 10^4$ |
| $O(n^{3/2})$ | $\approx 10^6$ |
| $O(n \log n)$ | $\approx 10^8$ |
| $O(n)$ | $\approx 10^9$ |
| $O(\log n)$ | essentially unbounded |

\vspace{0.4em}
\normalsize

Rules of thumb — actual constants vary, but the orders of magnitude are right and worth **memorizing**.

### Recap

\begin{itemize}
  \item $O,\Omega,\Theta$ correspond to $\le, \ge, =$. \quad $o,\omega$ correspond to $<, >$.
  \item Constants and lower-order terms disappear; logarithm bases disappear.
  \item Sequential composition $\Rightarrow$ \textbf{sum rule}; nesting $\Rightarrow$ \textbf{product rule}.
  \item The hierarchy: $\log\log < \log < \text{polylog} < \sqrt n < n < n\log n < n^k < n^{\log n} < 2^n < n!$
  \item Polynomial vs.\ exponential is the dividing line between tractable and not.
\end{itemize}

\vspace{0.4em}
Next: turning these tools on real code — \textbf{Part III, Mechanics.}
