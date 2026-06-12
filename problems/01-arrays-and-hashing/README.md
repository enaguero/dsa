# Arrays & Hashing

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Arrays
- [ ] Static vs dynamic arrays — memory layout, contiguous allocation
- [ ] Indexing in O(1), insertion/deletion at end O(1) amortized, middle O(n)
- [ ] Cache locality advantage over linked structures

### Hash Tables
- [ ] Hash function: maps a key to a bucket index
- [ ] Collision strategies: chaining (linked list per bucket) vs open addressing (linear/quadratic probing)
- [ ] Load factor and rehashing — why average O(1) can degrade to O(n)
- [ ] Hash sets vs hash maps

### Key Patterns
- [ ] Frequency counting with a hash map
- [ ] Grouping by a canonical key (e.g., sorted word → anagram group)
- [ ] Using a set for O(1) membership checks instead of O(n) list scans
- [ ] Prefix sums for range queries

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | `exercises/contains-duplicate.py` |
| [ ] | Easy   | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | `exercises/valid-anagram.py` |
| [ ] | Easy   | [Two Sum](https://leetcode.com/problems/two-sum/) | `exercises/two-sum.py` |
| [ ] | Medium | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | `exercises/group-anagrams.py` |
| [ ] | Medium | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | `exercises/top-k-frequent-elements.py` |
| [ ] | Medium | [Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/) | `exercises/encode-and-decode-strings.py` |
| [ ] | Medium | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | `exercises/product-of-array-except-self.py` |
| [ ] | Medium | [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | `exercises/valid-sudoku.py` |
| [ ] | Medium | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | `exercises/longest-consecutive-sequence.py` |
