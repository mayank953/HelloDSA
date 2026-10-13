# 26. Greedy Algorithms

**Part 4: Algorithms** · Intermediate · about 10 minutes to read

> Pick the best-looking choice at every step, when that is provably enough, and when it quietly fails.
**Run the code from this chapter:** [`code/26-greedy.py`](code/26-greedy.py)  

---

## The strategy of never looking back

Imagine you are hiking in thick fog and want to reach the top of a hill. You cannot see far, so at every step you do the obvious thing: **walk in the steepest upward direction**. You never plan ahead and never undo a step.

Sometimes that gets you to the summit. Sometimes it leaves you on a small bump, because the real peak needed you to go downhill first.

That is a **greedy algorithm**:

> **At every step, make the choice that looks best right now, and never reconsider it.**

Compare with what we have done so far:

| Technique | How it treats choices |
|---|---|
| **Backtracking** (chapter 13) | Tries a choice, and **undoes it** if it fails |
| **Dynamic programming** (chapter 25) | Considers **all** choices, remembering sub-results |
| **Greedy** | Picks **one** choice and **commits** |

Committing is what makes greedy algorithms **fast and simple** (often just a sort and one pass). It is also what makes them **dangerous**: a greedy algorithm is only correct when the problem has a special property. The whole skill of this chapter is knowing **when** greedy is allowed.

---

## When greedy works, and when it fails

Greedy is correct when:

1. **Greedy-choice property.** A locally best choice can always be extended to a globally optimal solution. (Picking the best-looking option now never *ruins* the chance of an optimal answer.)
2. **Optimal substructure.** What remains after the choice is a smaller problem of the same kind.

Consider the **coin change** problem from chapter 25: make an amount with the fewest coins. For *everyday* coins (1, 5, 10, 25 cents) "take the largest coin that fits" is correct. For coins `[1, 3, 4]` and amount 6 it is **wrong**:

```python
def greedy_coin_count(coins, amount):
    count = 0
    for coin in sorted(coins, reverse=True):          # always take the biggest coin that fits
        count += amount // coin
        amount %= coin
    return count

print("coins 1, 5, 10, 25 for 63 cents:", greedy_coin_count([1, 5, 10, 25], 63), "coins")     # 25+25+10+1+1+1
print("coins 1, 3, 4 for 6            :", greedy_coin_count([1, 3, 4], 6), "coins   (but 3 + 3 uses only 2!)")
```

**Output**

```text
coins 1, 5, 10, 25 for 63 cents: 6 coins
coins 1, 3, 4 for 6            : 3 coins   (but 3 + 3 uses only 2!)
```

The same strategy is right for one coin system and wrong for another. **Greedy is not a "try it and see" tool.** The rule:

> **Never trust a greedy idea until you have either a proof or a counterexample hunt.** In an interview, say out loud: *"Let me try to break this with a small example."*


---

## How to prove a greedy choice: the exchange argument

The most common proof is the **exchange argument**: *take any optimal solution; show you can swap its first choice for the greedy choice without making it worse.* Then the greedy choice is "safe". We will see one in action in the first problem.

---

## Problem 1: scheduling the most meetings

**Story.** One meeting room, many requests, each with a start and an end time. Which meetings should you accept so that **the most of them** fit, with no two overlapping?

Intervals: `(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)`.

There are several tempting greedy ideas:

1. Take the **earliest start** first.
2. Take the **shortest** meeting first.
3. Take the meeting that **ends earliest** first.

Only one of them is right. Let us test all three against a brute-force answer that tries every possible set of meetings:

```python
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
```

**Output**

```text
optimal for the trap case: 2
  earliest start: 1 meetings
shortest meeting: 2 meetings
 earliest finish: 2 meetings
```

Sorting by **earliest start** takes the long meeting and ruins everything. Sorting by **earliest finish** wins. Let us confirm on many random cases, to see whether the other two fail *and* whether "earliest finish" ever does:

```python
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
```

**Output**

```text
{'earliest start': 49, 'shortest meeting': 8, 'earliest finish': 0}
```

**Earliest finish never fails**; the other two do. Why? **The exchange argument:** take any optimal schedule. Look at its first meeting. The greedy choice (the meeting that finishes earliest of all) ends no later than that one. So we can *swap* the greedy meeting in as the first meeting: it still leaves just as much time for the rest, so the schedule is no worse. Therefore some optimal schedule starts with the greedy choice, and the same argument repeats for what remains.

