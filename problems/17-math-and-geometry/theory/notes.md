# Math & Geometry — Theory Notes

---

## 1. Modular Arithmetic

**Definition:** `a ≡ b (mod m)` iff `m | (a − b)` (m divides a−b).

### Properties
```
(a + b) mod m = ((a mod m) + (b mod m)) mod m
(a * b) mod m = ((a mod m) * (b mod m)) mod m
(a - b) mod m = ((a mod m) - (b mod m) + m) mod m   ← +m to avoid negative
```

Apply `mod m` at each step to prevent overflow (especially in competitive programming).

### Modular Inverse
For prime modulus `m` and `gcd(a, m) = 1`:
```
a⁻¹ ≡ a^(m-2) (mod m)      ← Fermat's Little Theorem: a^(m-1) ≡ 1 (mod m)
```
Compute with fast exponentiation in O(log m).

---

## 2. GCD & LCM

### Euclidean Algorithm
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
```
`lcm(a, b) = a * b // gcd(a, b)`

**Correctness:** `gcd(a, b) = gcd(b, a mod b)` because any common divisor of a and b also divides `a mod b = a − ⌊a/b⌋·b`. ✓

**Complexity:** O(log(min(a, b)))

*Proof:* After two steps, the argument decreases by at least half: `a mod b < a/2` when `b ≤ a/2`; and when `b > a/2`, `a mod b = a − b < a/2`. So every two steps halve the input → O(log a) steps total. ✓

Equivalently, the worst case is consecutive Fibonacci numbers (Lamé's theorem): `gcd(F_{n+1}, F_n)` requires n steps, and `F_n = O(φⁿ)` → log₂(F_n) = Θ(n) → O(log(min(a,b))) steps.

---

## 3. Fast Exponentiation (Binary Exponentiation)

**Goal:** Compute `base^exp mod m` in O(log exp).

```python
def pow_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:              # if current bit is 1
            result = result * base % mod
        base = base * base % mod  # square
        exp >>= 1                # move to next bit
    return result
```

**Correctness:** Decompose `exp` in binary: `exp = bₖ·2ᵏ + … + b₁·2 + b₀`. Then:
```
base^exp = base^(bₖ·2ᵏ) · … · base^(b₁·2) · base^(b₀)
         = (base^(2ᵏ))^bₖ · … · (base²)^b₁ · base^b₀
```
Each factor is a successive squaring of base, multiplied in only if the corresponding bit is 1. ✓

**Complexity:** O(log exp) multiplications.

---

## 4. Prime Numbers

### Trial Division (single number)
```python
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True
```
O(√n) — any composite n has a factor ≤ √n. ✓

### Sieve of Eratosthenes (primes up to N)
```python
def sieve(N):
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(N**0.5) + 1):
        if is_prime[p]:
            for multiple in range(p*p, N+1, p):
                is_prime[multiple] = False
    return [i for i, v in enumerate(is_prime) if v]
```

**Complexity:** O(N log log N)

*Proof:* Total work = `∑_{p prime ≤ N} N/p ≈ N · log log N` by Mertens' theorem. ✓

Start marking from `p²` because all smaller multiples of p were already marked by smaller primes. ✓

---

## 5. 2-D Matrix Operations

### Rotate Image 90° Clockwise
1. Transpose: `matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]`.
2. Reverse each row: `matrix[i].reverse()`.

**Why:** A 90° clockwise rotation maps `(i, j) → (j, n-1-i)`. Transposing maps `(i, j) → (j, i)`. Then reversing each row maps `(i, j) → (i, n-1-j)`. Combined: `(i, j) → (j, n-1-i)`. ✓

O(n²) time, O(1) space.

### Spiral Matrix
Peel the outermost ring: traverse right → down → left → up, then shrink boundaries. O(m·n) time.

### Set Matrix Zeroes
**Naïve:** mark zeros in a separate set. O(m·n) space.
**Optimal:** use the first row and first column as markers. Handle the corner `(0,0)` with a separate flag. O(1) extra space.

---

## 6. Happy Number (Cycle Detection)

Apply Floyd's cycle detection on the sequence of digit-square-sums. A number is happy iff the sequence eventually reaches 1 (which is a fixed point). All unhappy numbers eventually enter a cycle not containing 1.

O(log n) digits → each step is O(log n). Total steps until cycle ≤ O(cycle length) which is bounded.

---

## 7. Number Theory Tricks

| Trick | Code | Notes |
|-------|------|-------|
| Extract last digit | `n % 10` | |
| Remove last digit | `n // 10` | |
| Reverse integer | while loop + `% 10` + `// 10` | Handle overflow: check `INT_MIN/10 ≤ rev ≤ INT_MAX/10` |
| Power of 2 check | `n > 0 and (n & (n-1)) == 0` | |
| Power of 3 check | `n > 0 and 3**19 % n == 0` | 3^19 is largest power of 3 in int range |
| Digit sum | `sum(int(d) for d in str(n))` | |

---

## 8. Pitfalls
- **Integer overflow:** Python handles big ints natively. In other languages, `(a + b)` can overflow; use `a + (b - a) // 2` or modular forms.
- **Floating-point sqrt:** `int(n**0.5)` can be off by 1 due to float precision. Safer: `isqrt(n)` (Python 3.8+).
- **Sieve space:** for N = 10⁸, a boolean array uses 100 MB. Use a bitarray or segmented sieve.
