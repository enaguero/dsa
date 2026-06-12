# Trees — Theory Notes

---

## 1. Definitions

**Binary tree:** Each node has at most 2 children (left, right).

**Height `h(v)`:** Length of the longest path from node `v` to a leaf. Leaf has height 0. Empty tree: h = −1.

**Depth `d(v)`:** Length of the path from the root to `v`. Root has depth 0.

**Full binary tree:** every node has 0 or 2 children.
**Complete binary tree:** all levels filled except possibly the last, which is filled left-to-right.
**Perfect binary tree:** all internal nodes have 2 children and all leaves at the same depth.

### Height Bounds

| Tree type | Height |
|-----------|--------|
| Balanced (AVL, RB-tree) | O(log n) |
| Complete | ⌊log₂ n⌋ |
| Skewed (worst case) | n − 1 |

**Proof (perfect binary tree):** A perfect tree of height `h` has `2^(h+1) − 1` nodes (geometric series). Inverting: `h = log₂(n+1) − 1 = Θ(log n)`. ✓

---

## 2. Binary Search Tree (BST)

**BST Property:** For every node `v`: all keys in the left subtree < `key(v)` < all keys in the right subtree.

**Note:** The BST property must hold for the entire subtree, not just direct children.

| Operation | Balanced BST | Skewed BST |
|-----------|-------------|------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Min/Max | O(log n) | O(n) |

**Delete (3 cases):**
1. Leaf: just remove.
2. One child: replace node with child.
3. Two children: replace with **inorder successor** (min of right subtree), then delete the successor from right subtree.

**Inorder traversal of BST = sorted sequence** (proof by structural induction on the BST property).

---

## 3. DFS Traversals

All traversals visit each node exactly once → **O(n) time, O(h) space** (recursion stack).

```
Preorder:  root → left → right    [serialize, copy]
Inorder:   left → root → right    [sorted output from BST]
Postorder: left → right → root    [delete tree, evaluate expr]
```

### Iterative Inorder
```python
stack, curr = [], root
while stack or curr:
    while curr:
        stack.append(curr)
        curr = curr.left
    curr = stack.pop()
    visit(curr)
    curr = curr.right
```

**Invariant:** `stack` contains nodes whose left subtree is fully processed; `curr` is the next node to descend into.

---

## 4. BFS / Level-Order

```python
from collections import deque
q = deque([root])
while q:
    node = q.popleft()
    visit(node)
    if node.left:  q.append(node.left)
    if node.right: q.append(node.right)
```

O(n) time. O(w) space where `w` is the maximum width (up to O(n) for a complete tree).

---

## 5. Key Algorithms with Complexity

### Lowest Common Ancestor (LCA)
```python
def lca(root, p, q):
    if not root or root is p or root is q:
        return root
    left  = lca(root.left, p, q)
    right = lca(root.right, p, q)
    return root if (left and right) else (left or right)
```
**Correctness:** If both `p` and `q` are found in different subtrees, `root` is the LCA. Otherwise the LCA is in the subtree that returned non-null. O(n) time, O(h) space.

### Diameter
At each node, the longest path **through that node** = `left_height + right_height`. Track global max.
```python
def height(node):
    if not node: return 0
    l, r = height(node.left), height(node.right)
    diameter = max(diameter, l + r)
    return 1 + max(l, r)
```
O(n) time (each node processed once).

### Serialize / Deserialize
Preorder + null markers uniquely identifies a binary tree. O(n) time and space.

---

## 6. Balanced Tree Check

**Definition:** A tree is balanced if `|h(left) − h(right)| ≤ 1` at every node.

Naïve O(n²): check height at every node. Optimal O(n): return height from leaves up; if any node is unbalanced return -1 as a sentinel.

---

## 7. Pitfalls
- **BST validation:** don't just compare node with its children. Pass min/max bounds down the recursion.
  - `validate(node, lo=-∞, hi=+∞)` — valid iff `lo < node.val < hi`.
- **Height vs depth:** height is measured from leaves up, depth from root down.
- **Iterative inorder:** push left spine first, then process, then move right.
