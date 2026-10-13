"""24. Binary Search Beyond Sorted Arrays

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 24-binary-search-beyond.py
"""

def first_true(low, high, is_true):
    answer = high + 1                          # "none are true" until we find one
    while low <= high:
        mid = low + (high - low) // 2
        if is_true(mid):
            answer = mid                       # mid works: remember it, but look for an earlier one
            high = mid - 1
        else:
            low = mid + 1                      # mid is too small: the answer must be later
    return answer

print(first_true(0, 100, lambda x: x * x >= 50))      # the first x whose square is at least 50

def lower_bound(items, x):
    return first_true(0, len(items) - 1, lambda i: items[i] >= x)

def upper_bound(items, x):
    return first_true(0, len(items) - 1, lambda i: items[i] > x)

data = [1, 2, 2, 2, 3, 5, 5, 8]
print("lower_bound(2) =", lower_bound(data, 2), "  upper_bound(2) =", upper_bound(data, 2))
print("how many 2s?   =", upper_bound(data, 2) - lower_bound(data, 2))
print("where would 4 be inserted?", lower_bound(data, 4))

import bisect
print(bisect.bisect_left(data, 2), bisect.bisect_right(data, 2))

def search_rotated(items, target):          # items have distinct values
    low, high = 0, len(items) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if items[mid] == target:
            return mid
        if items[low] <= items[mid]:                         # the left half is sorted
            if items[low] <= target < items[mid]:
                high = mid - 1                               # the target lies in the sorted left half
            else:
                low = mid + 1
        else:                                                # the right half is sorted
            if items[mid] < target <= items[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1

rotated = [4, 5, 6, 7, 0, 1, 2]
print(search_rotated(rotated, 0), search_rotated(rotated, 5), search_rotated(rotated, 3))

def rotated_minimum(items):
    low, high = 0, len(items) - 1
    while low < high:                          # note: <, because we keep `high = mid`
        mid = low + (high - low) // 2
        if items[mid] > items[high]:
            low = mid + 1                      # the smallest is strictly to the right
        else:
            high = mid                         # mid could be the smallest: keep it in range
    return items[low]

print(rotated_minimum([4, 5, 6, 7, 0, 1, 2]), rotated_minimum([1, 2, 3]), rotated_minimum([2]))

def find_peak(items):
    low, high = 0, len(items) - 1
    while low < high:
        mid = low + (high - low) // 2
        if items[mid] < items[mid + 1]:
            low = mid + 1                      # still climbing: a peak is ahead
        else:
            high = mid
    return low

print(find_peak([1, 3, 20, 4, 1, 0]), find_peak([5, 4, 3]))

def integer_sqrt(n):
    return first_true(0, n, lambda x: (x + 1) * (x + 1) > n)

print([integer_sqrt(n) for n in [0, 1, 8, 9, 10, 99, 100]], integer_sqrt(10 ** 18))

import math

def min_eating_speed(piles, hours):
    def can_finish(speed):
        return sum(math.ceil(pile / speed) for pile in piles) <= hours
    return first_true(1, max(piles), can_finish)

print(min_eating_speed([3, 6, 7, 11], 8), min_eating_speed([30, 11, 23, 4, 20], 5), min_eating_speed([30, 11, 23, 4, 20], 6))

def ship_within_days(weights, days):
    def can_ship(capacity):
        needed, load = 1, 0
        for weight in weights:
            if load + weight > capacity:           # does not fit today: start a new day
                needed += 1
                load = 0
            load += weight
        return needed <= days
    return first_true(max(weights), sum(weights), can_ship)

print(ship_within_days(list(range(1, 11)), 5), ship_within_days([3, 2, 2, 4, 1, 4], 3))

calls = 0

def counted_check(speed):
    global calls
    calls += 1
    return sum(math.ceil(pile / speed) for pile in piles) <= hours

piles = [(i * 7919) % 100_000 + 1 for i in range(200)]       # 200 piles of up to 100,000 bananas
hours = 400
best = first_true(1, max(piles), counted_check)
print(f"slowest speed: {best} bananas/hour, found with only {calls} yes/no questions (the range had {max(piles):,} values)")

def real_sqrt(x, precision=1e-9):
    low, high, steps = 0.0, max(1.0, x), 0
    while high - low > precision:
        mid = (low + high) / 2
        if mid * mid >= x:
            high = mid                    # mid is big enough: the root is at mid or below
        else:
            low = mid
        steps += 1
    return high, steps

value, steps = real_sqrt(2)
print(f"sqrt(2) is about {value:.9f}, found after {steps} halvings")

print('\n[all code in this chapter ran successfully]')
