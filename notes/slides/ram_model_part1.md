---
title: "RAM Model & Asymptotic Analysis"
subtitle: "Part I — Theoretical Foundations"
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

## 1. Models of Computation

### Why a model is non-negotiable

A **model of computation** fixes three things:

- The set of admissible **operations**.
- The **cost** charged for each operation.
- The **state** the operations transform.

Without it, *"how fast is this algorithm?"* has no rigorous meaning.

The model is not neutral — different models give different complexity classes.

### Three historical models

:::::: {.columns}
::: {.column width="33%"}
**Turing machine**

(Turing, 1936)

Tape head + infinite tape. Excellent for computability and complexity classes, awkward for algorithms.
:::
::: {.column width="33%"}
**Lambda calculus**

(Church, 1936)

Function abstraction and application. Foundational for PL theory; inconvenient for resource analysis.
:::
::: {.column width="34%"}
**Random Access Machine**

(Cook–Reckhow, 1973)

CPU + random-access memory. Matches imperative code. **Our model.**
:::
::::::

### Why the RAM wins for algorithm analysis

1. Pseudocode in C / C++ / Java / Python translates **directly** into RAM operations.
2. Runtime predictions agree with empirical measurements for almost every algorithm in practice.
3. Simple enough to prove things rigorously about.

\vspace{0.5em}
\begin{block}{Robustness theorem}
A RAM running in time $T(n)$ is simulated by a Turing machine in $O(T(n)^3)$, and vice versa with logarithmic slowdown. So $\mathbf{P}$ is the **same class** under either model.
\end{block}

## 2. The Random Access Machine

### 2.1 Architecture

A **RAM** consists of:

- A read-only **input tape** $x_1, x_2, \ldots, x_n$.
- A write-only **output tape**.
- A fixed **program** $P = (P_1, \ldots, P_q)$.
- A **program counter** $\ell$.
- An **unbounded memory** $M = (M[0], M[1], M[2], \ldots)$.
- $O(1)$ **registers** $R[0], R[1], \ldots, R[r-1]$.

Only registers can be instruction operands. Memory is reached by **indirect addressing** — that's what makes access "random."

### 2.2 Instruction set

\small

| Instruction | Effect |
|---|---|
| `READ R[i]`, `WRITE R[i]` | I/O |
| `LOAD R[i], R[j]` | $R[i] \leftarrow M[R[j]]$ |
| `STORE R[i], R[j]` | $M[R[j]] \leftarrow R[i]$ |
| `MOVE`, `CONST` | register moves and immediates |
| `ADD / SUB / MUL / DIV` | $R[i] \leftarrow R[j]\ \text{op}\ R[k]$ |
| `JUMP` $\lambda$, `JZERO R[i],` $\lambda$ | control flow |
| `HALT` | stop |

\normalsize

Sufficient to express anything a high-level imperative language can.

### 2.3 Configuration and computation

A **configuration** is the tuple

$$\mathbf{C} = (\ell,\, R,\, M,\, \text{input pos},\, \text{output so far})$$

A **computation** is a sequence $C_0 \to C_1 \to C_2 \to \cdots$ determined by the program.

It **halts** on `HALT`. The output is whatever was written.

### 2.4 What this formalism buys us

Precise meaning for:

- *"Runs in time $T(n)$"* — number of transitions on input of size $n$.
- *"Uses space $S(n)$"* — highest memory address touched (+ register contents under log cost).
- *"Is correct"* — halts with the correct output for every valid input.

In practice you analyze pseudocode. The translation is mechanical, the asymptotic count unchanged. The formal model is what **justifies the practice.**

## 3. The Word RAM Model

### 3.1 Definition

The **word RAM** fixes what a cell holds:

- A **word size** $w$ (bits). Each register and cell holds an integer in $\{0, 1, \ldots, 2^w - 1\}$.
- The **transdichotomous assumption**:
  $$w \;\ge\; \lceil \log_2 n \rceil$$
  so one word can address the input.
- Instruction set: arithmetic, bitwise (AND, OR, XOR, shifts), compares, jumps, load/store. **Each is unit cost.**

### 3.2 What is a "word"?

Three defining properties:

1. **Width.** Exactly $w$ bits — on real hardware a constant of the architecture (32 or 64).
2. **Atomicity.** Any arithmetic on word-sized values completes in **one** CPU step.
3. **Addressability.** A word holds any index, pointer, or address used by the algorithm.

"Fits in a word" = $[0, 2^w - 1]$, $O(1)$ to operate on.
"Fits in $O(1)$ words" = e.g. a 256-bit integer on a 64-bit machine.

