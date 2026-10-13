"""
Problem: Calculate Power of a Number

Given two non-negative integers 'base' and 'exponent', calculate 'base' raised to the power of 'exponent' using recursion.

Example 1:
Input: base = 2, exponent = 3
Output: 8
Explanation: 2^3 = 2 * 2 * 2 = 8

Example 2:
Input: base = 5, exponent = 0
Output: 1
Explanation: Any number raised to the power of 0 is 1.

Example 3:
Input: base = 3, exponent = 4
Output: 81
Explanation: 3^4 = 3 * 3 * 3 * 3 = 81

Note:
- Both base and exponent are non-negative integers.
- You must use recursion to solve this problem.
- Do not use the built-in power function or operator.

Constraints:
0 <= base <= 100
0 <= exponent <= 1000

Function Signature:
def power(base: int, exponent: int) -> int:

Your task is to implement the power function using recursion.
"""

def power(base: int, exponent: int) -> int:
    # Your code here
    pass

# Test cases
def test_power():
    assert power(2, 3) == 8, "Test case 1 failed"
    assert power(5, 0) == 1, "Test case 2 failed"
    assert power(3, 4) == 81, "Test case 3 failed"
    assert power(10, 2) == 100, "Test case 4 failed"
    assert power(7, 1) == 7, "Test case 5 failed"
    print("All test cases passed!")

if __name__ == "__main__":
    test_power()

# LeetCode link: https://leetcode.com/problems/powx-n/ (Note: The LeetCode problem is a more complex variation of this question)
