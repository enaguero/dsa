# Trees

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Binary Tree Basics
- [ ] Each node has at most 2 children (left, right)
- [ ] Height: longest path from root to leaf; depth: distance from root
- [ ] Full, complete, perfect, and balanced trees — definitions and properties
- [ ] n nodes → height is O(log n) for balanced, O(n) worst case (skewed)

### Binary Search Tree (BST)
- [ ] Left subtree values < node < right subtree values (all nodes, not just children)
- [ ] Inorder traversal of a BST gives sorted output
- [ ] Search, insert, delete: O(h) — O(log n) balanced, O(n) worst case

### DFS Traversals (recursive and iterative)
- [ ] **Preorder** (root → left → right): serialize/copy a tree
- [ ] **Inorder** (left → root → right): sorted order from BST
- [ ] **Postorder** (left → right → root): delete tree, evaluate expression tree
- [ ] Iterative inorder: use an explicit stack

### BFS / Level-Order
- [ ] Use a queue; process level by level
- [ ] Useful for: level-order output, right side view, zigzag traversal

### Key Algorithms
- [ ] Lowest Common Ancestor (LCA): recurse; if both sides return non-null → current node is LCA
- [ ] Diameter: at each node, max path through it = left_height + right_height
- [ ] Path sum problems: carry running sum down, check at leaves

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | `exercises/invert-binary-tree.py` |
| [ ] | Easy   | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | `exercises/maximum-depth-of-binary-tree.py` |
| [ ] | Easy   | [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | `exercises/diameter-of-binary-tree.py` |
| [ ] | Easy   | [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | `exercises/balanced-binary-tree.py` |
| [ ] | Easy   | [Same Tree](https://leetcode.com/problems/same-tree/) | `exercises/same-tree.py` |
| [ ] | Easy   | [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | `exercises/subtree-of-another-tree.py` |
| [ ] | Medium | [Lowest Common Ancestor of a BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | `exercises/lowest-common-ancestor-of-a-binary-search-tree.py` |
| [ ] | Medium | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | `exercises/binary-tree-level-order-traversal.py` |
| [ ] | Medium | [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | `exercises/binary-tree-right-side-view.py` |
| [ ] | Medium | [Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) | `exercises/count-good-nodes-in-binary-tree.py` |
| [ ] | Medium | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | `exercises/validate-binary-search-tree.py` |
| [ ] | Medium | [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | `exercises/kth-smallest-element-in-a-bst.py` |
| [ ] | Medium | [Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | `exercises/construct-binary-tree-from-preorder-and-inorder-traversal.py` |
| [ ] | Hard   | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | `exercises/binary-tree-maximum-path-sum.py` |
| [ ] | Hard   | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | `exercises/serialize-and-deserialize-binary-tree.py` |
