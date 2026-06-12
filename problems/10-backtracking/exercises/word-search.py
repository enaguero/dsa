"""
Problem: Word Search
Difficulty: Medium
Category: Backtracking
LeetCode: https://leetcode.com/problems/word-search/
Status: Stub

Approach:
- TODO: describe the approach

Time Complexity: O(?)
Space Complexity: O(?)
"""


from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        # TODO: implement
        pass


if __name__ == "__main__":
    sol = Solution()
    print(sol.exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED"))
    print(sol.exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE"))
    print(sol.exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB"))
