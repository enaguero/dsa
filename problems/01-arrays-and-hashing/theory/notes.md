# Arrays & Hashing — Theory Notes

---

## 1. Arrays

### Formal Definition
An array is a sequence of `n` elements stored in **contiguous memory** starting at base address `B`. Element `i` is at address `B + i·w`, where `w` is the element size in bytes.

### Key Operations

| Operation | Time | Notes |
|-----------|------|-------|
| Access `a[i]` | O(1) | Address arithmetic: `B + i·w` |
| Search (unsorted) | O(n) | Must scan all elements |
| Insert at end | O(1) amort. | Dynamic array |
| Insert at index i | O(n) | Shift elements right |
| Delete at index i | O(n) | Shift elements left |

### Dynamic Array — Amortized O(1) Insert (Potential Method)

A dynamic array doubles its capacity when full. We prove insert is **O(1) amortized**.

**Potential function:** `Φ(D) = 2 · size − capacity`

- After initialising an empty array: `size=0, capacity=1 → Φ = -1` (treated as 0, cap ≥ 0 always).
- **Non-resize insert:** actual cost = 1. `ΔΦ = 2(size+1 − capacity) − 2(size − capacity) = 2`. Amortized cost = 1 + 2 = **3 = O(1)**.
- **Resize insert:** capacity doubles from `c` to `2c`, size goes from `c` to `c+1`. Actual cost = `c + 1` (copy c elements + insert). `ΔΦ = 2(c+1) − 2c − (2c − c) = 2 + 2 − c = −c + 2`. Amortized cost = `(c+1) + (−c+2) = 3 = O(1)`.

Total cost for `n` insertions ≤ 3n → each insertion is **O(1) amortized**. ✓

---

## 2. Hash Tables

### Formal Definition
A hash table stores key-value pairs using a **hash function** `h : U → {0, …, m−1}` that maps a universe of keys `U` to `m` buckets.

### Hash Function Properties
1. **Deterministic:** same key → same bucket.
2. **Uniform:** ideally, each key maps to any bucket with probability 1/m.
3. **Fast to compute:** O(1) or O(key length).

### Collision Strategies

**Chaining (separate chaining)**
- Each bucket holds a linked list of (key, value) pairs.
- Load factor: `α = n/m` where `n` = number of stored keys.
- Expected chain length = α.
- Expected O(1) search when α = O(1) (e.g., keep m ≥ n).

**Open Addressing (linear probing)**
- On collision, probe `h(k, i) = (h(k) + i) mod m`.
- Expected probes for unsuccessful search: `1 / (1 − α)` (geometric series).
- Degrades badly at α > 0.7; Python's dict uses α ≈ 2/3 before resize.

### Expected O(1) Analysis

Assuming **Simple Uniform Hashing** (each key equally likely to hash to any bucket, independently):

- P(key k₁ and k₂ collide) = 1/m.
- Expected number of keys in the same bucket as a query key = `(n−1)/m ≈ α`.
- Expected search time = `O(1 + α)`.
- With `m = Θ(n)`, α = Θ(1), so search is **expected O(1)**. ✓

### Rehashing
When α exceeds threshold (typically 0.75), create a new table of size `2m` and re-insert all keys. Cost = O(n). By amortized analysis similar to dynamic arrays: amortized O(1) per insertion.

### Python `dict` internals
- Open addressing with quadratic probing variant.
- Initial capacity = 8; load factor threshold ≈ 2/3.
- Keys must be **hashable** (immutable): int, str, tuple of hashables.

---

## 3. Prefix Sums

Preprocessing: `pre[i] = a[0] + a[1] + … + a[i]`.

Range sum `[l, r]` = `pre[r] − pre[l−1]` in O(1) after O(n) build.

---

## 4. Key Patterns

| Pattern | Idea | Example |
|---------|------|---------|
| Frequency map | `count = Counter(arr)` | Group anagrams, top-k |
| Canonical key | sort or freeze to create a group key | Anagram grouping |
| Set membership | O(1) lookup vs O(n) list scan | Contains duplicate |
| Complement lookup | store `target − x` in map | Two sum |
| Prefix sum | range queries in O(1) | Product except self |

---

## 5. Pitfalls & Edge Cases
- **Hash collision attack:** Python's hash is randomised per process (PYTHONHASHSEED) — don't rely on insertion order for security.
- **Mutable default dicts:** `dict.get(k, [])` returns a new list; `defaultdict(list)` mutates in place.
- **Integer overflow:** Python ints are arbitrary precision — no overflow, but very large ints hash slowly.
- **Floating-point keys:** avoid; `0.1 + 0.2 ≠ 0.3` in IEEE 754.
