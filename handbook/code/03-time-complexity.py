"""03. Time Complexity: Counting the Work

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 03-time-complexity.py
"""

def first_item(items):
    steps = 1                      # one step: read items[0]
    return items[0], steps

def sum_all(items):
    steps, total = 0, 0
    for value in items:            # the loop body runs once per item
        total += value
        steps += 1
    return total, steps

def count_pairs(items):
    steps, pairs = 0, 0
    for a in items:                # outer loop: n times
        for b in items:            # inner loop: n times for EACH outer step
            pairs += 1
            steps += 1
    return pairs, steps

for n in [10, 100, 1000]:
    data = list(range(n))
    print(f"n={n:<5} first_item={first_item(data)[1]:<2} sum_all={sum_all(data)[1]:<5} count_pairs={count_pairs(data)[1]}")

import math

print(f"{'n':>9} | {'log2(n)':>8} | {'n':>9} | {'n*log2(n)':>11} | {'n^2':>15}")
print("-" * 62)
for n in [10, 100, 1_000, 100_000, 1_000_000]:
    print(f"{n:>9} | {math.log2(n):>8.1f} | {n:>9} | {n * math.log2(n):>11.0f} | {n * n:>15}")

print(f"{'n':>4} | {'2^n':>20} | {'n!':>22}")
print("-" * 52)
for n in [5, 10, 20, 25, 30]:
    print(f"{n:>4} | {2 ** n:>20,} | {math.factorial(n):>22,}")

def steps(n):
    return 3 * n * n + 5 * n + 2

print(f"{'n':>10} | {'3n^2+5n+2':>18} | {'steps / n^2':>12}")
for n in [10, 100, 1_000, 100_000, 1_000_000]:
    print(f"{n:>10} | {steps(n):>18,} | {steps(n) / n ** 2:>12.4f}")

def two_loops(items):
    steps = 0
    for _ in items:        # n steps
        steps += 1
    for _ in items:        # another n steps
        steps += 1
    return steps           # 2n  ->  O(n)

print(two_loops(list(range(1000))))

def triangle_pairs(n):
    steps = 0
    for i in range(n):
        for j in range(i + 1, n):     # the inner loop shrinks as i grows
            steps += 1
    return steps

print(triangle_pairs(1000), "vs n*n =", 1000 * 1000)

def halving_steps(n):
    steps = 0
    while n > 1:
        n //= 2           # throw away half of what is left
        steps += 1
    return steps

for n in [8, 1024, 1_000_000, 1_000_000_000]:
    print(f"n = {n:>13,}: {halving_steps(n)} halvings")

def linear_search_steps(items, target):
    steps = 0
    for value in items:
        steps += 1
        if value == target:
            break
    return steps

n = 1000
data = list(range(n))
print("best case  (first item) :", linear_search_steps(data, 0))
print("worst case (last item)  :", linear_search_steps(data, n - 1))
print("worst case (not present):", linear_search_steps(data, -5))

average = sum(linear_search_steps(data, t) for t in data) / n
print("average over every position:", average)

def bubble_sort_comparisons(items):
    items = items[:]                      # work on a copy
    comparisons = 0
    for end in range(len(items) - 1, 0, -1):
        for i in range(end):
            comparisons += 1
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return comparisons

for n in [10, 100, 1000]:
    print(f"n={n:<5} comparisons={bubble_sort_comparisons(list(range(n, 0, -1))):>8}   n(n-1)/2={n * (n - 1) // 2}")

def merge_sort_comparisons(items):
    """Returns (sorted list, number of comparisons made while merging)."""
    if len(items) <= 1:
        return items[:], 0
    mid = len(items) // 2
    left, c1 = merge_sort_comparisons(items[:mid])
    right, c2 = merge_sort_comparisons(items[mid:])
    merged, i, j, comparisons = [], 0, 0, 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged += left[i:] + right[j:]
    return merged, c1 + c2 + comparisons

for n in [1024, 4096, 16384]:
    data = [(i * 7919) % n for i in range(n)]      # a scrambled but reproducible list
    _, c = merge_sort_comparisons(data)
    print(f"n={n:<6} merge sort comparisons={c:>8}   n*log2(n)={n * int(math.log2(n)):>8}   bubble would need {n * (n - 1) // 2:>10}")

def insertion_sort_comparisons(items):
    items = items[:]
    comparisons = 0
    for i in range(1, len(items)):
        j = i
        while j > 0:
            comparisons += 1
            if items[j - 1] > items[j]:
                items[j - 1], items[j] = items[j], items[j - 1]
                j -= 1
            else:
                break
    return comparisons

n = 1000
print("already sorted :", insertion_sort_comparisons(list(range(n))))
print("reverse sorted :", insertion_sort_comparisons(list(range(n, 0, -1))))

calls = 0

def factorial(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return n * factorial(n - 1)

factorial(50)
print("calls for n = 50:", calls)      # one call per number: O(n)

calls = 0
def fib(n):
    global calls
    calls += 1
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

for n in [10, 15, 20, 25]:
    calls = 0
    fib(n)
    print(f"fib({n}) needed {calls:>7,} calls")

print('\n[all code in this chapter ran successfully]')
