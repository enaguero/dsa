# Stack — Theory Notes

---

## 1. Core Concept

A stack is a **LIFO** (Last In, First Out) abstract data type supporting:
- `push(x)` — add element to top
- `pop()` — remove and return top element
- `peek()` / `top()` — view top without removing
- `is_empty()` — check if empty

Implemented with a dynamic array (Python `list`) or a linked list. All core operations are **O(1)**.

---

## 2. Stack as Recursion Mirror

Every recursive DFS can be converted to an explicit stack loop. The call stack IS a stack — each stack frame stores local variables and the return address. Understanding this lets you convert recursive solutions to iterative ones (useful for very deep trees where Python's recursion limit ~1000 is an issue).

```python
# Recursive DFS            # Iterative DFS
def dfs(node):             stack = [root]
    if not node: return    while stack:
    visit(node)                node = stack.pop()
    dfs(node.left)             visit(node)
    dfs(node.right)            if node.right: stack.append(node.right)
                               if node.left:  stack.append(node.left)
```

---

## 3. Monotonic Stack

A monotonic stack maintains its elements in **strictly increasing** or **strictly decreasing** order by popping elements that violate the invariant before pushing.

### Decreasing Monotonic Stack (→ Next Greater Element)

```python
stack = []   # stores indices, values are decreasing
result = [-1] * n
for i in range(n):
    while stack and arr[stack[-1]] < arr[i]:
        result[stack.pop()] = arr[i]   # arr[i] is the next greater for popped index
    stack.append(i)
```

**Invariant:** When we pop index `j` because `arr[i] > arr[j]`, `arr[i]` is the **first** element to the right of `j` that is greater than `arr[j]` — because every element between `j` and `i` that was also popped was ≤ arr[j] (or was already resolved).

### O(n) Proof

Each element is pushed exactly once and popped at most once → total push + pop operations = O(n). Therefore the entire loop runs in **O(n)** time, even though the inner `while` can pop multiple elements in a single outer iteration. ✓

---

## 4. Key Applications

### Balanced Parentheses
Push opening brackets; on closing bracket, check top matches. O(n) time, O(n) space.

### Min Stack
Maintain a parallel stack of running minimums. When pushing `x`, also push `min(x, min_stack[-1])`. Pop both stacks together. All ops O(1).

### Largest Rectangle in Histogram
For each bar, find the nearest shorter bar on left and right (two monotonic stack passes, or one combined pass). Area = `height × (right_boundary − left_boundary − 1)`. Overall O(n).

### Daily Temperatures
Decreasing stack of indices. When a warmer day is found, pop and record the gap. O(n).

---

## 5. Complexity Summary

| Operation | Array-backed Stack | Linked-list Stack |
|-----------|--------------------|-------------------|
| push | O(1) amort. | O(1) |
| pop | O(1) | O(1) |
| peek | O(1) | O(1) |
| Space | O(n) | O(n) |

---

## 6. Pitfalls
- **Empty stack pop:** always guard with `if stack:` before `stack.pop()`.
- **Monotonic direction confusion:** for next-greater use decreasing stack (pop when incoming is larger); for next-smaller use increasing stack (pop when incoming is smaller).
- **Histogram boundary:** sentinel values (append 0 at end) avoid a separate cleanup loop.
