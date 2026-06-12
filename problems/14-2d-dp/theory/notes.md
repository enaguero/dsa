# 2-D Dynamic Programming — Theory Notes

---

## 1. When Is a 2-D State Needed?

A 2-D DP table `dp[i][j]` is appropriate when the problem has **two independent parameters** that both change as we build the solution:
- Two string indices (i in s1, j in s2).
- A grid position (row i, column j).
- An item index and a remaining capacity (knapsack).
- A left and right endpoint of an interval.

---

## 2. Edit Distance (Levenshtein Distance)

**Problem:** Minimum number of insertions, deletions, or substitutions to transform `s` into `t`.

**State:** `dp[i][j]` = edit distance between `s[0..i-1]` and `t[0..j-1]`.

**Recurrence:**
```
if s[i-1] == t[j-1]:
    dp[i][j] = dp[i-1][j-1]                          # no operation needed
else:
    dp[i][j] = 1 + min(
        dp[i-1][j],     # delete from s (or insert into t)
        dp[i][j-1],     # insert into s (or delete from t)
        dp[i-1][j-1]    # substitute
    )
```

**Base cases:** `dp[i][0] = i` (delete i chars from s), `dp[0][j] = j` (insert j chars).

**Derivation of correctness:** Consider the last operation applied:
- If it's a substitution at position (i, j): cost 1 + optimal cost for (i-1, j-1).
- If it's a deletion: cost 1 + optimal cost for (i-1, j).
- If it's an insertion: cost 1 + optimal cost for (i, j-1).
The minimum over these three is optimal (optimal substructure). ✓

**Complexity:** O(m·n) time, O(m·n) space → O(n) space with rolling row.

---

## 3. Longest Common Subsequence (LCS)

**State:** `dp[i][j]` = LCS length of `s1[0..i-1]` and `s2[0..j-1]`.

**Recurrence:**
```
if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**Relationship to Edit Distance:** Edit distance = m + n − 2·LCS(s, t) when only insertions and deletions are allowed (no substitutions).

---

## 4. Grid DP (Unique Paths)

**State:** `dp[i][j]` = number of ways to reach cell (i, j) from (0, 0) moving only right or down.

**Recurrence:** `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.

**Base cases:** `dp[0][j] = dp[i][0] = 1` (only one way to travel along edges).

**Closed form:** `C(m+n-2, m-1)` — choose which m−1 of the m+n−2 steps are "down".

---

## 5. Interval DP (Burst Balloons)

**State:** `dp[l][r]` = maximum coins obtainable by bursting all balloons in `(l, r)` exclusive.

**Key insight:** Instead of thinking about which balloon to burst **first**, think about which to burst **last** in the interval. If balloon `k` is the last in `(l, r)` to be burst:
```
dp[l][r] = max over k in (l, r):
    dp[l][k] + nums[l]*nums[k]*nums[r] + dp[k][r]
```

Fill in order of increasing interval length. O(n³) time.

---

## 6. State Machine DP (Buy & Sell with Cooldown)

States: `held` (holding stock), `sold` (just sold, in cooldown), `rest` (not holding, not cooling down).

```
held[i]  = max(held[i-1], rest[i-1] - prices[i])   # keep or buy
sold[i]  = held[i-1] + prices[i]                     # sell
rest[i]  = max(rest[i-1], sold[i-1])                 # do nothing or exit cooldown
```

Answer: `max(sold[n-1], rest[n-1])`.

---

## 7. Space Optimisation for 2-D DP

When `dp[i][j]` depends only on the previous row (`dp[i-1][...]`), compress to a 1-D array.

```python
# Before (O(m*n))
dp = [[0]*(n+1) for _ in range(m+1)]

# After (O(n))
dp = [0] * (n+1)
for i in range(1, m+1):
    new_dp = [0] * (n+1)
    for j in range(1, n+1):
        new_dp[j] = f(dp[j], dp[j-1], new_dp[j-1])
    dp = new_dp
```

**Caveat for 0/1 knapsack:** iterate `j` in reverse to avoid using the same item twice.

---

## 8. Complexity Summary

| Problem | State | Time | Space (optimised) |
|---------|-------|------|-------------------|
| Unique Paths | O(m·n) | O(m·n) | O(n) |
| LCS | O(m·n) | O(m·n) | O(n) |
| Edit Distance | O(m·n) | O(m·n) | O(n) |
| Coin Change II | O(n·W) | O(n·W) | O(W) |
| Target Sum | O(n·S) | O(n·S) | O(S) |
| Interleaving String | O(m·n) | O(m·n) | O(n) |
| Burst Balloons | O(n²) | O(n³) | O(n²) |
| Regex Matching | O(m·n) | O(m·n) | O(n) |

---

## 9. Pitfalls
- **Fill order matters:** ensure that when computing `dp[i][j]`, the values it depends on are already filled. Traverse in increasing i and j for most grid/string problems.
- **Interval DP fill order:** fill by increasing interval length `(r - l)`, not by row.
- **Off-by-one in base cases:** `dp[0][0]` often has a special meaning (empty prefix). Explicitly set all base cases before the main loop.
- **Integer overflow in counting problems:** Python handles big ints natively, but be careful in other languages.
