# Heap / Priority Queue

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Binary Heap
- [ ] Complete binary tree stored as an array: children of index i are at 2i+1 and 2i+2
- [ ] **Min-heap**: parent ≤ children; root is always the minimum
- [ ] **Max-heap**: parent ≥ children; root is always the maximum
- [ ] Push: append + sift up — O(log n)
- [ ] Pop: swap root with last, remove last, sift down — O(log n)
- [ ] Peek (min/max): O(1)
- [ ] Build heap from array: O(n) via bottom-up heapify

### Python `heapq`
- [ ] `heapq` is a min-heap; negate values for max-heap behavior
- [ ] `heappush(h, x)`, `heappop(h)`, `h[0]` for peek
- [ ] `heapify(list)` in-place in O(n)

### Key Patterns
- [ ] **Top-K elements**: push all, pop K times — O(n log k) with a size-k heap
- [ ] **K-th largest**: maintain a min-heap of size k; root = k-th largest
- [ ] **Two-heap for median**: max-heap for lower half, min-heap for upper half; balance sizes
- [ ] **Merge K sorted lists**: push (val, list_index) and re-push next element after each pop

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | `exercises/kth-largest-element-in-a-stream.py` |
| [ ] | Easy   | [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) | `exercises/last-stone-weight.py` |
| [ ] | Medium | [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | `exercises/k-closest-points-to-origin.py` |
| [ ] | Medium | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | `exercises/kth-largest-element-in-an-array.py` |
| [ ] | Medium | [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | `exercises/task-scheduler.py` |
| [ ] | Medium | [Design Twitter](https://leetcode.com/problems/design-twitter/) | `exercises/design-twitter.py` |
| [ ] | Hard   | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | `exercises/find-median-from-data-stream.py` |
