# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Purpose

This is a Data Structures and Algorithms (DSA) study repository, organized around the NeetCode 150 problem set. The repository is structured for practicing coding interview problems across various algorithmic topics.

## Directory Structure

```
neetcode/neetcode_150/
├── 01_arrays_and_hashing/
├── 02_two_pointers/
├── 03_sliding_window/
├── 04_stack/
├── 05_binary_search/
├── 06_linked_list/
├── 07_trees/
├── 08_tries/
├── 09_heap_priority_queue/
├── 10_backtracking/
├── 11_graphs/
├── 12_advanced_graphs/
├── 13_1d_dynamic_programming/
├── 14_2d_dynamic_programming/
├── 15_greedy/
├── 16_intervals/
├── 17_math_and_geometry/
└── 18_bit_manipulation/
```

Each directory corresponds to a specific algorithmic topic category from the NeetCode 150 list.

## Working with Solutions

### File Naming Convention
When creating solution files, use descriptive names that include:
- Problem difficulty (easy/medium/hard)
- Problem name (snake_case)
- File extension appropriate for the language

Example: `medium_group_anagrams.py`, `easy_two_sum.js`

### Solution File Structure
Each solution should include:
1. Problem description/link (as comment at top)
2. Time and space complexity analysis
3. Approach explanation
4. Implementation
5. Test cases (if applicable)

### Language Support
This repository can contain solutions in any programming language. When adding solutions:
- Keep language-specific solutions in the appropriate topic directory
- Use consistent naming conventions within each language
- Include language-specific test commands if testing framework is set up

## Common Commands

### Testing Solutions
Since no test framework is currently configured, you'll need to run individual files directly:

**Python:**
```bash
python3 neetcode/neetcode_150/01_arrays_and_hashing/solution_name.py
```

**JavaScript/Node:**
```bash
node neetcode/neetcode_150/01_arrays_and_hashing/solution_name.js
```

**Java:**
```bash
javac neetcode/neetcode_150/01_arrays_and_hashing/SolutionName.java
java -cp neetcode/neetcode_150/01_arrays_and_hashing SolutionName
```

### Finding Solutions by Topic
```bash
# List all solutions in a topic
ls neetcode/neetcode_150/01_arrays_and_hashing/

# Search for a specific problem
find neetcode/neetcode_150 -name "*two_sum*"

# Count solutions per topic
for dir in neetcode/neetcode_150/*/; do echo "$(basename "$dir"): $(ls -1 "$dir" 2>/dev/null | wc -l)"; done
```

## Working on Problems

### Adding New Solutions
1. Identify the appropriate topic directory
2. Create file with descriptive name
3. Include problem context and complexity analysis
4. Implement solution with clear variable names
5. Add test cases or examples

### Code Review Focus Areas
- Time and space complexity accuracy
- Edge case handling
- Code clarity and readability
- Alternative approaches documented
