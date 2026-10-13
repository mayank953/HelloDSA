"""07. Fibonacci and Recursion Trees

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 07-fibonacci-and-recursion-trees.py
"""

def fib(n):
    if n <= 1:                 # base cases: F(0) = 0, F(1) = 1
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(n) for n in range(12)])

def print_tree(n, depth=0):
    print("    " * depth + f"fib({n})")
    if n <= 1:
        return n
    left = print_tree(n - 1, depth + 1)       # first child
    right = print_tree(n - 2, depth + 1)      # second child
    return left + right

print_tree(5)

calls = 0

def fib_counted(n):
    global calls
    calls += 1
    if n <= 1:
        return n
    return fib_counted(n - 1) + fib_counted(n - 2)

print(f"{'n':>3} | {'fib(n)':>8} | {'calls':>9}")
for n in [5, 10, 15, 20, 25]:
    calls = 0
    value = fib_counted(n)
    print(f"{n:>3} | {value:>8} | {calls:>9,}")

def fib_value(n):                     # a fast, loop-based Fibonacci for checking
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# number of calls for fib(n) is exactly  2 * F(n + 1) - 1
for n in [5, 10, 20]:
    calls = 0
    fib_counted(n)
    print(f"n={n:>2}: counted {calls:>6,} calls; formula 2*F(n+1)-1 = {2 * fib_value(n + 1) - 1:>6,}")

from collections import Counter

seen = Counter()

def fib_spy(n):
    seen[n] += 1
    if n <= 1:
        return n
    return fib_spy(n - 1) + fib_spy(n - 2)

fib_spy(10)
for n in range(10, -1, -1):
    print(f"fib({n:>2}) computed {seen[n]:>2} times  " + "#" * seen[n])

def fib_memo(n, notebook=None):
    if notebook is None:
        notebook = {}
    if n in notebook:                 # already answered? use it, no more calls below here
        return notebook[n]
    if n <= 1:
        notebook[n] = n
    else:
        notebook[n] = fib_memo(n - 1, notebook) + fib_memo(n - 2, notebook)
    return notebook[n]

print(fib_memo(50))
print(fib_memo(90))

calls = 0

def fib_memo_counted(n, notebook):
    global calls
    calls += 1
    if n in notebook:
        return notebook[n]
    notebook[n] = n if n <= 1 else fib_memo_counted(n - 1, notebook) + fib_memo_counted(n - 2, notebook)
    return notebook[n]

for n in [10, 20, 25, 30]:
    calls = 0
    fib_memo_counted(n, {})
    print(f"fib({n}): memoized version used {calls} calls")

from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n):
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

print(fib_cached(100))

def fib_loop(n):
    a, b = 0, 1                  # F(0), F(1)
    for _ in range(n):
        a, b = b, a + b          # slide the window forward by one
    return a

print(fib_loop(10), fib_loop(200))

def ways(n):
    if n <= 2:
        return n                      # 1 step: 1 way; 2 steps: 2 ways (1+1 or 2)
    return ways(n - 1) + ways(n - 2)

print([ways(n) for n in range(1, 11)])

print('\n[all code in this chapter ran successfully]')
