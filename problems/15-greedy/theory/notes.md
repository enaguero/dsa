# Greedy — Theory Notes

---

## 1. Core Concept

A greedy algorithm makes the **locally optimal choice** at each step, hoping it leads to a globally optimal solution. Unlike DP (which exhausts all options), greedy commits to a choice irrevocably.

---

## 2. When Does Greedy Work?

Two properties must hold:

### Greedy Choice Property
There exists an optimal solution that includes the greedy choice. Making the locally best choice does **not** foreclose reaching a globally optimal solution.

### Optimal Substructure
After making the greedy choice, the remaining subproblem has optimal substructure (same as DP).

---

## 3. Proving Correctness: Exchange Argument

The standard proof technique for greedy algorithms.

**Template:**
1. Let OPT be any optimal solution.
2. Let GREEDY be the greedy solution.
3. Show that OPT can be transformed into GREEDY by a sequence of exchanges, each of which does not decrease the solution's quality.
4. Therefore GREEDY is at least as good as OPT → GREEDY is optimal. ✓

**Example — Activity Selection (sort by end time):**
- Greedy: always pick the activity with the earliest end time that doesn't conflict.
- Let OPT contain activity A at position k (with later end time than greedy's choice G at position k).
- Swap A for G: G finishes no later than A, so all activities after A in OPT are still compatible with G. The new solution has the same number of activities → still optimal.
- After all exchanges, OPT = GREEDY. ✓

---

## 4. Greedy vs DP

| | Greedy | DP |
|---|--------|-----|
| Decision | One irrevocable local choice | All choices explored (or memoised) |
| Proof | Exchange argument | Optimal substructure + overlapping subproblems |
| Complexity | Usually O(n log n) or O(n) | Often O(n²) or more |
| When applicable | Greedy choice property holds | Always (if substructure exists) |

**Classic counterexample for greedy:**
Coin change with coins {1, 3, 4}, target = 6.
- Greedy: 4+1+1 = 3 coins.
- Optimal: 3+3 = 2 coins.
Greedy fails because {1, 3, 4} doesn't satisfy the greedy choice property for coin change. Use DP.

---

## 5. Key Greedy Patterns

### Kadane's Algorithm (Maximum Subarray)
```python
max_sum = curr = nums[0]
for n in nums[1:]:
    curr = max(n, curr + n)   # extend or restart
    max_sum = max(max_sum, curr)
```
**Intuition:** If the running sum goes negative, starting fresh from the current element is always better. O(n) time, O(1) space.

**Proof:** At each position, the optimal subarray ending at position i either starts fresh at i (`nums[i]`) or extends the optimal subarray ending at i-1 (`curr + nums[i]`). Greedy choice = the larger one. ✓

### Jump Game
```python
max_reach = 0
for i, jump in enumerate(nums):
    if i > max_reach: return False   # can't reach this position
    max_reach = max(max_reach, i + jump)
return True
```
**Invariant:** `max_reach` = the farthest position reachable with the first i+1 elements. O(n) time, O(1) space.

### Jump Game II (Minimum Jumps)
```python
jumps = curr_end = far = 0
for i in range(len(nums) - 1):
    far = max(far, i + nums[i])
    if i == curr_end:           # exhausted current jump range
        jumps += 1
        curr_end = far
return jumps
```
**Greedy choice:** From the current jump range `[prev_end+1, curr_end]`, always jump to the farthest reachable position. O(n) time, O(1) space.

### Gas Station
```python
total = tank = start = 0
for i in range(n):
    gain = gas[i] - cost[i]
    total += gain
    tank += gain
    if tank < 0:
        start = i + 1   # can't start from anything up to i
        tank = 0
return start if total >= 0 else -1
```
**Key insight:** If total gas ≥ total cost, a solution exists. The starting point must be after the last negative-tank position. O(n) time, O(1) space.

---

## 6. Sorting as a Greedy Pre-step

Many greedy algorithms require sorting as a first step to reveal the correct order to process elements:
- **Interval scheduling:** sort by end time.
- **Merge intervals:** sort by start time.
- **Hand of Straights:** sort and process smallest first.
- **Partition labels:** precompute last occurrence of each character.

Sorting is O(n log n) → dominates the overall complexity in these cases.

---

## 7. Pitfalls
- **Not verifying the greedy choice property:** test with small counterexamples before coding.
- **Greedy for NP-hard problems:** many NP-hard problems (e.g., general knapsack, TSP) have greedy approximations but not exact greedy solutions.
- **Gas Station:** if total < 0, there's no valid starting point — return -1 before returning `start`.
