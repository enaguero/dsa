# 1-D Dynamic Programming — Theory Notes

---

## 1. What Makes a Problem Suitable for DP?

### Optimal Substructure
A problem has optimal substructure if an optimal solution to the problem contains optimal solutions to subproblems.

**Formal statement:** Let OPT(n) be the optimal solution to the problem of size n. OPT(n) can be expressed as a function of OPT(k) for k < n.

**Counterexample (no optimal substructure):** Longest simple path in a graph — the longest path from s to t may go through u, but the longest path from s to u may conflict with the path from u to t (they share vertices). Shortest path has optimal substructure; longest simple path does not.

### Overlapping Subproblems
The same subproblems recur multiple times. If all subproblems are distinct (no overlap), divide-and-conquer is more appropriate.

**Example:** Fibonacci without memoisation computes fib(2) exponentially many times. With a cache: each subproblem solved once.

---

## 2. Approaches

### Top-Down (Memoisation)
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def dp(i):
    # base case
    if i <= 1: return i
    return dp(i - 1) + dp(i - 2)
```
- Natural to write (follows the recurrence directly).
- Only computes needed subproblems (lazy evaluation).
- Space: O(n) cache + O(n) call stack.

### Bottom-Up (Tabulation)
```python
dp = [0] * (n + 1)
dp[0], dp[1] = 0, 1
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
```
- Iterative: no stack overflow risk.
- Often faster (no function call overhead).
- Space: can often be optimised to O(1) when only recent states needed.

---

## 3. Complexity Formula

```
Time  = (number of distinct states) × (transition cost per state)
Space = (number of states stored simultaneously)
```

For 1-D DP: states = O(n), transition = O(1) typically → **O(n) time, O(n) space** (or O(1) with rolling array).

---

## 4. Common Patterns with Recurrences

### Linear Sequence
`dp[i] = f(dp[i-1], dp[i-2], …)`

**Climbing stairs:** `dp[i] = dp[i-1] + dp[i-2]`. (How many ways to reach step i.)
**Min cost climbing stairs:** `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`.

### Decision at Each Step (House Robber)
At each house, choose: rob (can't rob i-1) or skip.
```
dp[i] = max(dp[i-1],          # skip house i
            dp[i-2] + nums[i]) # rob house i
```
Space-optimised: keep only `prev2, prev1`.

**Proof of optimal substructure:** Any optimal solution either includes house i or doesn't. If it includes i, it must optimally solve the subproblem for houses 0..i−2. If it doesn't, it solves 0..i−1. Both are subproblems. ✓

### Unbounded Knapsack (Coin Change)
Each coin can be used any number of times.
```
dp[amount] = min_{coin in coins} (dp[amount - coin] + 1)
```
Fill from 0 to target. O(target × len(coins)) time.

### 0/1 Knapsack (Partition Equal Subset Sum)
Each item used at most once.
```
dp[i][w] = dp[i-1][w]                                  # don't take item i
            or dp[i-1][w - weight[i]] + value[i]        # take item i
```
Space-optimised to 1-D by iterating `w` in reverse (to prevent using the same item twice).

### LIS (Longest Increasing Subsequence)

**O(n²) DP:** `dp[i] = max(dp[j] + 1 for j < i if nums[j] < nums[i])`.

**O(n log n) with patience sort:** Maintain a list `tails` where `tails[k]` = smallest tail of all increasing subsequences of length k+1. Binary search to find where to place each element.

---

## 5. Palindrome DP

**Expand Around Centre:** For each centre (n centres for odd-length, n-1 for even-length), expand while characters match. O(n²) total.

**DP table:** `is_palindrome[i][j] = (s[i]==s[j]) and is_palindrome[i+1][j-1]`. Fill in order of increasing length. O(n²) time and space.

---

## 6. Decode Ways (DP on Prefixes)

`dp[i]` = number of ways to decode `s[0..i-1]`.

```
dp[i] += dp[i-1]  if s[i-1] != '0'         (single digit decode)
dp[i] += dp[i-2]  if 10 ≤ int(s[i-2:i]) ≤ 26  (two-digit decode)
```

Base: `dp[0] = 1` (empty string), `dp[1] = 1 if s[0] != '0' else 0`.

---

## 7. Space Optimisation

When `dp[i]` depends only on `dp[i-1]` (and `dp[i-2]`):
```python
# Instead of dp = [0] * n
prev2, prev1 = base_case_0, base_case_1
for i in range(2, n):
    curr = f(prev1, prev2)
    prev2, prev1 = prev1, curr
```
Reduces space from O(n) to **O(1)**.

---

## 8. Pitfalls
- **Base cases:** off-by-one errors in base cases propagate through the whole table. Verify with small examples.
- **State definition ambiguity:** `dp[i]` = "answer including i" vs "answer up to but not including i" — be explicit and consistent.
- **Coin change: initialise dp[0]=0, dp[1..] = ∞ (not found yet).** Return `-1` if `dp[target] == ∞`.
- **Memoisation with mutable arguments:** `@lru_cache` requires hashable arguments; convert lists to tuples.
