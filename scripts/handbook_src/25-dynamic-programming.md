## The most feared topic, and why you are ready for it

Dynamic programming (DP) has a reputation. People treat it as a separate, mysterious subject. It is not. **If you understood chapters 6, 7 and 12, you already know 90% of it.**

Here is the whole idea in one sentence:

> **Dynamic programming is recursion that refuses to solve the same problem twice.**

In chapter 7, naive Fibonacci made billions of calls because the *same* questions (`fib(10)`, `fib(9)`, ...) were asked again and again. We fixed it with a **notebook of answers**. That was DP. Everything in this chapter is the same move on different problems.

### When does DP apply?

Two conditions, and both must hold:

1. **Overlapping subproblems.** The recursion asks the *same* smaller question many times. (If every smaller question is different, there is nothing to remember: that is plain divide and conquer, like merge sort.)
2. **Optimal substructure.** The best answer for the whole problem is built from the best answers of smaller pieces.

There are **two ways** to write a DP solution. They give the same answers:

| | **Top-down (memoization)** | **Bottom-up (tabulation)** |
|---|---|---|
| How | Write the recursion, add a notebook | Fill a table from the smallest case upward, with loops |
| Feels like | "Natural" recursion plus a dictionary | Building a staircase one step at a time |
| Good for | Getting a correct solution quickly; only solves the subproblems it needs | Speed, no recursion limit, easy space optimisation |
| Watch out for | Recursion depth | Getting the loop order right |

---

## The Hello DSA method for DP

When a problem looks like DP, do these five steps *in order*, writing each one down:

1. **Define the state in words.** *"`dp[i]` is the best answer for the first `i` items"*, or *"`dp[i][j]` is the answer for the first `i` letters of A and the first `j` letters of B"*. This sentence is 80% of the work.
2. **Find the recurrence.** Ask: *what was the last decision?* (Take the item or leave it? Which coin was used last?) Express the state in terms of **smaller states**. This is the *"assume the smaller problem is solved, do your part"* of chapter 6.
3. **Base cases.** The smallest states that need no recursion.
4. **Choose the order.** Top-down (recursion plus notebook) or bottom-up (a loop that fills smaller states first).
5. **Answer and cost.** Which state is the final answer? Complexity = **(number of states) × (work per state)**. Can you keep only the last row or two to save space?

We will use these five steps on every problem below.

---

## Problem 1: climbing stairs (a warm-up you have already solved)

**State.** `ways(n)` is the number of ways to climb `n` steps with 1- or 2-steps.
**Recurrence.** The last move was a 1-step (from `n − 1`) or a 2-step (from `n − 2`), so `ways(n) = ways(n − 1) + ways(n − 2)`.
**Base.** `ways(1) = 1`, `ways(2) = 2`.

```python
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
```

Look at the three versions. **Same recurrence, three implementations.** The last also shows the **space optimisation**: each state depends only on the previous two, so we throw away the rest of the table (O(n) space becomes O(1)).

```python hide
assert all(ways_top_down(n) == ways_bottom_up(n) == ways_two_variables(n) for n in range(1, 30))
assert ways_two_variables(5) == 8
```

---

## Problem 2: house robber (take it or leave it)

**Story.** A thief walks down a street of houses, each holding some cash. Robbing **two adjacent houses** sets off the alarm. What is the most money the thief can take?

`nums = [2, 7, 9, 3, 1]`. Robbing 7 and 3 gives 10; robbing 2, 9, 1 gives 12, which is the best.

