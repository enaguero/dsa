"""
Problem: Course Schedule II
Difficulty: Medium
Category: Graphs
LeetCode: https://leetcode.com/problems/course-schedule-ii/
Status: Stub

Approach:
- TODO: describe the approach

Time Complexity: O(?)
Space Complexity: O(?)
"""


from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # TODO: implement
        pass


if __name__ == "__main__":
    sol = Solution()
    print(sol.findOrder(2, [[1,0]]))
    print(sol.findOrder(4, [[1,0],[2,0],[3,1],[3,2]]))
    print(sol.findOrder(1, []))
