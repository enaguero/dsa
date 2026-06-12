# Bit Manipulation — Theory Notes

---

## 1. Binary Representation

### Unsigned Integers
An n-bit unsigned integer represents values in `[0, 2ⁿ − 1]`. Each bit `bₖ` contributes `bₖ · 2ᵏ`.

### Two's Complement (Signed Integers)
The most significant bit (MSB) has weight `−2^(n-1)` instead of `+2^(n-1)`.

Value = `−bₙ₋₁ · 2^(n-1) + ∑_{k=0}^{n-2} bₖ · 2ᵏ`

**Range:** `[−2^(n-1), 2^(n-1) − 1]` for n-bit signed integer.

**Negation:** Flip all bits, then add 1.
```
~n + 1 = -n
```
**Proof:** For any n-bit value x: `x + ~x = 2ⁿ − 1` (all bits set). So `x + ~x + 1 = 2ⁿ ≡ 0 (mod 2ⁿ)` → `~x + 1 = −x`. ✓

**Python note:** Python integers are arbitrary precision (no overflow). Bitwise NOT: `~n = −n − 1`. To simulate 32-bit: `n & 0xFFFFFFFF`.

---

## 2. Bitwise Operators

| Operator | Symbol | Truth table | Effect |
|----------|--------|-------------|--------|
| AND | `a & b` | 1 iff both 1 | Masking / clearing bits |
| OR | `a \| b` | 1 if either 1 | Setting bits |
| XOR | `a ^ b` | 1 iff bits differ | Toggling, finding differences |
| NOT | `~a` | flip | `~a = -a - 1` in Python |
| Left shift | `a << k` | | Multiply by 2ᵏ |
| Right shift | `a >> k` | | Floor divide by 2ᵏ (arithmetic) |

### XOR Properties (Algebraically)
```
a ^ 0 = a              (identity element)
a ^ a = 0              (self-inverse)
a ^ b = b ^ a          (commutativity)
(a ^ b) ^ c = a ^ (b ^ c)  (associativity)
```

**XOR self-inverse proof:** In two's complement, `a ^ a` zeroes every bit because `b ⊕ b = 0` for any bit `b`. ✓

**Application — find unique element:** XOR all values. Every paired element cancels (a^a=0). The unique element remains.
```python
result = 0
for n in nums: result ^= n
```

---

## 3. Essential Bit Tricks

### Check bit k
```python
(n >> k) & 1   # returns 0 or 1
```

### Set bit k (force to 1)
```python
n | (1 << k)
```

### Clear bit k (force to 0)
```python
n & ~(1 << k)
```

### Toggle bit k
```python
n ^ (1 << k)
```

### Isolate lowest set bit
```python
n & (-n)   # equivalent to n & (~n + 1) by two's complement negation
```
**Why:** `-n = ~n + 1`. Adding 1 to `~n` propagates the carry through all trailing 1s of `~n` (which are trailing 0s of n), and the first trailing 0 of `~n` (which is the first trailing 1 of n) becomes 1. So `-n` has 1 only at the position of n's lowest set bit. `n & (-n)` keeps only that bit. ✓

### Clear lowest set bit
```python
n & (n - 1)
```
**Why:** Subtracting 1 flips the lowest set bit of n to 0 and sets all lower bits to 1. AND with n clears all lower bits. ✓

**Application — count set bits (Kernighan):**
```python
count = 0
while n:
    n &= n - 1   # remove lowest set bit
    count += 1
```
O(k) where k = popcount(n). ✓

### Check power of 2
```python
n > 0 and (n & (n - 1)) == 0
```
A power of 2 has exactly one set bit. `n-1` flips that bit and sets all lower bits. Their AND = 0. ✓

---

## 4. Number of 1 Bits (Popcount)

Three approaches:

| Method | Time | Notes |
|--------|------|-------|
| Kernighan loop | O(k) | k = number of set bits |
| `bin(n).count('1')` | O(log n) | Pythonic |
| DP: `dp[i] = dp[i>>1] + (i&1)` | O(n) total | Build table for all 0..n |

**DP explanation:** `i >> 1` removes the last bit of i. `i & 1` is the last bit. So popcount(i) = popcount(i>>1) + (last bit of i). ✓

---

## 5. Reverse Bits

```python
def reverse_bits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```
O(32) = O(1) for 32-bit integers.

---

## 6. Missing Number

In array `[0..n]` with one number missing:
```python
return n * (n + 1) // 2 - sum(nums)         # sum formula
# or:
return reduce(xor, range(n+1), 0) ^ reduce(xor, nums, 0)  # XOR
```
XOR version: XOR all 0..n and XOR all elements. Paired elements cancel; missing element remains. ✓

---

## 7. Sum of Two Integers Without `+`

```python
def get_sum(a, b):
    mask = 0xFFFFFFFF
    while b & mask:
        carry = (a & b) << 1
        a ^= b
        b = carry
    return a if b == 0 else a & mask  # handle negative results in Python
```
XOR computes sum without carry; AND+shift computes the carry. Iterate until no carry. ✓

---

## 8. Subset Enumeration with Bitmask

```python
n = len(items)
for mask in range(1 << n):        # 0 to 2ⁿ - 1
    subset = []
    for i in range(n):
        if mask & (1 << i):
            subset.append(items[i])
    process(subset)
```
O(2ⁿ · n) total. Used in bitmask DP (e.g., TSP, set cover).

---

## 9. Pitfalls
- **Python's `~n`:** in Python, `~n = -n - 1` (unbounded integers). To get 32-bit NOT: `n ^ 0xFFFFFFFF`.
- **Right shift signed vs unsigned:** Python's `>>` is arithmetic (sign-extending). For unsigned right shift: `(n & 0xFFFFFFFF) >> k`.
- **Overflow:** `1 << k` in Python never overflows. In C/Java, `1 << 31` for signed int overflows — use `1L << 31` (long).