**State.** `best[i]` = the most money from the **first `i` houses**.
**Recurrence.** Think about house `i` (the last one). **Take it or leave it** (chapter 11's wedding buffet again!):

- **Leave** it: the best we can do is `best[i − 1]`.
- **Take** it: we get its cash plus the best from the first `i − 2` houses (we skipped the neighbour): `nums[i − 1] + best[i − 2]`.

`best[i] = max(best[i − 1], best[i − 2] + nums[i − 1])`.
**Base.** `best[0] = 0` (no houses), `best[1] = nums[0]`.

```python
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
```

```python hide
import random
rng = random.Random(25)
def rob_brute(h, i=0):
    if i >= len(h): return 0
    return max(rob_brute(h, i + 1), h[i] + rob_brute(h, i + 2))
for _ in range(100):
    h = [rng.randint(0, 9) for _ in range(rng.randint(0, 12))]
    assert rob(h) == rob_compact(h) == rob_brute(h)
```

---

## Problem 3: coin change (the one where greedy fails)

**Story.** A cashier must give change for `amount` using the **fewest coins**. Coins `[1, 3, 4]`, amount `6`.

A natural first idea is **greedy**: always take the biggest coin that fits. Let us test it.

```python
def greedy_coins(coins, amount):
    count = 0
    for coin in sorted(coins, reverse=True):
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1

print("greedy for 6 with [1, 3, 4]:", greedy_coins([1, 3, 4], 6), "coins   (4 + 1 + 1)")
```

Greedy says 3 coins (`4 + 1 + 1`). But `3 + 3` is **two** coins. Greedy fails here, so we need to consider all the choices carefully: **DP**.

**State.** `fewest[a]` = the fewest coins needed to make amount `a`.
**Recurrence.** Think about the **last coin** used. It could be any coin `c` with `c <= a`. Then the rest, `a − c`, must itself be made with the fewest coins: `fewest[a] = 1 + min(fewest[a − c] for each coin c)`.
**Base.** `fewest[0] = 0`. Amounts that cannot be made stay at "infinity".

```python
def min_coins(coins, amount):
    INF = float("inf")
    fewest = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for coin in coins:                               # which coin was the LAST one used?
            if coin <= a and fewest[a - coin] + 1 < fewest[a]:
                fewest[a] = fewest[a - coin] + 1
    return fewest[amount] if fewest[amount] != INF else -1

print(min_coins([1, 3, 4], 6), min_coins([2], 3), min_coins([1, 2, 5], 11), min_coins([5], 0))
```

**Cost.** `amount` states, each trying `len(coins)` coins: **O(amount × coins)**.

### How many *ways* to make the amount?

A tiny change answers a different question: *in how many different ways can we make `amount`?* The same recurrence, but **add** instead of taking a minimum. The loop order matters: put the **coins in the outer loop** so that `1 + 3` and `3 + 1` count as **one** combination (not two orderings).

```python
def count_ways(coins, amount):
    ways = [1] + [0] * amount                     # one way to make 0: use no coins
    for coin in coins:                            # coins OUTSIDE: each combination is counted once
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]
    return ways[amount]

print(count_ways([1, 2, 5], 5), count_ways([2], 3), count_ways([1, 3, 4], 6))
```

```python hide
assert greedy_coins([1, 3, 4], 6) == 3 and min_coins([1, 3, 4], 6) == 2
assert min_coins([2], 3) == -1 and min_coins([1, 2, 5], 11) == 3 and min_coins([5], 0) == 0
assert count_ways([1, 2, 5], 5) == 4 and count_ways([2], 3) == 0 and count_ways([1, 3, 4], 6) == 4
from itertools import combinations_with_replacement
def ways_brute(coins, amount):
    total = 0
    for k in range(amount + 1):
        total += sum(1 for combo in combinations_with_replacement(coins, k) if sum(combo) == amount)
    return total
assert all(count_ways([1, 3, 4], a) == ways_brute([1, 3, 4], a) for a in range(0, 13))
```

---

## Problem 4: the 0/1 knapsack

**Story.** You are packing a backpack for a trek that can carry at most `W` kilograms. Each item has a **weight** and a **value**. You may take each item **at most once** ("0/1": take it or leave it). Maximise the total value.

Items `(weight, value)`: `(1, 1), (3, 4), (4, 5), (5, 7)` and capacity `W = 7`.

**State.** `best[i][w]` = the best value using only the **first `i` items** with capacity `w`.
**Recurrence.** Item `i`: **leave it** (`best[i − 1][w]`) or, if it fits, **take it** (`value + best[i − 1][w − weight]`). Choose the larger.
**Base.** With no items (`i = 0`) or no capacity (`w = 0`) the value is 0.

```python
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
```

Each row is "after considering one more item". The bottom-right cell is the answer. **Cost: O(items × capacity)**.

**Space optimisation.** Row `i` only needs row `i − 1`, so one row is enough *if we update capacities from high to low* (so that an item is not used twice):

```python
def knapsack_one_row(items, capacity):
    best = [0] * (capacity + 1)
    for weight, value in items:
        for w in range(capacity, weight - 1, -1):          # BACKWARDS: each item used at most once
            best[w] = max(best[w], value + best[w - weight])
    return best[capacity]

print(knapsack_one_row(items, 7))
```

```python hide
from itertools import combinations
def knapsack_brute(items, capacity):
    best = 0
    for r in range(len(items) + 1):
        for combo in combinations(items, r):
            if sum(w for w, _ in combo) <= capacity:
                best = max(best, sum(v for _, v in combo))
    return best
assert value == 9 == knapsack_brute(items, 7)
rng = random.Random(26)
for _ in range(100):
    its = [(rng.randint(1, 6), rng.randint(1, 9)) for _ in range(rng.randint(0, 8))]
    cap = rng.randint(0, 15)
    assert knapsack(its, cap)[0] == knapsack_one_row(its, cap) == knapsack_brute(its, cap)
```

A close cousin: **can we split a list into two groups with equal sums?** That is knapsack asking "is a subset summing to `total / 2` reachable?"

```python
def can_partition(numbers):
    total = sum(numbers)
    if total % 2:
        return False
    reachable = {0}                                  # sums we can make so far
    for x in numbers:
        reachable |= {s + x for s in reachable}      # for each item: leave it, or add it to every sum
    return total // 2 in reachable

print(can_partition([1, 5, 11, 5]), can_partition([1, 2, 3, 5]))
```

```python hide
assert can_partition([1, 5, 11, 5]) and not can_partition([1, 2, 3, 5]) and can_partition([])
```

---

## Problem 5: longest common subsequence (LCS)

**Story.** A diff tool compares two versions of a file; a biologist compares two DNA strands. Both ask: *what is the longest sequence of characters that appears, in order (not necessarily adjacent), in both strings?* (Remember subsequences from chapter 11.) For `"ABCBDAB"` and `"BDCABA"` one answer is `BCBA`, length 4.

**State.** `lcs[i][j]` = the LCS length of the **first `i` letters of A** and the **first `j` letters of B**.
**Recurrence.** Look at the last letters, `A[i − 1]` and `B[j − 1]`:

- If they are **equal**, that letter is part of the answer: `1 + lcs[i − 1][j − 1]`.
- If **different**, one of them is not used: `max(lcs[i − 1][j], lcs[i][j − 1])`.

**Base.** If either string is empty, the LCS is 0.

```python
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
```

Every cell depends on at most three neighbours (left, up, up-left). **Cost: O(m × n)** time and space (O(min(m, n)) space if you only need the length).

```python hide
length2, text2, _ = lcs("ABCBDAB", "BDCABA")
def is_subsequence(small, big):
    it = iter(big); return all(ch in it for ch in small)
assert length == 4 and len(text) == 4 and is_subsequence(text, "ABCBDAB") and is_subsequence(text, "BDCABA")
def lcs_brute(a, b):
    if not a or not b: return 0
    if a[-1] == b[-1]: return 1 + lcs_brute(a[:-1], b[:-1])
    return max(lcs_brute(a[:-1], b), lcs_brute(a, b[:-1]))
for x, y in [("", "abc"), ("abc", "abc"), ("abcdef", "acf"), ("aggtab", "gxtxayb"), ("xyz", "abc")]:
    assert lcs(x, y)[0] == lcs_brute(x, y)
```

---

## Problem 6: edit distance (autocorrect)

**Story.** Your phone's autocorrect decides whether "recieve" is close to "receive". The **edit distance** between two words is the **fewest single-letter edits** (insert, delete, replace) that turn one into the other. `"kitten" → "sitting"` takes 3: replace `k→s`, replace `e→i`, insert `g`.

**State.** `edit[i][j]` = the fewest edits to turn the **first `i` letters of A** into the **first `j` letters of B**.
**Recurrence.** Look at the last letters:

- **Equal:** no cost, `edit[i − 1][j − 1]`.
- **Different:** pay 1 for the cheapest of three moves:
  - **replace** the last letter: `edit[i − 1][j − 1]`
  - **delete** from A: `edit[i − 1][j]`
  - **insert** into A: `edit[i][j − 1]`

**Base.** Turning `i` letters into nothing needs `i` deletions; building `j` letters from nothing needs `j` insertions.

```python
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
```

```python hide
assert edit_distance("kitten", "sitting") == 3 and edit_distance("horse", "ros") == 3
assert edit_distance("", "abc") == 3 and edit_distance("abc", "") == 3 and edit_distance("same", "same") == 0
def edit_brute(a, b):
    if not a: return len(b)
    if not b: return len(a)
    if a[-1] == b[-1]: return edit_brute(a[:-1], b[:-1])
    return 1 + min(edit_brute(a[:-1], b[:-1]), edit_brute(a[:-1], b), edit_brute(a, b[:-1]))
for x, y in [("ab", "ba"), ("flaw", "lawn"), ("intention", "execution"[:6]), ("abc", "yabd")]:
    assert edit_distance(x, y) == edit_brute(x, y)
```

---

## Problem 7: longest increasing subsequence (LIS)

**Question.** The longest subsequence of a list whose values strictly increase. For `[10, 9, 2, 5, 3, 7, 101, 18]` it is `[2, 3, 7, 18]`, length 4.

**State.** `longest[i]` = the length of the longest increasing subsequence that **ends exactly at item `i`**.
**Recurrence.** Look back at every earlier item `j < i` that is **smaller** than item `i`: we can extend its sequence. `longest[i] = 1 + max(longest[j])` over those `j` (or 1 if none).

```python
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
```

**O(n²).** Notice how the answer is *not* the last cell, but the maximum over all of them, because the best sequence can end anywhere.

Combine DP with **binary search** (chapter 24) to get **O(n log n)**: keep a list `tails` where `tails[k]` is the **smallest possible last value** of an increasing subsequence of length `k + 1`. For each number, binary-search its place in `tails`: either it extends the longest sequence, or it replaces a larger tail (keeping tails as small as possible, which gives the most room to extend later).

```python
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
```

(`tails` is *not* itself the subsequence; it only tracks lengths.)

```python hide
assert lis_quadratic([10, 9, 2, 5, 3, 7, 101, 18]) == lis_fast([10, 9, 2, 5, 3, 7, 101, 18]) == 4
assert lis_quadratic([]) == lis_fast([]) == 0
for _ in range(200):
    data = [rng.randint(0, 15) for _ in range(rng.randint(0, 20))]
    assert lis_quadratic(data) == lis_fast(data)
```

---

## Problem 8: paths in a grid

**Question.** A robot starts at the top-left of a grid and may only move **right or down**. Cells marked `1` are blocked. How many different paths reach the bottom-right?

**State.** `paths[r][c]` = the number of ways to reach cell `(r, c)`.
**Recurrence.** You can only arrive from above or from the left: `paths[r][c] = paths[r − 1][c] + paths[r][c − 1]`, or `0` if the cell is blocked.
**Base.** `paths[0][0] = 1` (if it is open).

```python
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
```

The same grid with *costs* gives the **minimum path sum**: take the **min** of the two ways in instead of adding.

```python
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
```

Look back at chapter 13's maze: that **backtracking** enumerated every path (exponential). Here DP only **counts** them, in `O(rows × cols)`. When the question is "how many?" or "what is the best?" rather than "list them all", DP usually wins.

```python hide
assert unique_paths([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2 and unique_paths([[0] * 5 for _ in range(5)]) == 70
assert unique_paths([[1]]) == 0 and unique_paths([[0]]) == 1
assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7 and min_path_sum([[5]]) == 5
```

---

## How do I know it is DP?

| Clue in the question | Likely state |
|---|---|
| "Number of ways to...", "can we reach...", "minimum / maximum cost to..." | `dp[i]` over a prefix or a target amount |
| Take or leave each item (subset-like) | `dp[i]` or `dp[i][capacity]` |
| Two strings or two sequences | `dp[i][j]` over a prefix of each |
| A grid, moving right/down | `dp[r][c]` |
| The brute-force recursion repeats the same arguments | Memoize those arguments |

**Quick test:** write the plain recursion first and **draw its tree** (chapter 7). If you see the same node (same arguments) appearing more than once, memoize it. The arguments that vary are your state.

---

## Complexity: states times work

| Problem | States | Work per state | Time | Space (compact) |
|---|---|---|---|---|
| Stairs / Fibonacci | n | O(1) | O(n) | O(1) |
| House robber | n | O(1) | O(n) | O(1) |
| Coin change | amount | O(coins) | O(amount · coins) | O(amount) |
| 0/1 knapsack | items × capacity | O(1) | O(items · capacity) | O(capacity) |
| LCS / edit distance | m × n | O(1) | O(m · n) | O(min(m, n)) |
| LIS | n | O(n) (O(log n) with tails) | O(n²) (O(n log n)) | O(n) |
| Grid paths | rows × cols | O(1) | O(rows · cols) | O(cols) |

> **A subtle warning.** Knapsack's `O(items × capacity)` looks polynomial, but the capacity is a *number*, and its size in memory is only `log(capacity)` digits. So the running time is "pseudo-polynomial": fine for a capacity of a few thousand, impossible for one of 10²⁰.

---

## Common mistakes

- **Skipping step 1.** If you cannot say in one sentence what `dp[i]` *means*, stop and think.
- **Wrong loop order or direction** (the 1D knapsack must go **backwards**; counting combinations needs coins in the **outer** loop).
- **Missing base cases**, or off-by-one indexing between "first `i` items" (`dp[i]`) and the item at index `i − 1`.
- **Mutable default** (`memo={}`) shared across calls in top-down code.
- **Recursion too deep** for top-down on large inputs: switch to bottom-up.
- **Forgetting the answer may not be the last cell** (LIS takes the maximum over all of them).
- **Using DP when greedy is enough** (or greedy where DP is needed; see chapter 26).

---

## Practice

1. 🟢 *Min cost climbing stairs:* each step has a cost; you may start on step 0 or 1 and climb 1 or 2 at a time.
2. 🟢 *Tribonacci:* each term is the sum of the previous three.
3. 🟡 *Perfect squares:* the fewest perfect squares that sum to `n` (a coin-change in disguise).
4. 🟡 *Decode ways:* count the digit-string decodings (you built it in chapter 12; compare).
5. 🟡 *Word break:* can a string be split into dictionary words?
6. 🟡 *Longest palindromic subsequence* (hint: LCS of the string and its reverse).
7. 🟡 *Maximum product subarray* (track the maximum **and** minimum ending here).
8. 🔴 *Longest palindromic substring* with DP, then with the "expand around the centre" trick. Which is simpler?
9. 🔴 *Matrix chain multiplication* or *burst balloons* (interval DP).
10. 🔴 *Rod cutting* and *unbounded knapsack* (compare with 0/1: what changes in the loop?).

<details>
<summary>Hints</summary>

3. `fewest[n] = 1 + min(fewest[n − k*k])` over all squares `k*k <= n`.
5. `can[i]` = can the first `i` letters be split? It is true if some `j < i` has `can[j]` true and `s[j:i]` is a word.
7. A negative times a negative is positive, so remember the smallest product too.
10. Unbounded knapsack goes **forwards** through capacities (an item can be reused); 0/1 goes backwards.
</details>
