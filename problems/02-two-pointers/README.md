# Two Pointers

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Core Idea
- [ ] Two indices that move toward each other (opposite ends) or in the same direction
- [ ] Eliminates a nested loop: reduces O(n²) brute force to O(n)

### Opposite-End Pattern
- [ ] Start left=0, right=n-1; advance based on a comparison condition
- [ ] Works on sorted arrays (pair sum, container with most water)
- [ ] Palindrome check: compare chars while left < right

### Same-Direction Pattern
- [ ] Both pointers move forward but at different speeds or conditions
- [ ] Used for: removing duplicates in-place, partitioning arrays
- [ ] Fast & slow pointer (cycle detection) — covered more in Linked List

### When to Apply
- [ ] Problem involves pairs/triplets in a sorted (or sortable) array
- [ ] Need to find a subarray/substring satisfying a condition → consider sliding window instead

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | `exercises/valid-palindrome.py` |
| [ ] | Medium | [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | `exercises/two-sum-ii-input-array-is-sorted.py` |
| [ ] | Medium | [3Sum](https://leetcode.com/problems/3sum/) | `exercises/3sum.py` |
| [ ] | Medium | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | `exercises/container-with-most-water.py` |
| [ ] | Hard   | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | `exercises/trapping-rain-water.py` |
