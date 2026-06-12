# Binary Search — Theory Notes

---

## 1. Core Concept

Binary search finds a target in a **sorted** (or monotone) search space by halving the space at each step. It achieves O(log n) by maintaining a loop invariant that guarantees the answer lies within `[left, right]`.

---

## 2. Loop Invariant Proof

**Algorithm (standard):**
```python
left, right = 0, n - 1
while left <= right:
    mid = left + (right - left) // 2   # avoids overflow
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
return -1
```

**Invariant:** At the start of each iteration, if `target` exists, its index is in `[left, right]`.

- **Initialisation:** `[0, n-1]` contains the full array. ✓
- **Maintenance:**
  - If `arr[mid] < target`: target can't be at `mid` or left of `mid` (array sorted), so new left = mid+1 preserves invariant. ✓
  - If `arr[mid] > target`: similarly, right = mid−1. ✓
- **Termination:** Loop ends when `left > right`. If target exists, the invariant was maintained, so we would have found it (reached `arr[mid] == target`). If we exit without returning, target is absent. ✓

---

## 3. Complexity Derivation

**Recurrence:** `T(n) = T(n/2) + O(1)`

Apply Master Theorem: `a=1, b=2, f(n)=O(1)`.
`n^(log_b a) = n^(log_2 1) = n^0 = 1`.
`f(n) = O(1) = Θ(n^0)` → **Case 2**.
Result: `T(n) = Θ(n^0 · log n) = Θ(log n)`. ✓

Alternative (substitution): Assume `T(n) = c·log₂ n + d`. Then `T(n/2) + O(1) = c·log₂(n/2) + d + 1 = c(log n − 1) + d + 1 = c·log n − c + d + 1`. Setting equal: `c·log n + d = c·log n + (−c + d + 1)` → `c = 1`. So `T(n) = log₂ n + d`. ✓

**Space:** O(1) iterative, O(log n) recursive (call stack depth).

---

## 4. Boundary Variants

### Left Boundary (first true)
Find the **leftmost** index where `condition(arr[mid])` is true (condition is monotone: false…false…true…true).

```python
left, right = 0, n          # right = n means "not found" sentinel
while left < right:
    mid = (left + right) // 2
    if condition(arr[mid]):
        right = mid         # mid might be the answer, don't exclude
    else:
        left = mid + 1
return left                 # left == right at termination
```

### Right Boundary (last true)
Find the **rightmost** index where condition is true.

```python
left, right = -1, n - 1
while left < right:
    mid = (left + right + 1) // 2   # ceil to avoid infinite loop
    if condition(arr[mid]):
        left = mid          # mid might be the answer, don't exclude
    else:
        right = mid - 1
return left
```

**Why `(left + right + 1) // 2` for right boundary:** When `right − left = 1`, floor-mid = left, and if condition(arr[left]) is true we'd set left = left → infinite loop. Ceiling-mid = right, which either advances left or shrinks right. ✓

---

## 5. Searching on the Answer Space

Many problems aren't about searching an array — they binary search on the **answer itself**.

**Template:**
```python
def feasible(candidate) -> bool:
    # check if 'candidate' works
    ...

left, right = min_possible, max_possible
while left < right:
    mid = (left + right) // 2
    if feasible(mid):
        right = mid         # or left = mid + 1 for max feasible
    else:
        left = mid + 1
return left
```

**Key insight:** The feasibility function must be **monotone** — once false, stays false (or once true, stays true) as the candidate increases.

Examples:
- Koko Eating Bananas: `feasible(speed)` = can finish all piles in H hours.
- Min days to ship: `feasible(capacity)` = can ship all packages in D days.

---

## 6. Rotated Sorted Array

One half is always unrotated (sorted). Check which half is sorted by comparing `arr[mid]` with `arr[left]`:
- If `arr[left] ≤ arr[mid]`: left half is sorted. Target in left half iff `arr[left] ≤ target < arr[mid]`.
- Else: right half is sorted. Target in right half iff `arr[mid] < target ≤ arr[right]`.

---

## 7. Complexity Summary

| Variant | Time | Space |
|---------|------|-------|
| Classic | O(log n) | O(1) |
| On answer space | O(log(max) · cost(feasible)) | O(1) |
| Recursive | O(log n) | O(log n) |

---

## 8. Pitfalls
- **`mid = (left + right) // 2`** can overflow in languages with fixed-width integers. Use `left + (right - left) // 2`.
- **Off-by-one in boundaries:** draw a small example and trace the pointers.
- **Non-monotone feasibility:** binary search fails if feasibility is not monotone — verify before applying.
