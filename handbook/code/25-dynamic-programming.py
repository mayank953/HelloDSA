"""25. Dynamic Programming

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 25-dynamic-programming.py
"""

from functools import lru_cache

@lru_cache(maxsize=None)
def ways_top_down(n):                       # recursion + notebook
    if n <= 2:
        return n
    return ways_top_down(n - 1) + ways_top_down(n - 2)

def ways_bottom_up(n):                      # fill a table from the base cases upward
    if n <= 2:
        return n
    table = [0] * (n + 1)
    table[1], table[2] = 1, 2
    for step in range(3, n + 1):
        table[step] = table[step - 1] + table[step - 2]
    return table[n]

def ways_two_variables(n):                  # we only ever look back two steps: keep just those
    if n <= 2:
        return n
    previous, current = 1, 2
    for _ in range(n - 2):
        previous, current = current, previous + current
    return current

print(ways_top_down(40), ways_bottom_up(40), ways_two_variables(40))

def rob(houses):
    best = [0] * (len(houses) + 1)
    if houses:
        best[1] = houses[0]
    for i in range(2, len(houses) + 1):
        best[i] = max(best[i - 1], best[i - 2] + houses[i - 1])    # leave it, or take it
    return best[-1]

def rob_compact(houses):
    skip, take = 0, 0                                               # best up to two houses ago / one ago
    for money in houses:
        skip, take = take, max(take, skip + money)
    return take

print(rob([2, 7, 9, 3, 1]), rob_compact([2, 7, 9, 3, 1]), rob([]), rob([5]))

def greedy_coins(coins, amount):
    count = 0
    for coin in sorted(coins, reverse=True):
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1

print("greedy for 6 with [1, 3, 4]:", greedy_coins([1, 3, 4], 6), "coins   (4 + 1 + 1)")

def min_coins(coins, amount):
    INF = float("inf")
    fewest = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for coin in coins:                               # which coin was the LAST one used?
            if coin <= a and fewest[a - coin] + 1 < fewest[a]:
                fewest[a] = fewest[a - coin] + 1
    return fewest[amount] if fewest[amount] != INF else -1

print(min_coins([1, 3, 4], 6), min_coins([2], 3), min_coins([1, 2, 5], 11), min_coins([5], 0))

def count_ways(coins, amount):
    ways = [1] + [0] * amount                     # one way to make 0: use no coins
    for coin in coins:                            # coins OUTSIDE: each combination is counted once
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]
    return ways[amount]

print(count_ways([1, 2, 5], 5), count_ways([2], 3), count_ways([1, 3, 4], 6))

def knapsack(items, capacity):
    best = [[0] * (capacity + 1) for _ in range(len(items) + 1)]
    for i, (weight, value) in enumerate(items, start=1):
        for w in range(capacity + 1):
            best[i][w] = best[i - 1][w]                              # leave item i
            if weight <= w:                                          # or take it, if it fits
                best[i][w] = max(best[i][w], value + best[i - 1][w - weight])
    return best[len(items)][capacity], best

items = [(1, 1), (3, 4), (4, 5), (5, 7)]
value, table = knapsack(items, 7)
print("best value:", value)
for row in table:
    print(row)

def knapsack_one_row(items, capacity):
    best = [0] * (capacity + 1)
    for weight, value in items:
        for w in range(capacity, weight - 1, -1):          # BACKWARDS: each item used at most once
            best[w] = max(best[w], value + best[w - weight])
    return best[capacity]

print(knapsack_one_row(items, 7))

def can_partition(numbers):
    total = sum(numbers)
    if total % 2:
        return False
    reachable = {0}                                  # sums we can make so far
    for x in numbers:
        reachable |= {s + x for s in reachable}      # for each item: leave it, or add it to every sum
    return total // 2 in reachable

print(can_partition([1, 5, 11, 5]), can_partition([1, 2, 3, 5]))

def lcs(a, b):
    rows, cols = len(a) + 1, len(b) + 1
    table = [[0] * cols for _ in range(rows)]
    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:
                table[i][j] = 1 + table[i - 1][j - 1]
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    # walk back through the table to recover one actual LCS
    i, j, letters = len(a), len(b), []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            letters.append(a[i - 1]); i -= 1; j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return table[-1][-1], "".join(reversed(letters)), table

length, text, table = lcs("ABCBDAB", "BDCABA")
print(length, text)
print("     " + "  ".join(" " + c for c in "BDCABA"))
for letter, row in zip(" " + "ABCBDAB", table):
    print(letter, row)

def edit_distance(a, b):
    rows, cols = len(a) + 1, len(b) + 1
    edit = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        edit[i][0] = i                                  # delete everything
    for j in range(cols):
        edit[0][j] = j                                  # insert everything
    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:
                edit[i][j] = edit[i - 1][j - 1]
            else:
                edit[i][j] = 1 + min(edit[i - 1][j - 1],    # replace
                                     edit[i - 1][j],        # delete
                                     edit[i][j - 1])        # insert
    return edit[-1][-1]

print(edit_distance("kitten", "sitting"), edit_distance("horse", "ros"), edit_distance("", "abc"), edit_distance("same", "same"))

def lis_quadratic(numbers):
    if not numbers:
        return 0
    longest = [1] * len(numbers)
    for i in range(len(numbers)):
        for j in range(i):
            if numbers[j] < numbers[i]:
                longest[i] = max(longest[i], longest[j] + 1)
    return max(longest)

print(lis_quadratic([10, 9, 2, 5, 3, 7, 101, 18]))

import bisect

def lis_fast(numbers):
    tails = []
    for x in numbers:
        position = bisect.bisect_left(tails, x)       # the first tail that is >= x
        if position == len(tails):
            tails.append(x)                            # x extends the longest sequence found so far
        else:
            tails[position] = x                        # x is a better (smaller) ending for that length
    return len(tails)

print(lis_fast([10, 9, 2, 5, 3, 7, 101, 18]))

def unique_paths(grid):
    rows, cols = len(grid), len(grid[0])
    paths = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                continue                                   # a wall: 0 ways
            if r == 0 and c == 0:
                paths[r][c] = 1
            else:
                from_above = paths[r - 1][c] if r > 0 else 0
                from_left = paths[r][c - 1] if c > 0 else 0
                paths[r][c] = from_above + from_left
    return paths[-1][-1]

print(unique_paths([[0, 0, 0], [0, 1, 0], [0, 0, 0]]), unique_paths([[0] * 5 for _ in range(5)]))

def min_path_sum(costs):
    rows, cols = len(costs), len(costs[0])
    best = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                best[r][c] = costs[0][0]
            else:
                options = []
                if r > 0: options.append(best[r - 1][c])
                if c > 0: options.append(best[r][c - 1])
                best[r][c] = costs[r][c] + min(options)
    return best[-1][-1]

print(min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))

print('\n[all code in this chapter ran successfully]')
