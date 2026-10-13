# 24. Binary Search Beyond Sorted Arrays

**Part 4: Algorithms** · Advanced · about 8 minutes to read

> Lower and upper bound, rotated arrays, and binary search on the answer.
**In this repo:** [Binary search with recursion](../recursion/03-searching-and-sorting/)  
**Run the code from this chapter:** [`code/24-binary-search-beyond.py`](code/24-binary-search-beyond.py)  

---

## What binary search really needs

In chapter 10 you saw binary search find a number in a **sorted list** by halving the range. Most people leave it there: "binary search = look for something in a sorted array."

That description is too small. Look at what the algorithm *actually* uses. At each step it asks **one yes/no question** about the middle position (*"is the middle too small?"*), and the answer lets it discard **half** of the possibilities. Nothing in that needs an array. It needs only this:

> **A yes/no question whose answers go `NO, NO, NO, ..., NO, YES, YES, ..., YES`.** (Once the answer flips to YES, it stays YES.) We call such a question **monotone**.

Where the answer flips from NO to YES is a **boundary**, and binary search finds a boundary in `log n` questions, whether the "positions" are array indexes, numbers from 1 to a billion, or speeds, capacities, or even real numbers.

This chapter has three parts: a **universal template**, a family of **array variations** (duplicates, rotation), and **"binary search on the answer"**, one of the most powerful tricks in interviews.

---

## One template to rule them all

**Goal:** given a monotone question `is_true(x)` over the integers from `low` to `high` (`False, False, ..., True, True`), find the **first** `x` where it is `True`. If none, say `high + 1`.

```python
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
```

**Output**

```text
8
```

Three details make this template safe, and once you memorise it you can stop worrying about off-by-one errors:

1. When `is_true(mid)` holds, `mid` is **a candidate**: store it, then search the **left** side for something even earlier (`high = mid - 1`).
2. When it does not hold, `mid` and everything before it are ruled out (`low = mid + 1`).
3. The loop condition is `low <= high`, and every step shrinks the range, so it **always terminates**.

---

## Variations on a sorted array

### Lower bound and upper bound

For a sorted list there are two standard questions, and each is just the template with a different yes/no:

- **Lower bound** (`bisect_left`): the **first index** whose value is **`>= x`**. Question: *"is `items[i] >= x`?"*
- **Upper bound** (`bisect_right`): the **first index** whose value is **`> x`**.

```python
def lower_bound(items, x):
    return first_true(0, len(items) - 1, lambda i: items[i] >= x)

def upper_bound(items, x):
    return first_true(0, len(items) - 1, lambda i: items[i] > x)

data = [1, 2, 2, 2, 3, 5, 5, 8]
print("lower_bound(2) =", lower_bound(data, 2), "  upper_bound(2) =", upper_bound(data, 2))
print("how many 2s?   =", upper_bound(data, 2) - lower_bound(data, 2))
print("where would 4 be inserted?", lower_bound(data, 4))
```

**Output**

```text
lower_bound(2) = 1   upper_bound(2) = 4
how many 2s?   = 3
where would 4 be inserted? 5
```

