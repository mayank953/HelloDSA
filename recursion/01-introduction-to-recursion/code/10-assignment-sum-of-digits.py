"""
Problem: Sum of Digits in a Number

Given an integer n, calculate the sum of its digits.

Example 1:
Input: n = 123
Output: 6
Explanation: 1 + 2 + 3 = 6

Example 2:
Input: n = 54321
Output: 15
Explanation: 5 + 4 + 3 + 2 + 1 = 15

Example 3:
Input: n = 0
Output: 0
Explanation: The sum of digits in 0 is 0.

Note:
- The input number can be positive, negative, or zero.
- For negative numbers, ignore the minus sign and sum the digits of the absolute value.

Constraints:
-10^9 <= n <= 10^9

Function Signature:
def sum_of_digits(n: int) -> int:

Your task is to implement the sum_of_digits function.
"""

def sum_of_digits(n):
    # Your code here
    pass

# Test cases
def test_sum_of_digits():
    assert sum_of_digits(123) == 6, "Test case 1 failed"
    assert sum_of_digits(54321) == 15, "Test case 2 failed"
    assert sum_of_digits(0) == 0, "Test case 3 failed"
    assert sum_of_digits(-123) == 6, "Test case 4 failed"
    assert sum_of_digits(1000000000) == 1, "Test case 5 failed"
    print("All test cases passed!")

if __name__ == "__main__":
    test_sum_of_digits()
