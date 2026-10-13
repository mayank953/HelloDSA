"""04. Space Complexity: Counting the Memory

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 04-space-complexity.py
"""

def total_in_one_variable(numbers):
    total = 0                    # ONE extra variable, however long the list is
    for value in numbers:
        total += value
    return total                 # auxiliary space: O(1)

def doubled_copy(numbers):
    result = []                  # a new list that grows with the input
    for value in numbers:
        result.append(value * 2)
    return result                # auxiliary space: O(n)

print(total_in_one_variable([1, 2, 3, 4]))
print(doubled_copy([1, 2, 3, 4]))

def reversed_copy(items):
    return items[::-1]                         # O(n) extra space: a whole new list

def reverse_in_place(items):
    left, right = 0, len(items) - 1
    while left < right:                        # swap from both ends, no new list
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1                             # O(1) extra space

numbers = [1, 2, 3, 4, 5]
reverse_in_place(numbers)
print(numbers)

current_depth = 0
deepest = 0

def factorial(n):
    global current_depth, deepest
    current_depth += 1                       # a new frame was just created
    deepest = max(deepest, current_depth)
    result = 1 if n <= 1 else n * factorial(n - 1)
    current_depth -= 1                       # this frame is about to disappear
    return result

for n in [5, 50, 500]:
    current_depth = deepest = 0
    factorial(n)
    print(f"factorial({n}): deepest stack = {deepest} frames")

def binary_search_depth(numbers, target, low, high, depth=1):
    if low > high:
        return depth
    mid = (low + high) // 2
    if numbers[mid] == target:
        return depth
    if numbers[mid] < target:
        return binary_search_depth(numbers, target, mid + 1, high, depth + 1)
    return binary_search_depth(numbers, target, low, mid - 1, depth + 1)

for n in [1_000, 1_000_000]:
    data = list(range(n))
    print(f"n={n:>9,}: binary search recursion depth for a missing item = {binary_search_depth(data, -1, 0, n - 1)}")

def sum_with_slicing(items, tracker):
    tracker["alive"] += len(items)                       # this frame holds `items`
    tracker["peak"] = max(tracker["peak"], tracker["alive"])
    if len(items) == 0:
        result = 0
    else:
        result = items[0] + sum_with_slicing(items[1:], tracker)   # items[1:] is a NEW list
    tracker["alive"] -= len(items)
    return result

for n in [10, 100, 500]:       # (1000 would hit Python's recursion limit: another cost of deep recursion)
    tracker = {"alive": 0, "peak": 0}
    sum_with_slicing(list(range(n)), tracker)
    print(f"n={n:>5}: peak items held across all frames = {tracker['peak']:>8,}   (n*(n+1)/2 = {n * (n + 1) // 2:,})")

def sum_with_index(items, i=0):
    if i == len(items):
        return 0
    return items[i] + sum_with_index(items, i + 1)    # nothing copied: same list, new index

def fib_plain(n, counter):
    counter[0] += 1
    if n <= 1:
        return n
    return fib_plain(n - 1, counter) + fib_plain(n - 2, counter)

def fib_memo(n, counter, memo=None):
    if memo is None:
        memo = {}
    counter[0] += 1
    if n in memo:
        return memo[n]
    memo[n] = n if n <= 1 else fib_memo(n - 1, counter, memo) + fib_memo(n - 2, counter, memo)
    return memo[n]

for n in [10, 20, 25]:
    plain, memo = [0], [0]
    fib_plain(n, plain)
    fib_memo(n, memo)
    print(f"fib({n}): plain used {plain[0]:>7,} calls, memoized used {memo[0]:>3} calls")

print('\n[all code in this chapter ran successfully]')
