# Heap / Priority Queue — Theory Notes

---

## 1. Formal Definition

A **binary heap** is a complete binary tree satisfying the **heap property**:
- **Min-heap:** `key(parent) ≤ key(child)` for all nodes.
- **Max-heap:** `key(parent) ≥ key(child)` for all nodes.

"Complete binary tree" means all levels are full except possibly the last, filled left-to-right. This allows compact array storage.

---

## 2. Array Representation

For a node at index `i` (0-indexed):
```
parent(i)      = (i - 1) // 2
left_child(i)  = 2 * i + 1
right_child(i) = 2 * i + 2
```

The root is at index 0. A complete binary tree of `n` nodes has height `⌊log₂ n⌋`.

---

## 3. Core Operations

### Sift Up — O(log n)
After inserting at the end, restore heap property by swapping with parent until heap property holds.

```python
def _sift_up(self, i):
    while i > 0:
        parent = (i - 1) // 2
        if self.heap[parent] > self.heap[i]:   # min-heap
            self.heap[parent], self.heap[i] = self.heap[i], self.heap[parent]
            i = parent
        else:
            break
```
At most `h = ⌊log₂ n⌋` swaps → O(log n). ✓

### Sift Down — O(log n)
After replacing root with last element (during pop), restore heap property downward.

```python
def _sift_down(self, i):
    n = len(self.heap)
    while True:
        smallest = i
        l, r = 2*i+1, 2*i+2
        if l < n and self.heap[l] < self.heap[smallest]: smallest = l
        if r < n and self.heap[r] < self.heap[smallest]: smallest = r
        if smallest == i: break
        self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
        i = smallest
```
At most `h` swaps → O(log n). ✓

---

## 4. Build Heap — O(n) Proof

Naïve approach: insert n elements one by one → O(n log n).

**Optimal (Floyd's algorithm):** Start from the last non-leaf node `⌊n/2⌋ − 1` and sift down each node.

**Why O(n)?**

Let `h = ⌊log₂ n⌋`. Nodes at height `k` from the bottom: at most `⌈n / 2^(k+1)⌉`. Sift-down cost for a node at height `k` = O(k).

Total cost:
```
∑_{k=0}^{h} ⌈n / 2^(k+1)⌉ · k
≤ n · ∑_{k=0}^{∞} k / 2^(k+1)
= n · ∑_{k=0}^{∞} k / 2^(k+1)
```

Using the identity `∑_{k=0}^{∞} k · x^k = x / (1−x)²` for `|x| < 1`, set `x = 1/2`:
```
∑_{k=0}^{∞} k / 2^k = (1/2) / (1/2)² = 2
∑_{k=0}^{∞} k / 2^(k+1) = 1
```

Total cost ≤ n · 1 = **O(n)**. ✓

---

## 5. Operation Summary

| Operation | Time | Notes |
|-----------|------|-------|
| peek (find min/max) | O(1) | Root element |
| push | O(log n) | Append + sift up |
| pop | O(log n) | Swap root with last, sift down |
| build from array | O(n) | Floyd's algorithm |
| arbitrary delete | O(log n) | Swap with last, sift up or down |

---

## 6. Python `heapq`

Python only provides a **min-heap**. For max-heap, negate values.

```python
import heapq

h = []
heapq.heappush(h, 3)
heapq.heappush(h, 1)
min_val = h[0]          # peek: O(1)
heapq.heappop(h)        # pop min: O(log n)
heapq.heapify(lst)      # in-place: O(n)

# Max-heap: negate
heapq.heappush(h, -val)
max_val = -h[0]
```

For objects: push tuples `(priority, item)`. Python compares tuple elements lexicographically.

---

## 7. Key Patterns

### Top-K Elements
Maintain a size-k min-heap. For each element, push it; if size > k, pop (removing the smallest). After processing all n elements, the heap contains the k largest. O(n log k) time, O(k) space.

### K-th Largest
Same as Top-K: size-k min-heap's root is the k-th largest.

### Two-Heap for Median
- Max-heap `lo` for lower half, min-heap `hi` for upper half.
- Invariant: `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`.
- Median: `lo[0]` if sizes unequal, or `(lo[0] + hi[0]) / 2` if equal.
- Add element: push to `lo` then rebalance. O(log n) per operation.

### Merge K Sorted Lists
Push `(val, list_index, node)` for each list's head. Pop min, push next node of that list. O(N log k) where N = total elements.

---

## 8. Pitfalls
- **Stability:** Python's `heapq` is not stable. Add a counter as tiebreaker: `(priority, counter, item)`.
- **Mutation:** don't modify elements already in the heap — the heap won't re-heapify. Use `heapq.heapreplace()` or rebuild.
- **`heapq.nlargest(k, arr)`** is O(n log k) — faster than sorting for small k. For large k, sort instead.
