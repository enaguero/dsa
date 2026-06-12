# 2-D Dynamic Programming

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### When 2-D State Is Needed
- [ ] The problem depends on *two* changing quantities: (index in string 1, index in string 2), (row, col), (item, capacity), etc.
- [ ] `dp[i][j]` encodes the answer for the subproblem defined by those two indices

### Grid DP
- [ ] `dp[i][j]` = answer for cell (i, j) using cells above and to the left
- [ ] Base cases: first row and first column
- [ ] Examples: unique paths, minimum path sum

### String DP
- [ ] **LCS (Longest Common Subsequence)**: `dp[i][j]` = LCS of s1[:i] and s2[:j]
  - Match: `dp[i][j] = dp[i-1][j-1] + 1`
  - No match: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`
- [ ] **Edit Distance**: insert/delete/replace; recurrence covers all three operations
- [ ] **Distinct Subsequences**, **Interleaving String**: 2-D DP on two string prefixes

### Other Patterns
- [ ] **Buy & Sell with Cooldown**: state machine — held, sold, rest
- [ ] **Coin Change II**: 2-D knapsack (coin index × amount); inner loop is the amount
- [ ] **Burst Balloons**: interval DP — `dp[l][r]` = max coins for balloons in (l, r)
- [ ] **Regular Expression Matching**: 2-D on (string index, pattern index)

### Space Optimization
- [ ] Many 2-D DPs only need the previous row → compress to O(n) space
- [ ] Be careful of traversal direction when compressing

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Medium | [Unique Paths](https://leetcode.com/problems/unique-paths/) | `exercises/unique-paths.py` |
| [ ] | Medium | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | `exercises/longest-common-subsequence.py` |
| [ ] | Medium | [Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) | `exercises/best-time-to-buy-and-sell-stock-with-cooldown.py` |
| [ ] | Medium | [Coin Change II](https://leetcode.com/problems/coin-change-ii/) | `exercises/coin-change-ii.py` |
| [ ] | Medium | [Target Sum](https://leetcode.com/problems/target-sum/) | `exercises/target-sum.py` |
| [ ] | Medium | [Interleaving String](https://leetcode.com/problems/interleaving-string/) | `exercises/interleaving-string.py` |
| [ ] | Medium | [Edit Distance](https://leetcode.com/problems/edit-distance/) | `exercises/edit-distance.py` |
| [ ] | Hard   | [Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | `exercises/longest-increasing-path-in-a-matrix.py` |
| [ ] | Hard   | [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) | `exercises/distinct-subsequences.py` |
| [ ] | Hard   | [Burst Balloons](https://leetcode.com/problems/burst-balloons/) | `exercises/burst-balloons.py` |
| [ ] | Hard   | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | `exercises/regular-expression-matching.py` |
