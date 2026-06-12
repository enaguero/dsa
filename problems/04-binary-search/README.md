# Binary Search

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Classic Binary Search
- [ ] Precondition: search space is sorted (or monotone)
- [ ] Loop invariant: answer is always in [left, right]
- [ ] `mid = left + (right - left) // 2` to avoid integer overflow
- [ ] O(log n) — halves the search space each iteration

### Boundary Variants
- [ ] **Left boundary**: find first index where condition is true
  - When `condition(mid)` is true, `right = mid` (don't exclude mid)
- [ ] **Right boundary**: find last index where condition is true
  - When `condition(mid)` is true, `left = mid` (don't exclude mid)
- [ ] Off-by-one errors: carefully choose `< ` vs `<=` and how you update left/right

### Searching on the Answer Space
- [ ] Instead of searching an array, binary search on possible *answers*
- [ ] Define a feasibility function `can_do(x)` that is monotone
- [ ] Examples: "minimum capacity", "minimum days", "koko eating bananas"

### Rotated Sorted Array
- [ ] One half is always sorted — use that to determine which half to search

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Binary Search](https://leetcode.com/problems/binary-search/) | `exercises/binary-search.py` |
| [ ] | Medium | [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | `exercises/search-a-2d-matrix.py` |
| [ ] | Medium | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | `exercises/koko-eating-bananas.py` |
| [ ] | Medium | [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | `exercises/find-minimum-in-rotated-sorted-array.py` |
| [ ] | Medium | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | `exercises/search-in-rotated-sorted-array.py` |
| [ ] | Medium | [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) | `exercises/time-based-key-value-store.py` |
| [ ] | Hard   | [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | `exercises/median-of-two-sorted-arrays.py` |
