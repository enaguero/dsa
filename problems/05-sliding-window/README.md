# Sliding Window

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Core Idea
- [ ] Maintain a window [left, right] over a sequence; slide it to avoid recomputation
- [ ] Amortizes cost: each element enters and leaves the window at most once → O(n)

### Fixed-Size Window
- [ ] Window size k is given; advance both pointers together
- [ ] Useful for: max/min subarray of size k, moving averages

### Variable-Size Window
- [ ] Expand right until the window is invalid, then shrink from left
- [ ] Or expand until the window is valid, record result, then shrink
- [ ] Maintain window state with a hash map or counter

### Common Window State to Track
- [ ] Character frequencies (for substring/anagram problems)
- [ ] Running sum or product
- [ ] Count of distinct elements

### When to Apply
- [ ] "Longest/shortest subarray/substring with property X"
- [ ] The property is monotone: adding elements can only make it better (or worse), removing restores it

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | `exercises/best-time-to-buy-and-sell-stock.py` |
| [ ] | Medium | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | `exercises/longest-substring-without-repeating-characters.py` |
| [ ] | Medium | [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | `exercises/longest-repeating-character-replacement.py` |
| [ ] | Medium | [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | `exercises/permutation-in-string.py` |
| [ ] | Hard   | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | `exercises/minimum-window-substring.py` |
| [ ] | Hard   | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | `exercises/sliding-window-maximum.py` |