Both are O(log n). The **count** of a value is just `upper_bound − lower_bound`, and the **first** and **last** positions of a value fall out too. (Python's `bisect` module provides these two as `bisect_left` and `bisect_right`.)

```python
import bisect
print(bisect.bisect_left(data, 2), bisect.bisect_right(data, 2))
```

**Output**

```text
1 4
```


### Search in a rotated sorted array

A sorted list `[1, 2, 3, 4, 5, 6, 7]` was **rotated** by some amount to `[4, 5, 6, 7, 1, 2, 3]`. Find a target in O(log n).

It is not sorted any more, but here is the key observation: **if you split it at the middle, at least one half is still perfectly sorted.** So at each step:

1. Figure out which half is sorted (compare the ends).
2. Ask: *is the target inside the sorted half's range?* If yes, go there. If not, go to the other half.

```python
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
```

**Output**

```text
4 1 -1
```

### The minimum of a rotated array (the pivot)

Compare the middle to the **last** element: if `items[mid] > items[high]`, the drop (and therefore the minimum) is to the **right** of `mid`; otherwise the minimum is at `mid` or to its left.

```python
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
```

**Output**

```text
0 1 2
```

### A peak element

A **peak** is an item bigger than its neighbours. In any list (even unsorted!) one exists. Compare `items[mid]` to `items[mid + 1]`: if the right neighbour is bigger, a peak must exist on the right (climb up); otherwise one exists at `mid` or to the left.

```python
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
```

**Output**

```text
2 0
```


---

## Binary search on the answer

Here is the big idea. Suppose a problem asks for the **smallest (or largest) value of something** that makes some condition true, **and** if a value works then every bigger value works too. (Or the reverse.) Then:

1. The answer lies in a **range of numbers**.
2. You can write a function `works(x)`, "does this value succeed?", which is **monotone** (`False ... False True ... True`).
3. So **binary search the range** using `works` as the question!

You do not search a list; you search the *space of possible answers*. Even if the answer could be up to a billion, `works` is called only about 30 times.

### Example 1: integer square root

**Question.** The integer square root of `n`: the largest `x` with `x·x ≤ n`. (Without `math.sqrt`.)

The question *"is `(x + 1)² > n`?"* is monotone in `x`, so the answer is the **first** `x` for which it is true.

```python
def integer_sqrt(n):
    return first_true(0, n, lambda x: (x + 1) * (x + 1) > n)

print([integer_sqrt(n) for n in [0, 1, 8, 9, 10, 99, 100]], integer_sqrt(10 ** 18))
```

**Output**

```text
[0, 1, 2, 3, 3, 9, 10] 1000000000
```

For `n = 10¹⁸` that is about 60 questions instead of a billion.


### Example 2: eating bananas (the minimum speed)

**Question.** A monkey has piles of bananas, `piles = [3, 6, 7, 11]`, and `h = 8` hours. Each hour it picks **one pile** and eats up to `speed` bananas from it (a pile smaller than `speed` takes the full hour anyway). What is the **slowest speed** that finishes everything within `h` hours?

**The monotone question.** *"Can the monkey finish at speed `s`?"* If speed `s` works, a faster speed works too. So `works(s)` is `False ... False True ... True`, and we need the **first `True`**.

Computing `works(s)` is easy: the time for a pile is `ceil(pile / s)`.

```python
import math

def min_eating_speed(piles, hours):
    def can_finish(speed):
        return sum(math.ceil(pile / speed) for pile in piles) <= hours
    return first_true(1, max(piles), can_finish)

print(min_eating_speed([3, 6, 7, 11], 8), min_eating_speed([30, 11, 23, 4, 20], 5), min_eating_speed([30, 11, 23, 4, 20], 6))
```

**Output**

```text
4 30 23
```

The speed lies between `1` and `max(piles)`, and we do about `log(max(piles))` checks, each costing O(n). Total **O(n log max)**, instead of trying every speed.

### Example 3: shipping packages within D days

**Question.** Packages with weights `[1, 2, ..., 10]` must be shipped **in order**, a ship carrying a fixed capacity per day. Find the **smallest capacity** that ships everything in at most `days` days.

**The range.** The capacity is at least `max(weights)` (or the heaviest package never ships) and at most `sum(weights)` (everything in one day).

**`works(capacity)`:** load packages greedily, starting a new day when the next one does not fit, and see whether the number of days is within the limit. Bigger capacity never needs more days, so it is monotone.

```python
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
```

**Output**

```text
15 6
```

This exact structure solves "**split an array into k parts to minimise the largest sum**", "allocate books to students", "painter's partition", and many more with different stories. Spot the pattern: **minimise the maximum** (or maximise the minimum) is almost always binary search on the answer.


### Counting the questions

Is it really that few? Let us count `works` calls for a big range:

```python
calls = 0

def counted_check(speed):
    global calls
    calls += 1
    return sum(math.ceil(pile / speed) for pile in piles) <= hours

piles = [(i * 7919) % 100_000 + 1 for i in range(200)]       # 200 piles of up to 100,000 bananas
hours = 400
best = first_true(1, max(piles), counted_check)
print(f"slowest speed: {best} bananas/hour, found with only {calls} yes/no questions (the range had {max(piles):,} values)")
```

**Output**

```text
slowest speed: 33060 bananas/hour, found with only 16 yes/no questions (the range had 99,820 values)
```


### Real numbers

The same idea works for real numbers: instead of `low = mid + 1`, we move to `mid` and **stop when the range is tiny**. For example, the square root of 2:

```python
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
```

**Output**

```text
sqrt(2) is about 1.414213562, found after 31 halvings
```


---

## How to spot a binary-search-on-the-answer problem

Ask yourself:

1. Is the thing I am looking for a **number** I can range over (a speed, a capacity, a time, a distance, a size)?
2. Can I write a **checking function** `works(x)` that answers "is `x` enough?" in reasonable time (usually O(n))?
3. Is it **monotone**: if `x` works, does every larger (or every smaller) value work too?

If all three are yes, binary search the answer. Typical wording: *"minimum time/speed/capacity such that..."*, *"maximum possible minimum distance..."*, *"smallest value for which it is possible to..."*.

---

## Common mistakes

- **A non-monotone question.** If `works(x)` is not `False...False True...True`, binary search silently gives wrong answers.
- **Off-by-one in the search range**: forgetting that the true answer can be `max(weights)` (not 1) or `high + 1` ("none").
- **Infinite loops** when `low < high` is combined with `low = mid` (or `high = mid - 1`). With `low = mid`, round `mid` up; with `high = mid`, round down and use `low < high`.
- **Integer overflow** in other languages for `(low + high) / 2`: write `low + (high - low) / 2`.
- **Forgetting that the answer variable must be stored** when `is_true(mid)` succeeds (the template's `answer = mid`).
- **Searching an unsorted array** with a plain binary search.

---

## Practice

1. 🟢 Find the number of times a value appears in a sorted list in O(log n).
2. 🟢 Find the **first bad version** in `1..n` given an `is_bad(version)` function that is monotone.
3. 🟡 Search in a rotated array that may contain **duplicates**. What gets worse?
4. 🟡 *Koko with fractions:* modify the banana problem so speeds may be non-integers.
5. 🟡 **Capacity to ship** with a different goal: given a capacity, what is the *minimum number of days*?
6. 🟡 Find the **median of two sorted arrays** in O(log(min(m, n))).
7. 🔴 *Aggressive cows / magnetic force:* place `k` items in positions so that the **smallest gap is as large as possible**.
8. 🔴 Find the **k-th smallest element** in a sorted matrix (binary search on the value, counting how many entries are ≤ it).
9. 🔴 *Split array largest sum* (minimise the largest part when splitting into k parts).

<details>
<summary>Hints</summary>

1. `upper_bound(x) − lower_bound(x)`.
3. When `items[low] == items[mid] == items[high]` you cannot tell which half is sorted, so you must shrink by one: the worst case degrades to O(n).
7. Binary search the *gap* `d`: greedily place items at least `d` apart and count how many fit; bigger `d` fits fewer, so it is monotone.
8. For a candidate value `v`, count entries `<= v` row by row; the answer is the first `v` with count `>= k`.
</details>

---

[← 23. Sorting Algorithms Compared](23-sorting-compared.md) · [Handbook contents](README.md) · [25. Dynamic Programming →](25-dynamic-programming.md)
