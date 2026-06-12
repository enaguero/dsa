# Greedy

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Greedy Choice Property
- [ ] At each step, pick the locally optimal choice; prove it leads to a globally optimal solution
- [ ] **Exchange argument**: assume an optimal solution doesn't use the greedy choice; swap it in and show the result is no worse
- [ ] Greedy does NOT always work — know when DP is needed instead

### When Greedy Works
- [ ] The problem has optimal substructure AND making the greedy choice never blocks a better future option
- [ ] Sorting often enables the greedy choice (e.g., sort by end time for interval scheduling)

### Common Patterns
- [ ] **Interval scheduling / activity selection**: sort by end time, always pick earliest-ending non-overlapping interval
- [ ] **Jump game**: track the farthest reachable index; if current index > farthest → can't proceed
- [ ] **Gas station**: total gas ≥ total cost → solution exists; find starting point by tracking running surplus
- [ ] **Kadane's algorithm (max subarray)**: reset running sum to 0 when it goes negative
- [ ] **Hand of Straights / Merge Triplets**: sort, then greedily match

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Medium | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | `exercises/maximum-subarray.py` |
| [ ] | Medium | [Jump Game](https://leetcode.com/problems/jump-game/) | `exercises/jump-game.py` |
| [ ] | Medium | [Jump Game II](https://leetcode.com/problems/jump-game-ii/) | `exercises/jump-game-ii.py` |
| [ ] | Medium | [Gas Station](https://leetcode.com/problems/gas-station/) | `exercises/gas-station.py` |
| [ ] | Medium | [Hand of Straights](https://leetcode.com/problems/hand-of-straights/) | `exercises/hand-of-straights.py` |
| [ ] | Medium | [Merge Triplets to Form Target Triplet](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/) | `exercises/merge-triplets-to-form-target-triplet.py` |
| [ ] | Medium | [Partition Labels](https://leetcode.com/problems/partition-labels/) | `exercises/partition-labels.py` |
| [ ] | Medium | [Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/) | `exercises/valid-parenthesis-string.py` |