```python
def max_meetings(intervals):
    count, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):      # earliest finish first
        if start >= last_end:                                       # does it start after the last one ended?
            count += 1
            last_end = end
    return count

meetings = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
print(max_meetings(meetings))
```

**Output**

```text
4
```

**Cost.** Sorting dominates: **O(n log n)**; then one pass.


---

## Problem 2: the fractional knapsack versus the 0/1 knapsack

Remember the knapsack from chapter 25? You pack a backpack of capacity `W`, each item has a weight and value. There it was **0/1**: take an item whole or not at all, and we needed DP.

Now change one rule: you may take **a fraction** of an item (think of gold dust or flour). The greedy rule becomes natural: **take items with the best value per kilogram first.**

```python
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
```

**Output**

```text
fractional: 240.0
```

Now the **same greedy rule on the 0/1 version** (no fractions) goes wrong:

```python
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
```

**Output**

```text
0/1 greedy by ratio: 160   0/1 true optimum (DP): 220
```

Greedy picks the 10 kg and 20 kg items (160) and then cannot fit the 30 kg one, whereas taking the 20 kg and 30 kg items gives 220. **The ability to take a fraction is exactly what makes the greedy choice safe**, which is a great example of how a tiny change in the rules flips the answer from "greedy works" to "need DP".


---

## Problem 3: can I reach the end? (jump game)

**Question.** `jumps[i]` is the farthest you may jump from position `i`. Starting at index 0, can you reach the last index? `[2, 3, 1, 1, 4]` → yes. `[3, 2, 1, 0, 4]` → no (you always get stuck at the 0).

**Greedy.** Keep track of the **farthest index reachable** so far. Walk forward; if you are standing on a position beyond that frontier, you are stuck. Otherwise, extend the frontier.

```python
def can_reach_end(jumps):
    farthest = 0
    for i, reach in enumerate(jumps):
        if i > farthest:                        # this position cannot be reached at all
            return False
        farthest = max(farthest, i + reach)
    return True

print(can_reach_end([2, 3, 1, 1, 4]), can_reach_end([3, 2, 1, 0, 4]))
```

**Output**

```text
True False
```

**Minimum number of jumps** (assuming the end is reachable). Think in **levels**, like BFS (chapter 17): the first jump covers positions `1..jumps[0]`; the second jump covers everything reachable from *those*; and so on. Count how many "levels" it takes to cover the end.

```python
def min_jumps(jumps):
    count, level_end, farthest = 0, 0, 0
    for i in range(len(jumps) - 1):
        farthest = max(farthest, i + jumps[i])
        if i == level_end:                      # we are at the edge of the current jump's range
            count += 1                          # we must jump again...
            level_end = farthest                # ...to the farthest place seen so far
    return count

print(min_jumps([2, 3, 1, 1, 4]), min_jumps([1, 1, 1, 1]), min_jumps([5]))
```

**Output**

```text
2 3 0
```


---

## Problem 4: the gas station tour

**Story.** `n` petrol stations on a circular road. Station `i` sells `gas[i]` litres, and driving to the next station costs `cost[i]` litres. Starting with an empty tank, **which station lets you complete the full circle**? (At most one answer.)

`gas = [1, 2, 3, 4, 5]`, `cost = [3, 4, 5, 1, 2]` → start at station 3.

**Two greedy observations:**

1. If the **total** gas is less than the **total** cost, nobody can finish: return `-1`.
2. Otherwise, walk once keeping a running tank. The moment the tank goes **negative** at station `i`, *none* of the stations from the current start up to `i` can be the answer (they would all run dry at the same spot or earlier), so **restart from `i + 1`**.

```python
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
```

**Output**

```text
3 -1
```

One pass, **O(n)**, instead of trying every start in O(n²).


---

## Problem 5: Huffman coding, the greedy heap

**Story.** To store text compactly, give **frequent letters short codes** and rare letters long ones. Morse code does this: `E` is a single dot, `Q` is long. Huffman's algorithm builds the best possible such code, using a greedy rule and a **heap** from chapter 21:

> **Repeatedly take the two least frequent items and merge them into one node whose frequency is their sum.** Repeat until one tree remains. The path from the root (left = `0`, right = `1`) is each letter's code.

Rare letters get merged first, so they end up deepest in the tree, with the longest codes.

