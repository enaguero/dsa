# Backtracking — Theory Notes

---

## 1. Core Concept

Backtracking is a **systematic search** through a decision tree. At each node, we:
1. Make a choice (extend the current partial solution).
2. Recurse to explore consequences.
3. Undo the choice (**backtrack**) to try the next option.

Backtracking is depth-first search on the implicit decision tree, with **pruning** to cut branches that can't lead to a valid solution.

---

## 2. General Template

```python
def backtrack(state, start, choices):
    if is_complete(state):
        results.append(state[:])   # copy — not a reference
        return
    for i in range(start, len(choices)):
        if is_valid(state, choices[i]):
            state.append(choices[i])          # make choice
            backtrack(state, next_start, choices)
            state.pop()                       # undo choice
```

---

## 3. Problem Categories

### Subsets — O(2ⁿ)

Every element is either included or excluded → 2 choices per element → 2ⁿ subsets.

```python
def subsets(nums):
    result, subset = [], []
    def bt(start):
        result.append(subset[:])
        for i in range(start, len(nums)):
            subset.append(nums[i])
            bt(i + 1)
            subset.pop()
    bt(0)
    return result
```

### Permutations — O(n!)

Each level has `n − depth` choices. Total leaves = n!. Total nodes = `∑_{k=0}^{n} n!/k!  ≤ e·n!` = O(n!).

```python
def permute(nums):
    result = []
    def bt(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                bt(path + [nums[i]], used)
                used[i] = False
    bt([], [False]*len(nums))
    return result
```

### Combinations C(n, k) — O(C(n,k) · k)

Choose `k` elements from `n`. Number of results = C(n,k). Each result has length k. Total work ∝ C(n,k)·k.

**Pruning:** if `len(nums) - start + 1 < k - len(current)` (not enough elements remain), prune immediately.

### Duplicates

Sort the input first. Skip `choices[i]` if `i > start and choices[i] == choices[i-1]` to avoid duplicate results at the same decision level.

---

## 4. Complexity Analysis

### Decision Tree Size

| Problem | Branching factor | Depth | Total nodes |
|---------|-----------------|-------|-------------|
| Subsets | 2 at each element | n | O(2ⁿ) |
| Permutations (no repeats) | n, n-1, ..., 1 | n | O(n!) |
| Combinations C(n,k) | ≤ n | k | O(C(n,k)) |
| N-Queens | ≤ n | n | O(n!) but pruned heavily |

### Effect of Pruning

Pruning reduces the actual number of nodes explored but doesn't change the worst-case bound (since the worst case has no prunable branches). In practice, N-Queens at n=8 explores ~15,720 nodes vs 8! = 40,320 worst case.

---

## 5. Space Complexity

- **Call stack depth** = depth of the decision tree (O(n) for most problems).
- **State at each level** = O(depth) for path/current-subset storage.
- Total space: O(n) ignoring output storage.

---

## 6. Board Problems (N-Queens, Sudoku)

Use constraint sets (row, col, diagonals) to check validity in O(1) rather than O(n).

```python
# N-Queens: track which cols and diagonals are occupied
cols, diag1, diag2 = set(), set(), set()
def place(row):
    if row == n:
        result.append(board[:])
        return
    for col in range(n):
        if col in cols or (row-col) in diag1 or (row+col) in diag2:
            continue
        # place queen
        cols.add(col); diag1.add(row-col); diag2.add(row+col)
        board[row] = col
        place(row + 1)
        cols.remove(col); diag1.remove(row-col); diag2.remove(row+col)
```

---

## 7. Pitfalls
- **Copying state:** `result.append(path)` stores a reference — it will be empty after backtracking. Use `path[:]` or `path.copy()`.
- **Duplicate avoidance:** only skip `nums[i] == nums[i-1]` if `i > start` (not `i > 0`), to allow the same value at different positions of the decision tree.
- **Word Search board:** mark the cell as visited before recursing (`board[r][c] = '#'`), restore after.
