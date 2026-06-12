# Linked List — Theory Notes

---

## 1. Structure

```
Singly:   [val | next] → [val | next] → [val | None]
Doubly:   None ← [prev | val | next] ↔ [prev | val | next] → None
```

Each node is an independent heap allocation. There is **no** contiguous memory requirement.

| Operation | Singly LL | Doubly LL | Array |
|-----------|-----------|-----------|-------|
| Access index i | O(n) | O(n) | O(1) |
| Insert at head | O(1) | O(1) | O(n) |
| Insert at tail (with tail ptr) | O(1) | O(1) | O(1) amort. |
| Insert at position (node given) | O(1) | O(1) | O(n) |
| Delete (node given) | O(n)* | O(1) | O(n) |
| Search | O(n) | O(n) | O(n) |

*Singly LL delete with node reference requires finding predecessor: O(n).

---

## 2. Sentinel / Dummy Head

A dummy node before the real head eliminates special-casing for operations on the head.

```python
dummy = ListNode(0)
dummy.next = head
curr = dummy
# ... operate on curr.next ...
return dummy.next   # new head
```

**Why it works:** Every "real" node now has a predecessor. Insert/delete never need to check `if prev is None`.

---

## 3. Floyd's Cycle Detection

### Algorithm
```python
slow, fast = head, head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True   # cycle exists
return False
```

### Correctness Proof

Let `F` = distance from head to cycle entry, `C` = cycle length, `h` = distance from cycle entry to meeting point (inside cycle).

When `slow` enters the cycle, `fast` is already `F mod C` steps ahead in the cycle. After `k` more steps inside the cycle:
- `slow` is at position `k` (from cycle entry)
- `fast` is at position `F mod C + 2k` (from cycle entry)

They meet when positions are equal mod C:
```
k ≡ F mod C + 2k  (mod C)
0 ≡ F mod C + k   (mod C)
k ≡ -F ≡ C - (F mod C)  (mod C)
```
So they always meet within `C` steps of `slow` entering the cycle. ✓

### Finding Cycle Entry
After detection (slow == fast at some point inside cycle):
- Reset one pointer to head, keep the other at meeting point.
- Both advance one step at a time.
- They meet at the **cycle entry** after exactly `F` steps.

**Proof:** From meeting point, fast needs `C − h` steps to reach the entry (going around the remainder of the cycle, which is also `F mod C`). From head, it takes `F` steps. Both travel `F` steps and both arrive at the entry simultaneously. ✓

---

## 4. In-Place Reversal

**Invariant:** After processing node `curr`, the sublist from `prev` to the node `curr` points to has been reversed.

```python
prev, curr = None, head
while curr:
    next_node = curr.next   # save before unlinking
    curr.next = prev        # reverse pointer
    prev = curr             # advance prev
    curr = next_node        # advance curr
return prev                 # new head
```

Each node visited exactly once → O(n) time, O(1) space.

---

## 5. Fast & Slow for Middle

When `fast` reaches the end, `slow` is at the middle:
- Odd length n: slow at `(n-1)/2` (exact middle).
- Even length n: slow at `n/2 - 1` (first of two middles) or `n/2` depending on init.

---

## 6. Key Patterns

| Pattern | Technique | Example |
|---------|-----------|---------|
| Middle of list | fast/slow pointers | Reorder list |
| Nth from end | two pointers, n apart | Remove nth from end |
| Cycle detection | Floyd's | Linked List Cycle |
| Cycle entry | Floyd's + reset | Find Duplicate Number |
| Reverse sublist | three-pointer | Reverse k-group |
| Merge sorted | compare heads | Merge k sorted lists |
| Deep copy | hashmap old→new | Copy with random pointer |

---

## 7. LRU Cache Implementation

Use a **doubly linked list** + **hash map**:
- Hash map: `key → node` for O(1) lookup.
- DLL: maintains recency order. Most recent at head, least recent at tail.
- `get(key)`: find node → move to head → O(1).
- `put(key, val)`: if exists, update + move to head. If new, insert at head; if over capacity, remove tail. Both O(1).

---

## 8. Pitfalls
- **Losing the next pointer:** always save `curr.next` before changing `curr.next`.
- **Off-by-one in k-group reversal:** carefully count nodes before committing to a reversal.
- **Null checks:** `fast.next.next` requires both `fast` and `fast.next` to be non-null.
