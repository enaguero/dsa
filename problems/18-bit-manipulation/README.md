# Bit Manipulation

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Binary Representation
- [ ] Two's complement for signed integers: flip all bits + 1 gives the negation
- [ ] Most significant bit (MSB) is the sign bit in signed integers
- [ ] Python integers have arbitrary precision (no fixed int size)

### Bitwise Operators
| Operator | Symbol | Effect |
|----------|--------|--------|
| AND | `a & b` | 1 only if both bits are 1 |
| OR | `a \| b` | 1 if either bit is 1 |
| XOR | `a ^ b` | 1 if bits differ (0 if same) |
| NOT | `~a` | flips all bits (`~a = -a - 1` in Python) |
| Left shift | `a << k` | multiply by 2ᵏ |
| Right shift | `a >> k` | divide by 2ᵏ (arithmetic) |

### Essential Tricks
- [ ] **Check bit k**: `(n >> k) & 1`
- [ ] **Set bit k**: `n | (1 << k)`
- [ ] **Clear bit k**: `n & ~(1 << k)`
- [ ] **Toggle bit k**: `n ^ (1 << k)`
- [ ] **Isolate lowest set bit**: `n & (-n)` or `n & (~n + 1)`
- [ ] **Clear lowest set bit**: `n & (n - 1)` — also used to count set bits (Kernighan's)
- [ ] **XOR for duplicate detection**: XOR all values; pairs cancel, leaving the unique element
- [ ] **Check power of 2**: `n > 0 and (n & (n - 1)) == 0`

### Counting Set Bits
- [ ] Brian Kernighan: loop `n &= n-1`, count iterations — O(number of set bits)
- [ ] `bin(n).count('1')` in Python
- [ ] DP approach: `dp[i] = dp[i >> 1] + (i & 1)`

### Bit Mask for Subsets
- [ ] Iterate all subsets of an n-bit mask: `for mask in range(1 << n)`
- [ ] Check if bit i is in mask: `mask & (1 << i)`

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Single Number](https://leetcode.com/problems/single-number/) | `exercises/single-number.py` |
| [ ] | Easy   | [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | `exercises/number-of-1-bits.py` |
| [ ] | Easy   | [Counting Bits](https://leetcode.com/problems/counting-bits/) | `exercises/counting-bits.py` |
| [ ] | Easy   | [Reverse Bits](https://leetcode.com/problems/reverse-bits/) | `exercises/reverse-bits.py` |
| [ ] | Easy   | [Missing Number](https://leetcode.com/problems/missing-number/) | `exercises/missing-number.py` |
| [ ] | Medium | [Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers/) | `exercises/sum-of-two-integers.py` |
| [ ] | Medium | [Reverse Integer](https://leetcode.com/problems/reverse-integer/) | `exercises/reverse-integer.py` |
