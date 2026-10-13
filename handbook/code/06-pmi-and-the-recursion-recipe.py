"""06. PMI and the Recursion Recipe

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 06-pmi-and-the-recursion-recipe.py
"""

# Let the computer double-check the formula for a few thousand values of n.
for n in range(1, 3001):
    assert sum(range(1, n + 1)) == n * (n + 1) // 2
print("formula holds for n = 1 ... 3000")

depth = 0

def trace(fn):
    def wrapper(*args):
        global depth
        print("    " * depth + f"call   {fn.__name__}{args}")
        depth += 1
        result = fn(*args)
        depth -= 1
        print("    " * depth + f"return {fn.__name__}{args} -> {result}")
        return result
    return wrapper

@trace
def sum_to(n):
    if n == 0:                         # base case
        return 0
    small_answer = sum_to(n - 1)       # assume: this is 1 + ... + (n - 1)
    return n + small_answer            # my part: add n

sum_to(4)

def power(base, exponent):
    if exponent == 0:                          # base case: anything to the power 0 is 1
        return 1
    small_answer = power(base, exponent - 1)   # assume: base ** (exponent - 1)
    return base * small_answer                 # my part

print(power(2, 10), power(5, 0), power(3, 4))

def fast_power(base, exponent):
    if exponent == 0:
        return 1
    half = fast_power(base, exponent // 2)     # assume: base ** (exponent // 2)
    if exponent % 2 == 0:
        return half * half                     # even exponent: just square the half
    return half * half * base                  # odd exponent: one extra base

print(fast_power(2, 10), fast_power(3, 5), fast_power(2, 1000) == 2 ** 1000)

@trace
def count_digits(n):
    if n < 10:                              # base case: one digit left
        return 1
    small_answer = count_digits(n // 10)    # assume: digits of the number without its last digit
    return 1 + small_answer                 # my part

count_digits(2468)

def sum_of_digits(n):
    n = abs(n)                               # ignore a minus sign
    if n < 10:
        return n
    small_answer = sum_of_digits(n // 10)
    return n % 10 + small_answer

print(sum_of_digits(1234), sum_of_digits(0), sum_of_digits(-987), sum_of_digits(1_000_000_000))

@trace
def gcd(a, b):
    if b == 0:                    # base case
        return a
    return gcd(b, a % b)          # assume: this is the answer; my part: nothing more to do

gcd(48, 18)

print('\n[all code in this chapter ran successfully]')
