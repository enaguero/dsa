# Backtracking

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Core Model
- [ ] Build a solution incrementally via a **decision tree**: at each step, choose among valid options
- [ ] If a path violates constraints or can't lead to a solution → **prune** (backtrack immediately)
- [ ] Undo the last choice after recursing (restore state) so the next branch starts clean

### General Template
```
def backtrack(state, choices):
    if is_solution(state):
        results.append(copy of state)
        return
    for choice in choices:
        if is_valid(choice, state):
            make_choice(state, choice)
            backtrack(state, remaining_choices)
            undo_choice(state, choice)
```

### Problem Categories
- [ ] **Subsets**: include or exclude each element; 2ⁿ subsets total
- [ ] **Permutations**: all orderings; n! total; track a `used` array
- [ ] **Combinations**: choose k from n; use a start index to avoid reuse
- [ ] **Duplicates**: sort first, then skip duplicate elements at the same level
- [ ] **Board problems** (Sudoku, N-Queens): prune by row/column/box constraints

### Complexity
- [ ] Worst case is exponential, but pruning makes it much faster in practice
- [ ] Justify O(n! ) for permutations, O(2ⁿ) for subsets

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Medium | [Subsets](https://leetcode.com/problems/subsets/) | `exercises/subsets.py` |
| [ ] | Medium | [Combination Sum](https://leetcode.com/problems/combination-sum/) | `exercises/combination-sum.py` |
| [ ] | Medium | [Permutations](https://leetcode.com/problems/permutations/) | `exercises/permutations.py` |
| [ ] | Medium | [Subsets II](https://leetcode.com/problems/subsets-ii/) | `exercises/subsets-ii.py` |
| [ ] | Medium | [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | `exercises/combination-sum-ii.py` |
| [ ] | Medium | [Word Search](https://leetcode.com/problems/word-search/) | `exercises/word-search.py` |
| [ ] | Medium | [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | `exercises/palindrome-partitioning.py` |
| [ ] | Medium | [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | `exercises/letter-combinations-of-a-phone-number.py` |
| [ ] | Hard   | [N-Queens](https://leetcode.com/problems/n-queens/) | `exercises/n-queens.py` |
