"""
Problem: Max Area of Island
Difficulty: Medium
Category: Graphs
LeetCode: https://leetcode.com/problems/max-area-of-island/
Status: Stub

Approach:
- TODO: describe the approach

Time Complexity: O(?)
Space Complexity: O(?)
"""


from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        # TODO: implement
        pass


if __name__ == "__main__":
    sol = Solution()
    print(sol.maxAreaOfIsland([[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]))
    print(sol.maxAreaOfIsland([[0,0,0,0,0,0,0,0]]))
