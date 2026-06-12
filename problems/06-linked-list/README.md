# Linked List

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Structure
- [ ] Node: value + pointer to next (singly) or next+prev (doubly)
- [ ] No random access — traversal is O(n); insertion/deletion at a known node is O(1)
- [ ] Head pointer is the entry point; tail.next = None (singly) or None (doubly)

### Sentinel / Dummy Head
- [ ] A dummy node before the real head simplifies edge cases (empty list, removing head)
- [ ] Return `dummy.next` as the new head

### Fast & Slow Pointers
- [ ] Floyd's cycle detection: fast moves 2 steps, slow moves 1
- [ ] If they meet → cycle exists; meeting point used to find cycle entry
- [ ] Find middle of list: when fast reaches end, slow is at middle

### In-Place Reversal
- [ ] Track `prev`, `curr`, `next_node`; relink one node at a time
- [ ] Useful as a building block: reverse a segment, reverse k-groups

### Common Patterns
- [ ] Merge two sorted lists: compare heads, attach smaller, recurse/iterate
- [ ] Remove nth from end: two-pointer with n-step head start
- [ ] Copy list with random pointer: interleave copy nodes or use hash map

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | `exercises/reverse-linked-list.py` |
| [ ] | Easy   | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | `exercises/merge-two-sorted-lists.py` |
| [ ] | Easy   | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | `exercises/linked-list-cycle.py` |
| [ ] | Medium | [Reorder List](https://leetcode.com/problems/reorder-list/) | `exercises/reorder-list.py` |
| [ ] | Medium | [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | `exercises/remove-nth-node-from-end-of-list.py` |
| [ ] | Medium | [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | `exercises/copy-list-with-random-pointer.py` |
| [ ] | Medium | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | `exercises/add-two-numbers.py` |
| [ ] | Medium | [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) | `exercises/find-the-duplicate-number.py` |
| [ ] | Medium | [LRU Cache](https://leetcode.com/problems/lru-cache/) | `exercises/lru-cache.py` |
| [ ] | Hard   | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | `exercises/merge-k-sorted-lists.py` |
| [ ] | Hard   | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | `exercises/reverse-nodes-in-k-group.py` |
