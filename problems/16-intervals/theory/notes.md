# Intervals — Theory Notes

---

## 1. Core Definitions

An **interval** is a pair `[start, end]` representing a contiguous range on the number line. Two intervals `[a, b]` and `[c, d]` **overlap** iff `a ≤ d` and `c ≤ b` (or equivalently, they do NOT overlap iff `b < c` or `d < a`).

---

## 2. Merge Intervals

**Algorithm:**
1. Sort by `start` time: O(n log n).
2. Iterate: if the current interval overlaps the last merged interval, extend the end. Otherwise, append.

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:           # overlap
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

**Correctness:** After sorting by start, any interval that overlaps with the last merged interval must overlap with it (since its start ≤ last_end). Intervals that don't overlap can't be merged with anything to the left (their start is past the farthest right end). ✓

**Complexity:** O(n log n) — sorting dominates; the scan is O(n).

---

## 3. Insert Interval

Given a sorted non-overlapping list, insert a new interval and merge.

```python
def insert(intervals, new):
    result, i, n = [], 0, len(intervals)
    # Add all intervals that end before new starts
    while i < n and intervals[i][1] < new[0]:
        result.append(intervals[i]); i += 1
    # Merge overlapping intervals with new
    while i < n and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    result.append(new)
    # Add remaining
    result.extend(intervals[i:])
    return result
```

O(n) time (single pass), O(n) space.

---

## 4. Non-Overlapping Intervals (Minimum Removals)

**Goal:** Find the minimum number of intervals to remove so that the rest are non-overlapping.

**Equivalently:** Find the maximum number of non-overlapping intervals (activity selection), then subtract from total.

**Greedy — sort by end time:**
```python
def erase_overlap_intervals(intervals):
    intervals.sort(key=lambda x: x[1])
    count = 0
    end = float('-inf')
    for start, e in intervals:
        if start >= end:
            end = e       # keep this interval
        else:
            count += 1    # remove this interval (it overlaps)
    return count
```

**Why sort by end time?** (Exchange Argument)
Suppose an optimal solution keeps interval A with end time `e_A` instead of greedy's choice G with `e_G ≤ e_A`. Swapping A for G leaves all subsequent intervals compatible (G ends no later than A). So replacing A with G never reduces the count of kept intervals. ✓

**Complexity:** O(n log n) sort + O(n) scan = **O(n log n)**.

---

## 5. Meeting Rooms I & II

### Meeting Rooms I
Can a person attend all meetings? iff no two intervals overlap after sorting by start.

### Meeting Rooms II — Minimum Rooms

**Lower bound:** The minimum number of rooms needed is at least `max_overlap` (the maximum number of simultaneously active meetings). This is also achievable (tight bound).

**Sweep line approach:**
```python
import heapq
def min_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []   # min-heap of end times of active meetings
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)  # reuse a room
        else:
            heapq.heappush(heap, end)     # need a new room
    return len(heap)
```

**Alternative (two-pointer sweep):**
```python
starts = sorted(s for s, e in intervals)
ends   = sorted(e for s, e in intervals)
rooms = active = 0
j = 0
for s in starts:
    if s < ends[j]: active += 1   # a new meeting starts before any ends
    else: j += 1                  # reuse the room that just ended
    rooms = max(rooms, active)
return rooms
```

Both are O(n log n).

---

## 6. Minimum Interval to Include Each Query

For each query point `q`, find the smallest-length interval `[l, r]` with `l ≤ q ≤ r`.

**Efficient approach:**
1. Sort intervals by length.
2. Sort queries with their original indices.
3. For each query (increasing): add all intervals whose start ≤ query to a min-heap (by end). Remove all intervals whose end < query. The heap's root is the answer (smallest remaining interval containing the query). O((n + m) log n).

---

## 7. Complexity Summary

| Problem | Time | Space |
|---------|------|-------|
| Merge Intervals | O(n log n) | O(n) |
| Insert Interval | O(n) | O(n) |
| Non-Overlapping (min removals) | O(n log n) | O(1) |
| Meeting Rooms I | O(n log n) | O(1) |
| Meeting Rooms II | O(n log n) | O(n) |
| Min Interval per Query | O((n+m) log n) | O(n+m) |

---

## 8. Pitfalls
- **Overlap condition:** `[1,2]` and `[2,3]` overlap (they share point 2). The condition is `start ≤ last_end`, not `<`.
- **Sorting key:** for merge, sort by start; for activity selection (remove minimum), sort by end. Confusing the two gives wrong results.
- **Open vs closed intervals:** clarify whether endpoints are included. Most LeetCode problems use closed intervals.
