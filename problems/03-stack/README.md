# Stack

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Stack Basics
- [ ] LIFO (Last In, First Out) — push/pop/peek all O(1)
- [ ] Implemented with a dynamic array or linked list
- [ ] The call stack is itself a stack — recursion and iterative DFS mirror each other

### Monotonic Stack
- [ ] Maintains elements in strictly increasing or decreasing order
- [ ] Increasing stack: pop when new element is smaller → finds next smaller element
- [ ] Decreasing stack: pop when new element is larger → finds next greater element
- [ ] Each element pushed and popped at most once → O(n) overall

### Common Applications
- [ ] Balanced parentheses / bracket matching
- [ ] Next greater/smaller element
- [ ] Daily temperatures, car fleet problems
- [ ] Histogram largest rectangle (use stack to track indices)
- [ ] Expression evaluation and conversion (infix → postfix)

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | `exercises/valid-parentheses.py` |
| [ ] | Medium | [Min Stack](https://leetcode.com/problems/min-stack/) | `exercises/min-stack.py` |
| [ ] | Medium | [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | `exercises/evaluate-reverse-polish-notation.py` |
| [ ] | Medium | [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | `exercises/generate-parentheses.py` |
| [ ] | Medium | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | `exercises/daily-temperatures.py` |
| [ ] | Medium | [Car Fleet](https://leetcode.com/problems/car-fleet/) | `exercises/car-fleet.py` |
| [ ] | Hard   | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | `exercises/largest-rectangle-in-histogram.py` |
