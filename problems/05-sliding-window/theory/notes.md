# Sliding Window — Theory Notes

---

## 1. Core Concept

A sliding window maintains a contiguous subarray `[left, right]` and slides it across the input to avoid recomputing from scratch. The key property that makes this O(n) is: **each element enters the window exactly once (right advances) and leaves the window at most once (left advances)**.

---

## 2. Amortized O(n) Proof

**Claim:** Both the fixed-size and variable-size sliding window algorithms run in O(n) time.

**Proof:** Define a charge of 1 unit for each pointer movement. `right` moves from 0 to n−1: exactly n movements. `left` moves from 0 to at most n−1: at most n movements. Total pointer movements ≤ 2n. Any work done per step is O(1) (assuming O(1) window-state updates). Therefore total work = O(n). ✓

If the window-state update is not O(1) (e.g., maintaining a sorted structure), the complexity multiplies: O(n log n) with a heap, O(n·k) with a naïve scan.

---

## 3. Fixed-Size Window (size k)

```python
window_sum = sum(arr[:k])
result = window_sum
for i in range(k, n):
    window_sum += arr[i] - arr[i - k]   # slide: add right, remove left
    result = max(result, window_sum)
```

Window state update: O(1) per step. Total: O(n).

---

## 4. Variable-Size Window

Two sub-patterns:

### Find Longest Window Satisfying Property P
```python
left = 0
for right in range(n):
    add(arr[right])          # expand window
    while not valid():       # shrink until valid
        remove(arr[left])
        left += 1
    result = max(result, right - left + 1)
```

### Find Shortest Window Satisfying Property P
```python
left = 0
for right in range(n):
    add(arr[right])
    while valid():           # valid → try to shrink
        result = min(result, right - left + 1)
        remove(arr[left])
        left += 1
```

**Why this works:** Suppose a valid window `[l, r]` exists. When `right` reaches `r`, all elements `[l, r]` are inside the window. At that point, `left` will be shrunk as far as possible — it will stop at `l` because shrinking further breaks validity. We don't need to try windows starting before `l` because they would only be longer (or equally long), not shorter. ✓

---

## 5. Window State Management

| Desired information | Data structure | Update cost |
|--------------------|----------------|-------------|
| Sum or count | Integer | O(1) |
| Frequency map | `Counter` / `dict` | O(1) |
| Number of distinct elements | `Counter` + count | O(1) |
| Maximum in window | `deque` (monotonic) | O(1) amort. |
| Sorted order in window | `SortedList` | O(log k) |

### Sliding Window Maximum with Deque
Maintain a decreasing deque of indices. Invariant: `deque[0]` is always the index of the max in the current window.
- Append right: pop from back while `arr[deque[-1]] ≤ arr[right]`.
- Remove left: pop from front if `deque[0] == left`.
- Max: `arr[deque[0]]`.
Each index added and removed at most once → O(n) overall.

---

## 6. Key Problems & Complexities

| Problem | Window type | State | Time |
|---------|-------------|-------|------|
| Best Time to Buy/Sell Stock | Variable (max profit) | running min | O(n) |
| Longest Substring No Repeat | Variable longest | char frequency | O(n) |
| Longest Repeating Char Replacement | Variable longest | char counts | O(n) |
| Permutation in String | Fixed (len of p) | char frequency | O(n) |
| Minimum Window Substring | Variable shortest | char needs | O(n) |
| Sliding Window Maximum | Fixed (k) | deque | O(n) |

---

## 7. Pitfalls
- **Shrinking too aggressively:** for "longest" problems, only shrink until the window is valid, not until it becomes optimal.
- **Character frequency equality:** `Counter(s) == Counter(t)` is O(Σ) where Σ is alphabet size — fine for fixed-size windows but avoid calling inside the loop for large Σ. Instead, maintain a running mismatch counter.
- **Left > right:** after shrinking, left may equal right+1. Guard `right - left + 1 ≥ 0`.
