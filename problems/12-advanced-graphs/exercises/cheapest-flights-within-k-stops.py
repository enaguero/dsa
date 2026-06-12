"""
Problem: Cheapest Flights Within K Stops
Difficulty: Medium
Category: Advanced Graphs
LeetCode: https://leetcode.com/problems/cheapest-flights-within-k-stops/
Status: Stub

Approach:
- TODO: describe the approach

Time Complexity: O(?)
Space Complexity: O(?)
"""


from typing import List


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # TODO: implement
        pass


if __name__ == "__main__":
    sol = Solution()
    print(sol.findCheapestPrice(4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1))
    print(sol.findCheapestPrice(3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 1))
    print(sol.findCheapestPrice(3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 0))
