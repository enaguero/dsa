# Two Pointers — Theory Notes

---

## 1. Core Concept

Two pointers is a technique where two index variables scan a data structure, moving according to a condition. It converts O(n²) nested-loop brute force into O(n) by exploiting a **monotone** relationship: when one pointer advances, the search space for the other pointer only moves in one direction.

---

## 2. Patterns

### Pattern A — Opposite Ends (Converging Pointers)

```
left = 0, right = n - 1
while left < right:
    if condition(arr[left], arr[right]):
        process()
    elif too_small:
        left += 1
    else:
        right -= 1
```

**Correctness proof (Two Sum on sorted array):**

*Claim:* If a valid pair `(i, j)` with `i < j` and `arr[i] + arr[j] = target` exists, the algorithm finds it.

*Proof by contradiction:* Suppose the algorithm misses pair `(i*, j*)`. Without loss of generality, assume left pointer passes `i*` (moves past it) because at that moment `arr[left] + arr[right] < target` (sum too small). But then `arr[right] ≤ arr[j*]`, so `arr[i*] + arr[right] ≤ arr[i*] + arr[j*] = target`. Since the sum was too small, `arr[right] < arr[j*]` — but the array is sorted, so right hasn't passed `j*` yet. As left passed `i*` while right ≥ j*, there will be a step where left = i* and right = j*, and we'd process the pair. Contradiction. ✓

**Convergence:** At each step, either `left` increases or `right` decreases. Since `left ≤ right`, the loop terminates in at most `n` steps.

**Complexity:** O(n) time, O(1) space.

---

### Pattern B — Same Direction (Fast & Slow / Read & Write)

```
slow = 0
for fast in range(n):
    if condition(arr[fast]):
        arr[slow] = arr[fast]
        slow += 1
```

Used for: in-place filtering, removing duplicates, Dutch national flag partition.

**Invariant:** `arr[0..slow-1]` always satisfies the desired property. `fast` scans forward to find the next qualifying element.

---

### Pattern C — Fast & Slow (Floyd's — see Linked List)

Two pointers at different speeds. Cycle detection: if a cycle exists, fast catches slow.

---

## 3. 3Sum — Reduction to 2Sum

Fix one element `a[i]`, then run converging two-pointer on `a[i+1..n-1]` to find a pair summing to `-a[i]`. Sort first: O(n log n). Outer loop: O(n). Inner two-pointer: O(n). Total: **O(n²)**.

Duplicate skipping: after finding or skipping a pair, advance pointers past identical values to avoid duplicate triplets.

---

## 4. Complexity Summary

| Problem | Time | Space |
|---------|------|-------|
| Valid palindrome | O(n) | O(1) |
| Two Sum II (sorted) | O(n) | O(1) |
| 3Sum | O(n²) | O(1) or O(n) sort |
| Container with most water | O(n) | O(1) |
| Trapping rain water | O(n) | O(1) |

---

## 5. When to Apply

- Array/string is **sorted** (or can be sorted without changing the answer).
- You need pairs or triplets satisfying a sum/difference condition.
- You're partitioning or compressing in-place.
- Moving both pointers left → you only need to check each element once.

---

## 6. Pitfalls
- **Unsorted input:** two-pointer for sum problems requires sorted order; sorting takes O(n log n) — still better than O(n²).
- **Duplicate handling in 3Sum:** after a match, skip `while arr[left] == arr[left-1]: left += 1` to avoid duplicate triplets.
- **Off-by-one:** use `while left < right`, not `≤`, for converging pointers.
