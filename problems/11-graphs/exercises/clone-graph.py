"""
Problem: Clone Graph
Difficulty: Medium
Category: Graphs
LeetCode: https://leetcode.com/problems/clone-graph/
Status: Stub

Approach:
- TODO: describe the approach

Time Complexity: O(?)
Space Complexity: O(?)
"""


from typing import Optional


"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        # TODO: implement
        pass


if __name__ == "__main__":
    sol = Solution()
    print(sol.cloneGraph([[2,4],[1,3],[2,4],[1,3]]))
    print(sol.cloneGraph([[]]))
    print(sol.cloneGraph([]))