```python
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
```

**Output**

```text
a -> 0
b -> 110
c -> 100
d -> 101
r -> 111
11 letters, fixed 3 bits each = 33 bits;  Huffman = 23 bits
```

The most frequent letter, `a` (5 of 11 letters), gets the shortest code.

**Decoding is unambiguous** because **no code is the beginning of another** (a *prefix-free* code): you read bits until they match a code, output the letter, and start over.

```python
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
```

**Output**

```text
abracadabra
```


---

## Problem 6: minimum spanning tree (Kruskal)

**Story.** Connect several towns with roads (or cables) so that **every town is reachable** and the **total length is as small as possible**. You need only `n − 1` roads (more would form a cycle, which is wasteful).

**Kruskal's greedy rule.** Sort all possible roads by length. Go through them from **shortest to longest**; **add a road if it connects two towns that are not yet connected** (skip it if it would close a cycle). We check "already connected?" with the **Union-Find** structure from chapter 22.

```python
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
```

**Output**

```text
(7, [('A', 'B', 1), ('B', 'C', 2), ('C', 'D', 4)])
```

The road `A-C` (length 3) was skipped because `A` and `C` were already connected through `B`. **Cost:** sorting, `O(E log E)`. (Dijkstra, from chapter 22, is also a greedy algorithm: it always finalises the closest unfinished node.)


---

## Greedy versus dynamic programming

| | **Greedy** | **Dynamic programming** |
|---|---|---|
| Choices | Commits to one and moves on | Explores all and remembers sub-answers |
| Speed | Usually O(n) or O(n log n) | Usually O(n²) or more |
| Correct when | The greedy-choice property holds (needs a proof) | Optimal substructure and overlapping subproblems |
| Typical example | Earliest-finish scheduling, Huffman, Kruskal | Knapsack, edit distance, LCS |
| Danger | A plausible-looking idea that is wrong | Getting the state or the order wrong |

**A practical workflow:**

1. Think of a greedy idea. Say it in one sentence.
2. **Try to break it** with 3 to 5 tiny examples. Ties, duplicates, and "a big item that looks attractive" are the usual culprits.
3. If it survives, try an **exchange argument** (or at least write a brute force and compare on random small inputs, as we did above).
4. If it breaks, you probably need DP.

---

## Common mistakes

- **Trusting a greedy rule because it works on the given example.** Always hunt for counterexamples.
- **Sorting by the wrong key** (earliest start instead of earliest finish).
- **Ignoring ties**: when two choices look equally good, the order you pick can matter.
- **Using greedy on a 0/1 problem** (knapsack) when fractions are not allowed.
- **Confusing "locally best" with "globally best".**
- **Forgetting to prove or test** the greedy choice, and being unable to defend it in an interview.

---

## Practice

1. 🟢 *Assign cookies:* children with greed factors and cookies with sizes; feed as many children as possible.
2. 🟢 *Maximum number of items you can buy* with a budget (sort by price).
3. 🟡 *Minimum number of platforms* needed for a railway station given arrival and departure times (sort the events, or use a heap).
4. 🟡 *Minimum arrows to burst balloons* (intervals on a line).
5. 🟡 *Merge intervals* and *insert an interval* (greedy with sorting).
6. 🟡 *Task scheduler with cooldown:* arrange tasks so the same one is not repeated within `n` slots.
7. 🔴 *Candy:* children in a row with ratings, each needs at least one candy and more than a lower-rated neighbour. Minimum candies (two greedy passes).
8. 🔴 Find a coin system where greedy is optimal for **every** amount, and one where it fails. Why do "canonical" coin systems work?
9. 🔴 Implement **Prim's algorithm** with a heap and compare with Kruskal.

<details>
<summary>Hints</summary>

1. Sort both lists; give each child the smallest cookie that satisfies them.
3. Sweep over the sorted arrival and departure times: +1 when a train arrives, −1 when one leaves; the answer is the peak.
4. Sort by end coordinate; shoot an arrow at the end of the first balloon, skipping all that overlap it.
7. One pass left to right (compare with the left neighbour), one pass right to left (compare with the right neighbour); take the maximum at each position.
</details>

---

[← 25. Dynamic Programming](25-dynamic-programming.md) · [Handbook contents](README.md) · [27. Patterns and the Interview Playbook →](27-patterns-and-interview-playbook.md)
