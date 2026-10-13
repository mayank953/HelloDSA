"""26. Greedy Algorithms

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 26-greedy.py
"""

def greedy_coin_count(coins, amount):
    count = 0
    for coin in sorted(coins, reverse=True):          # always take the biggest coin that fits
        count += amount // coin
        amount %= coin
    return count

print("coins 1, 5, 10, 25 for 63 cents:", greedy_coin_count([1, 5, 10, 25], 63), "coins")     # 25+25+10+1+1+1
print("coins 1, 3, 4 for 6            :", greedy_coin_count([1, 3, 4], 6), "coins   (but 3 + 3 uses only 2!)")

from itertools import combinations

def pick(intervals, key):
    """Greedy: sort by `key`, then take every meeting that does not overlap the ones already taken."""
    chosen = []
    for start, end in sorted(intervals, key=key):
        if all(end <= s or start >= e for s, e in chosen):
            chosen.append((start, end))
    return len(chosen)

def best_possible(intervals):
    """Brute force: try every subset, keep the largest one with no overlaps."""
    best = 0
    for size in range(len(intervals) + 1):
        for subset in combinations(intervals, size):
            if all(a[1] <= b[0] or b[1] <= a[0] for a, b in combinations(subset, 2)):
                best = max(best, size)
    return best

strategies = {
    "earliest start": lambda iv: iv[0],
    "shortest meeting": lambda iv: iv[1] - iv[0],
    "earliest finish": lambda iv: iv[1],
}

traps = [(0, 10), (1, 2), (3, 4)]                      # a long meeting that starts first
print("optimal for the trap case:", best_possible(traps))
for name, key in strategies.items():
    print(f"{name:>16}: {pick(traps, key)} meetings")

import random
rng = random.Random(7)
failures = {name: 0 for name in strategies}
for _ in range(300):
    ivs = []
    for _ in range(rng.randint(1, 8)):
        start = rng.randint(0, 12)
        ivs.append((start, start + rng.randint(1, 6)))
    optimum = best_possible(ivs)
    for name, key in strategies.items():
        if pick(ivs, key) != optimum:
            failures[name] += 1
print(failures)

def max_meetings(intervals):
    count, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):      # earliest finish first
        if start >= last_end:                                       # does it start after the last one ended?
            count += 1
            last_end = end
    return count

meetings = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
print(max_meetings(meetings))

def fractional_knapsack(items, capacity):
    total = 0.0
    for weight, value in sorted(items, key=lambda it: it[1] / it[0], reverse=True):   # best value per kg first
        if capacity >= weight:
            total += value                       # take it all
            capacity -= weight
        else:
            total += value * capacity / weight   # take just the fraction that fits, then stop
            break
    return total

things = [(10, 60), (20, 100), (30, 120)]       # (weight, value)
print("fractional:", fractional_knapsack(things, 50))

def greedy_01(items, capacity):
    total = 0
    for weight, value in sorted(items, key=lambda it: it[1] / it[0], reverse=True):
        if weight <= capacity:
            total += value
            capacity -= weight
    return total

def best_01(items, capacity):
    best = [0] * (capacity + 1)
    for weight, value in items:
        for w in range(capacity, weight - 1, -1):
            best[w] = max(best[w], value + best[w - weight])
    return best[capacity]

print("0/1 greedy by ratio:", greedy_01(things, 50), "  0/1 true optimum (DP):", best_01(things, 50))

def can_reach_end(jumps):
    farthest = 0
    for i, reach in enumerate(jumps):
        if i > farthest:                        # this position cannot be reached at all
            return False
        farthest = max(farthest, i + reach)
    return True

print(can_reach_end([2, 3, 1, 1, 4]), can_reach_end([3, 2, 1, 0, 4]))

def min_jumps(jumps):
    count, level_end, farthest = 0, 0, 0
    for i in range(len(jumps) - 1):
        farthest = max(farthest, i + jumps[i])
        if i == level_end:                      # we are at the edge of the current jump's range
            count += 1                          # we must jump again...
            level_end = farthest                # ...to the farthest place seen so far
    return count

print(min_jumps([2, 3, 1, 1, 4]), min_jumps([1, 1, 1, 1]), min_jumps([5]))

def gas_station(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start, tank = 0, 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                        # we ran dry: start over from the next station
            start, tank = i + 1, 0
    return start

print(gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), gas_station([2, 3, 4], [3, 4, 3]))

import heapq, itertools
from collections import Counter

def huffman_codes(text):
    tiebreaker = itertools.count()                       # so the heap never compares two trees
    heap = [(count, next(tiebreaker), letter) for letter, count in Counter(text).items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        count_a, _, tree_a = heapq.heappop(heap)         # the two rarest...
        count_b, _, tree_b = heapq.heappop(heap)
        heapq.heappush(heap, (count_a + count_b, next(tiebreaker), (tree_a, tree_b)))   # ...merged

    codes = {}
    def assign(tree, prefix):
        if isinstance(tree, str):
            codes[tree] = prefix or "0"                  # a one-letter text still needs one bit
        else:
            assign(tree[0], prefix + "0")
            assign(tree[1], prefix + "1")
    assign(heap[0][2], "")
    return codes

text = "abracadabra"
codes = huffman_codes(text)
for letter, code in sorted(codes.items()):
    print(letter, "->", code)

encoded = "".join(codes[ch] for ch in text)
print(f"{len(text)} letters, fixed 3 bits each = {len(text) * 3} bits;  Huffman = {len(encoded)} bits")

def decode(bits, codes):
    reverse = {code: letter for letter, code in codes.items()}
    result, current = [], ""
    for bit in bits:
        current += bit
        if current in reverse:               # a complete code: emit its letter
            result.append(reverse[current])
            current = ""
    return "".join(result)

print(decode(encoded, codes))

class UnionFind:
    def __init__(self, items):
        self.parent = {x: x for x in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        self.parent[root_b] = root_a
        return True

def kruskal(towns, roads):
    union_find = UnionFind(towns)
    chosen, total = [], 0
    for a, b, length in sorted(roads, key=lambda road: road[2]):      # shortest first
        if union_find.union(a, b):                                    # connects two separate groups: keep it
            chosen.append((a, b, length))
            total += length
    return total, chosen

roads = [("A", "B", 1), ("B", "C", 2), ("A", "C", 3), ("C", "D", 4), ("B", "D", 5)]
print(kruskal("ABCD", roads))

print('\n[all code in this chapter ran successfully]')