### 3.3 Why $w \ge \log_2 n$ is reasonable

If $w < \log_2 n$, an index into the input wouldn't fit in a register — array indexing wouldn't be $O(1)$.

In practice $w$ is a hardware constant. Read the assumption as:

\begin{center}
\emph{"For every $n$ we care about, $w \ge \log_2 n$."}
\end{center}

On a 64-bit machine this covers all $n \le 2^{64}$ — about $1.8 \times 10^{19}$ items. More than enough.

### 3.4 Bit tricks and word-level parallelism

In **one** word op an algorithm manipulates $\Theta(w) = \Theta(\log n)$ bits at once.

Consequences:

- Integer sort in $O\!\left(n \sqrt{\log \log n}\right)$ (Han–Thorup, 2002) — beats the comparison lower bound.
- Predecessor search in $O(\log w) = O(\log \log u)$ via van Emde Boas.
- Constant-time rank / select on bit vectors.

Invisible in pseudocode, legitimate in the model.

### 3.5 The word RAM in everyday analysis

For routine analysis: pretend each variable holds an arbitrary integer and each op is unit cost.

When you write
$$T_{\text{mergesort}}(n) = O(n \log n)$$
you implicitly mean: *under the word RAM with $w = \Omega(\log n)$, merge sort performs $O(n \log n)$ operations.*

The word RAM is the rigorous justification for that everyday practice.

## 4. Cost Criteria

### 4.1 Uniform cost

> Every instruction costs **one time step**, regardless of operand size. Memory access costs one step regardless of address.

This is the **unit-cost RAM** — the criterion used in essentially all undergraduate analysis.

Realistic when all numbers fit in a single machine word:

- Sorting integers up to $2^{64}$
- Traversing graphs with millions of nodes
- Multiplying matrices of doubles

### 4.2 Logarithmic cost

> Cost of an instruction = **bit length** of its operands.

\begin{align*}
\text{memory access at } a &\;\propto\; \lceil \log_2(a+1) \rceil \\
\text{arithmetic on } x,y &\;\propto\; \lceil \log_2(\max(|x|,|y|) + 1) \rceil
\end{align*}

Realistic for cryptographic primitives (2048-bit integers, etc.).

It also makes the RAM polynomially equivalent to the Turing machine even on instances with huge numbers.

### 4.3 The pragmatic compromise

For this document (and most courses):

- **Use** the uniform criterion.
- **Assume** every value fits in a constant number of words.
- **Verify** the assumption for algorithms whose numbers grow.

\vspace{0.5em}
\begin{alertblock}{When the assumption breaks}
Multiplying two 1024-bit RSA integers produces a 2048-bit result (32 words on a 64-bit machine). Each multiplication is no longer $O(1)$ — switch to bit-complexity analysis.
\end{alertblock}

## 5. Computational Equivalence

### 5.1 Polynomial-time equivalence

All of these define the **same** class $\mathbf{P}$:

- Multi-tape and single-tape Turing machines.
- RAM under logarithmic cost.
- RAM under uniform cost, with operands restricted to $O(\log n)$ bits.
- Word RAM with $w = O(\log n)$.
- Lambda calculus with explicit cost annotations.

Polynomial in one $\Rightarrow$ polynomial in all (at most polynomial blowup).

### 5.2 The Cobham–Edmonds thesis

> Polynomial time is the same across all reasonable models — and polynomial-time algorithms are precisely those we consider **tractable**.

\vspace{0.5em}

The computational analogue of the Church–Turing thesis.

Not a theorem — an empirical claim about what *"feasible computation"* means.

### 5.3 What this means for the practitioner

Day-to-day analysis: don't worry about the choice of model.

Big-O classifications, polynomial vs. exponential — these carry over.

\vspace{0.5em}

Exceptions where the model **does** matter:

| Situation | Use |
|---|---|
| Very large numbers (crypto, CAS) | logarithmic cost |
| I/O-dominated workloads | external memory model |
| Parallel algorithms | PRAM / work-span |

(All three covered in Part V.)

### Recap

\begin{itemize}
  \item A model fixes operations, costs, state — non-negotiable for rigor.
  \item The \textbf{Word RAM} with the \textbf{transdichotomous assumption} $w \ge \log_2 n$ is the model behind everyday analysis.
  \item Uniform cost is the default; switch to logarithmic when numbers grow.
  \item Reasonable models are polynomially equivalent — $\mathbf{P}$ is robust.
\end{itemize}

\vspace{0.5em}
Next: how to compare growth rates — \textbf{Part II, Asymptotic Analysis.}
