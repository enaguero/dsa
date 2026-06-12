# Tries

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Structure
- [ ] Each node holds a map of children (char → TrieNode) and an `is_end` flag
- [ ] Root node is empty; each path from root to an `is_end` node spells a word
- [ ] Space: O(alphabet_size × average_word_length × number_of_words)

### Core Operations
- [ ] **Insert**: walk (and create) nodes for each character, set `is_end = True` at last node — O(n)
- [ ] **Search**: walk nodes for each character; return True only if `is_end` at last node — O(n)
- [ ] **StartsWith**: same as search but don't require `is_end` — O(n)

### Why a Trie over a Hash Set
- [ ] O(n) vs O(n) lookup, but trie enables *prefix* queries efficiently
- [ ] Common use: autocomplete, spell checker, IP routing, word dictionaries with wildcards

### Wildcard / DFS on Trie
- [ ] `.` wildcard: branch into all children at that level (DFS/BFS)
- [ ] Prune early if a branch can't possibly match

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Medium | [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | `exercises/implement-trie-prefix-tree.py` |
| [ ] | Medium | [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | `exercises/design-add-and-search-words-data-structure.py` |
| [ ] | Hard   | [Word Search II](https://leetcode.com/problems/word-search-ii/) | `exercises/word-search-ii.py` |
