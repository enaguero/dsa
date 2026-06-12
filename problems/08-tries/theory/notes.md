# Tries — Theory Notes

---

## 1. Formal Definition

A **Trie** (prefix tree / radix tree) is a rooted tree where:
- Each node represents a **prefix** of some stored key.
- Each edge is labelled with a character.
- Each node stores: `children: dict[char, TrieNode]` and `is_end: bool`.
- The root represents the empty prefix `""`.

A word `w` is stored iff the path spelling `w` from root exists and the last node has `is_end = True`.

---

## 2. Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}   # char -> TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

---

## 3. Complexity Analysis

Let `m` = word length, `n` = number of words, `Σ` = alphabet size (e.g., 26 for lowercase).

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(m) | O(m) per word |
| Search | O(m) | O(1) |
| StartsWith | O(m) | O(1) |
| Total space | — | O(Σ · m · n) worst case |

**Space derivation (worst case):** If all `n` words share no prefixes, each word creates `m` new nodes, each with up to `Σ` children pointers. Total nodes = `n · m`. Total pointers = `n · m · Σ`. In practice, shared prefixes reduce this significantly.

**Space derivation (best case):** All words are the same → `m` nodes total, O(m · Σ) space.

---

## 4. Trie vs Hash Set for Word Lookup

| Metric | Trie | Hash Set |
|--------|------|----------|
| Search time | O(m) | O(m) to hash |
| Prefix search | O(m) — native | O(n · m) — scan all |
| Space | O(Σ · m · n) | O(m · n) |
| Construction | O(m · n) | O(m · n) |

**Trie wins:** prefix queries (autocomplete, startsWith), longest common prefix, word frequency with shared prefixes.
**Hash set wins:** exact lookup only, smaller memory footprint.

---

## 5. Wildcard Search (DFS on Trie)

For patterns with `.` (match any char):

```python
def search(self, word: str) -> bool:
    def dfs(j, node):
        for i in range(j, len(word)):
            ch = word[i]
            if ch == '.':
                return any(dfs(i + 1, child) for child in node.children.values())
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end
    return dfs(0, self.root)
```

**Complexity:** O(Σ^(number of dots) · m) in the worst case — each dot branches to all children.

---

## 6. Word Search II (Trie + DFS on Grid)

Build a trie from the word list. DFS from every grid cell, navigating the trie simultaneously. Prune when the current grid path is not a trie prefix. Remove completed words from the trie to avoid revisiting.

**Time:** O(m · n · 4 · 3^(L−1)) where m×n is grid size and L is max word length. Pruning makes this much better in practice.

---

## 7. Pitfalls
- **`is_end` flag:** don't just mark leaves. A word can be a prefix of another word — `is_end` distinguishes them.
- **Memory:** for large alphabets or long words, tries can be much more memory-intensive than hash sets.
- **Dict vs array children:** `dict` is flexible; a fixed array of size 26 is faster for lowercase-only inputs (`children = [None] * 26`, index by `ord(ch) - ord('a')`).
