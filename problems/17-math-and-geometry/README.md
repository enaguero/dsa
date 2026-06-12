# Math & Geometry

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Modular Arithmetic
- [ ] `(a + b) % m = ((a % m) + (b % m)) % m` — apply mod at each step to prevent overflow
- [ ] `(a * b) % m = ((a % m) * (b % m)) % m`
- [ ] Modular inverse: `a⁻¹ mod m = a^(m-2) mod m` when m is prime (Fermat's little theorem)

### GCD & LCM
- [ ] Euclidean algorithm: `gcd(a, b) = gcd(b, a % b)`; base case `gcd(a, 0) = a`
- [ ] `lcm(a, b) = a * b // gcd(a, b)`

### Fast Exponentiation (Binary Exponentiation)
- [ ] Compute `x^n` in O(log n) by squaring: if n is even → `(x²)^(n/2)`; if odd → `x * x^(n-1)`

### Prime Numbers
- [ ] Sieve of Eratosthenes: mark multiples of each prime up to √n; O(n log log n)
- [ ] Trial division for single number: check divisors up to √n

### 2-D Geometry
- [ ] Rotate matrix 90° clockwise: transpose then reverse each row
- [ ] Spiral traversal: peel outer layer, recurse/iterate inward
- [ ] Set matrix zeroes: first pass records zero positions, second pass zeros rows/cols

### Number Theory Tricks
- [ ] Happy number: cycle detection (Floyd's) on the digit-square-sum sequence
- [ ] Power of 2/3: `n > 0 and (n & n-1) == 0` for power of 2
- [ ] Digit extraction: `n % 10` gets last digit; `n // 10` removes it

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Happy Number](https://leetcode.com/problems/happy-number/) | `exercises/happy-number.py` |
| [ ] | Easy   | [Plus One](https://leetcode.com/problems/plus-one/) | `exercises/plus-one.py` |
| [ ] | Medium | [Rotate Image](https://leetcode.com/problems/rotate-image/) | `exercises/rotate-image.py` |
| [ ] | Medium | [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | `exercises/spiral-matrix.py` |
| [ ] | Medium | [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | `exercises/set-matrix-zeroes.py` |
| [ ] | Medium | [Pow(x, n)](https://leetcode.com/problems/powx-n/) | `exercises/powx-n.py` |
| [ ] | Medium | [Multiply Strings](https://leetcode.com/problems/multiply-strings/) | `exercises/multiply-strings.py` |
| [ ] | Medium | [Detect Squares](https://leetcode.com/problems/detect-squares/) | `exercises/detect-squares.py` |
