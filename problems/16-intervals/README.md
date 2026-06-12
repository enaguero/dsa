# Intervals

> **[Theory Notes](theory/notes.md)** — formal definitions, complexity proofs, and patterns.
> **[Exercises](exercises/)** — solution stubs (one `.py` file per problem).


## Theory

### Core Operations
- [ ] **Sort by start time**: prerequisite for most interval problems
- [ ] **Overlap check**: interval A and B overlap iff `A.start <= B.end && B.start <= A.end`
- [ ] **Merge**: if current interval overlaps with last merged, extend its end; otherwise append

### Sweep Line
- [ ] Convert intervals to events: `(time, +1)` for start, `(time, -1)` for end
- [ ] Sort events and scan; track running count of active intervals
- [ ] Useful for: meeting rooms (max simultaneous), minimum platforms needed

### Insert Interval
- [ ] Skip intervals entirely before the new one (no overlap)
- [ ] Merge all overlapping intervals with the new one (extend new interval's bounds)
- [ ] Append the rest

### Non-Overlapping Intervals (Minimum Removals)
- [ ] Greedy: sort by end time; keep an interval only if it doesn't overlap with the last kept
- [ ] Count removals = total − kept

### Meeting Rooms II (Min Rooms)
- [ ] Sort start times and end times separately (two-pointer sweep)
- [ ] Or use a min-heap tracking end times of ongoing meetings

---

## Problems

| Status | Difficulty | Problem | Solution file |
|--------|------------|---------|---------------|
| [ ] | Easy   | [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) | `exercises/meeting-rooms.py` |
| [ ] | Medium | [Insert Interval](https://leetcode.com/problems/insert-interval/) | `exercises/insert-interval.py` |
| [ ] | Medium | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | `exercises/merge-intervals.py` |
| [ ] | Medium | [Non-Overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | `exercises/non-overlapping-intervals.py` |
| [ ] | Medium | [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | `exercises/meeting-rooms-ii.py` |
| [ ] | Hard   | [Minimum Interval to Include Each Query](https://leetcode.com/problems/minimum-interval-to-include-each-query/) | `exercises/minimum-interval-to-include-each-query.py` |
