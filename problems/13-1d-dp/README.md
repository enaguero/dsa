# 1-D Dynamic Programming

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Prerequisites
- [ ] **Overlapping subproblems**: the same subproblem is solved multiple times in naive recursion
- [ ] **Optimal substructure**: the optimal solution is built from optimal solutions of subproblems

### Approaches
- [ ] **Top-down (memoization)**: recursive + a cache (dict or array); natural to write, O(n) time & space
- [ ] **Bottom-up (tabulation)**: fill a DP array iteratively from base cases; often more space-efficient
- [ ] **Space optimization**: when `dp[i]` only depends on `dp[i-1]` (and maybe `dp[i-2]`), use variables instead of an array

### How to Design a DP Solution
1. Define the state: what does `dp[i]` represent?
2. Write the recurrence: how does `dp[i]` relate to smaller states?
3. Identify base cases
4. Determine evaluation order (usually left to right)

### Common Patterns
- [ ] **Linear sequence**: Fibonacci, climbing stairs, min cost climbing stairs
- [ ] **Decision at each step**: house robber — take or skip, can't take adjacent
- [ ] **Unbounded knapsack**: coin change — reuse items; inner loop over coins
- [ ] **0/1 knapsack**: partition equal subset — each item used at most once
- [ ] **LIS (Longest Increasing Subsequence)**: O(n²) DP or O(n log n) with patience sort
- [ ] **String DP**: decode ways, word break — DP on prefixes

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | `exercises/climbing-stairs.py` |
| [ ] | Easy   | [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) | `exercises/min-cost-climbing-stairs.py` |
| [ ] | Medium | [House Robber](https://leetcode.com/problems/house-robber/) | `exercises/house-robber.py` |
| [ ] | Medium | [House Robber II](https://leetcode.com/problems/house-robber-ii/) | `exercises/house-robber-ii.py` |
| [ ] | Medium | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | `exercises/longest-palindromic-substring.py` |
| [ ] | Medium | [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) | `exercises/palindromic-substrings.py` |
| [ ] | Medium | [Decode Ways](https://leetcode.com/problems/decode-ways/) | `exercises/decode-ways.py` |
| [ ] | Medium | [Coin Change](https://leetcode.com/problems/coin-change/) | `exercises/coin-change.py` |
| [ ] | Medium | [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | `exercises/maximum-product-subarray.py` |
| [ ] | Medium | [Word Break](https://leetcode.com/problems/word-break/) | `exercises/word-break.py` |
| [ ] | Medium | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | `exercises/longest-increasing-subsequence.py` |
| [ ] | Medium | [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | `exercises/partition-equal-subset-sum.py` |
