# 3. Time Complexity: Counting the Work

**Part 1: Foundations** · Beginner · about 9 minutes to read

> Count steps instead of seconds. Big-O from first principles, loops, nested loops, logarithms, best and worst case, with exact step counts.
**In this repo:** [Time and space complexity notes, notebooks and PDFs](../dsa-topics/time-and-space-complexity/)  
**Run the code from this chapter:** [`code/03-time-complexity.py`](code/03-time-complexity.py)  

---

## The question behind every algorithm

You wrote a solution. It gives the right answer on the sample input. Now someone asks: *"Will it still work when the input is a million times bigger?"*

You cannot answer that by running it once on your laptop. A fast laptop hides a slow algorithm; a slow laptop makes a good one look bad. We need a way to talk about **how the amount of work grows as the input grows**, without caring about the machine.

That is **time complexity**.

> **Idea in one line.** Do not measure seconds. **Count how many basic steps the algorithm takes as a function of the input size `n`.**

---

## Counting steps, the honest way

A *basic step* is one cheap thing: compare two numbers, add two numbers, read one list item. We will not argue about whether one step takes 1 or 3 nanoseconds. We only care how the **number of steps** grows.

Let us give each program a step counter and just watch.

```python
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
```

**Output**

```text
n=10    first_item=1  sum_all=10    count_pairs=100
n=100   first_item=1  sum_all=100   count_pairs=10000
n=1000  first_item=1  sum_all=1000  count_pairs=1000000
```

Look at the three columns as `n` grows ten times, then a hundred times:

- `first_item` does **1 step** no matter what. It is **constant**.
- `sum_all` does **n steps**. Ten times the data, ten times the work. It is **linear**.
- `count_pairs` does **n × n steps**. Ten times the data, a *hundred* times the work. It is **quadratic**.

We write these as **O(1)**, **O(n)** and **O(n²)**. Read "O of n" as "grows like n".


---

## How fast do the common shapes grow?

These are the shapes you will meet again and again. Look at the numbers, not the formulas.

```python
import math

print(f"{'n':>9} | {'log2(n)':>8} | {'n':>9} | {'n*log2(n)':>11} | {'n^2':>15}")
print("-" * 62)
for n in [10, 100, 1_000, 100_000, 1_000_000]:
    print(f"{n:>9} | {math.log2(n):>8.1f} | {n:>9} | {n * math.log2(n):>11.0f} | {n * n:>15}")
```

**Output**

```text
        n |  log2(n) |         n |   n*log2(n) |             n^2
--------------------------------------------------------------
       10 |      3.3 |        10 |          33 |             100
      100 |      6.6 |       100 |         664 |           10000
     1000 |     10.0 |      1000 |        9966 |         1000000
   100000 |     16.6 |    100000 |     1660964 |     10000000000
  1000000 |     19.9 |   1000000 |    19931569 |   1000000000000
```

And the two that are *dangerous*:

```python
print(f"{'n':>4} | {'2^n':>20} | {'n!':>22}")
print("-" * 52)
for n in [5, 10, 20, 25, 30]:
    print(f"{n:>4} | {2 ** n:>20,} | {math.factorial(n):>22,}")
```

**Output**

```text
   n |                  2^n |                     n!
----------------------------------------------------
   5 |                   32 |                    120
  10 |                1,024 |              3,628,800
  20 |            1,048,576 | 2,432,902,008,176,640,000
  25 |           33,554,432 | 15,511,210,043,330,985,984,000,000
  30 |        1,073,741,824 | 265,252,859,812,191,058,636,308,480,000,000
```

Read the table like a story:

- **O(log n)** barely moves: a million items need about twenty steps. This is the shape of *halving*.
- **O(n)** grows in step with the input.
- **O(n log n)** is only a little worse than linear. This is where good sorting lives.
- **O(n²)** explodes: a million items means a *trillion* steps.
- **O(2ⁿ)** and **O(n!)** are only usable for tiny inputs (n around 20 to 25). Those are the shapes of "try every possibility" recursion.

---

## Drop the constants and the small terms

Suppose your program does exactly `3n² + 5n + 2` steps. Is the `5n + 2` important? Look at how much of the total it is as `n` grows:

```python
def steps(n):
    return 3 * n * n + 5 * n + 2

print(f"{'n':>10} | {'3n^2+5n+2':>18} | {'steps / n^2':>12}")
for n in [10, 100, 1_000, 100_000, 1_000_000]:
    print(f"{n:>10} | {steps(n):>18,} | {steps(n) / n ** 2:>12.4f}")
```

**Output**

```text
         n |          3n^2+5n+2 |  steps / n^2
        10 |                352 |       3.5200
       100 |             30,502 |       3.0502
      1000 |          3,005,002 |       3.0050
    100000 |     30,000,500,002 |       3.0001
   1000000 |  3,000,005,000,002 |       3.0000
```

The ratio settles at 3. The `5n + 2` fades into nothing; only the **fastest-growing term** decides the shape. And the constant 3 just says "a few times the same shape". So:

> **Big-O keeps only the dominant term and throws away constants.** `3n² + 5n + 2` is **O(n²)**. `100n` is **O(n)**. `7` is **O(1)**.

Does that mean constants never matter? They matter *between two algorithms of the same shape* (a quick sort is usually faster than a heap sort even though both are O(n log n)). But for the question "what happens when n is huge?", the shape wins every time.


---

## Reading the complexity off the code

### Rule 1: one loop over the input is O(n)

### Rule 2: loops one after the other add up, and we keep the biggest

```python
def two_loops(items):
    steps = 0
    for _ in items:        # n steps
        steps += 1
    for _ in items:        # another n steps
        steps += 1
    return steps           # 2n  ->  O(n)

print(two_loops(list(range(1000))))
```

**Output**

```text
2000
```

### Rule 3: a loop inside a loop multiplies

### Rule 4: a loop whose bound depends on the outer variable

```python
def triangle_pairs(n):
    steps = 0
    for i in range(n):
        for j in range(i + 1, n):     # the inner loop shrinks as i grows
            steps += 1
    return steps

print(triangle_pairs(1000), "vs n*n =", 1000 * 1000)
```

**Output**

```text
499500 vs n*n = 1000000
```

That is `(n−1) + (n−2) + … + 1 = n(n−1)/2`, which is about **half** of n². Half is just a constant, so it is still **O(n²)**. This pattern, "compare every pair", is everywhere.


### Rule 5: halving (or doubling) gives a logarithm

```python
def halving_steps(n):
    steps = 0
    while n > 1:
        n //= 2           # throw away half of what is left
        steps += 1
    return steps

for n in [8, 1024, 1_000_000, 1_000_000_000]:
    print(f"n = {n:>13,}: {halving_steps(n)} halvings")
```

**Output**

```text
n =             8: 3 halvings
n =         1,024: 10 halvings
n =     1,000,000: 19 halvings
n = 1,000,000,000: 29 halvings
```

A billion items, about thirty halvings. That is the superpower of **binary search** and of every algorithm that discards half at each step.

> **Why log base 2 and not another base?** Changing the base only multiplies by a constant, and Big-O ignores constants. So we just write **O(log n)**.


---

## Best case, worst case, average case

The same algorithm can behave very differently on different inputs of the *same size*. Linear search is the cleanest example. We are looking for a target in a list of `n` numbers:

```python
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
```

**Output**

```text
best case  (first item) : 1
worst case (last item)  : 1000
worst case (not present): 1000
average over every position: 500.5
```

- **Best case O(1)**: lucky, it is the very first item.
- **Worst case O(n)**: it is last, or not there at all.
- **Average case O(n)**: about half the list, which is still a multiple of n.

**When someone says "the complexity" with no further detail, they mean the worst case.** It is the promise you can make: "no input will ever be slower than this".


---

## Meet some real algorithms and count their steps

### Bubble sort: always about n²/2 comparisons

```python
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
```

**Output**

```text
n=10    comparisons=      45   n(n-1)/2=45
n=100   comparisons=    4950   n(n-1)/2=4950
n=1000  comparisons=  499500   n(n-1)/2=499500
```

### Merge sort: about n log n comparisons

```python
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
```

**Output**

```text
n=1024   merge sort comparisons=    8929   n*log2(n)=   10240   bubble would need     523776
n=4096   merge sort comparisons=   41369   n*log2(n)=   49152   bubble would need    8386560
n=16384  merge sort comparisons=  206826   n*log2(n)=  229376   bubble would need  134209536
```

Same job, sorting. For 16,384 numbers one needs roughly a quarter of a million comparisons; the other needs over a hundred million. And the gap widens with every doubling of `n`. *That* is why we care.


### Insertion sort: it depends on the input

```python
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
```

**Output**

```text
already sorted : 999
reverse sorted : 499500
```

An already-sorted list costs `n − 1` comparisons (**O(n)**, best case). A reverse-sorted list costs `n(n−1)/2` (**O(n²)**, worst case). Same code, same size, completely different cost: this is why best and worst case are different questions.


---

## Hidden costs inside Python's own operations

A single innocent line can hide a loop. Know these:

| Operation | Cost | Why |
|---|---|---|
| `items[i]` (read or write by index) | **O(1)** | Python jumps straight to the position |
| `items.append(x)` | **O(1)** on average | Usually there is spare room at the end |
| `items.pop()` (from the end) | **O(1)** | Nothing has to move |
| `items.insert(0, x)`, `items.pop(0)` | **O(n)** | Every other item shifts by one |
| `x in items` | **O(n)** | A hidden linear search |
| `items[a:b]` | **O(b − a)** | Builds a copy |
| `x in a_set`, `a_dict[key]` | **O(1)** on average | Hashing (chapter 18) |
| `sorted(items)` | **O(n log n)** | A good sort inside |
| `len(items)` | **O(1)** | The length is stored |
| `"".join(parts)` | **O(total length)** | One pass |

A line like `if x in items:` *inside a loop over items* is a hidden nested loop: **O(n²)**. Turning `items` into a `set` first often cuts it to **O(n)**.

---

## A first look at recursion's time

We will do this properly in the recursion chapters, but here is the preview. For a recursive function, ask two questions:

1. **How many calls are made?**
2. **How much work does each call do besides calling?**

Total time ≈ (number of calls) × (work per call).

```python
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
```

**Output**

```text
calls for n = 50: 50
fib(10) needed     177 calls
fib(15) needed   1,973 calls
fib(20) needed  21,891 calls
fib(25) needed 242,785 calls
```

`factorial` makes one call per level: **O(n)**. `fib` makes *two* calls per level, so the calls roughly multiply: **O(2ⁿ)**. Five more steps of `n` cost about eleven times more calls. We dissect this in chapter 7.

The common recurrences, so you can recognise them later:

| Shape of the recursion | Time |
|---|---|
| `T(n) = T(n−1) + O(1)` (shrink by one, constant work) | **O(n)** |
| `T(n) = T(n−1) + O(n)` (shrink by one, linear work) | **O(n²)** |
| `T(n) = T(n/2) + O(1)` (halve, constant work: binary search) | **O(log n)** |
| `T(n) = 2T(n/2) + O(n)` (halve twice, linear merge: merge sort) | **O(n log n)** |
| `T(n) = 2T(n−1) + O(1)` (two calls, shrink by one: naive Fibonacci, subsets) | **O(2ⁿ)** |


---

## What can a computer do in one second?

A useful rule of thumb, to decide *before* coding whether an idea is fast enough. A modern machine does about **10⁷ to 10⁸ simple steps per second** (Python sits at the lower end of that range, compiled languages at the upper end). So:

| If the input size is up to | An algorithm of this shape is fine |
|---|---|
| about 20 to 25 | O(2ⁿ) |
| about 500 | O(n³) |
| about 5,000 to 10,000 | O(n²) |
| about 1,000,000 | O(n log n) |
| about 10,000,000 or more | O(n) |
| anything | O(log n) or O(1) |

Many interview questions state the limit, such as `n ≤ 10⁵`. Read it as a hint: with `n = 10⁵`, an O(n²) idea needs 10¹⁰ steps and is too slow, so *look for something better*.

---

## Try it: what is the complexity?

Cover the answers and decide. For each, ask: *what is `n`, and how many times does the innermost line run?*

```python
# Q1
for i in range(n):
    print(i)

# Q2
for i in range(n):
    for j in range(n):
        print(i, j)

# Q3
i = 1
while i < n:
    i *= 2

# Q4
for i in range(n):
    for j in range(5):
        print(i, j)

# Q5
for i in range(n):
    for j in range(i):
        print(i, j)

# Q6
def f(n):
    if n == 0:
        return
    f(n - 1)
    f(n - 1)
```

<details>
<summary>Answers</summary>

1. **O(n)**. One loop.
2. **O(n²)**. Nested, both over `n`.
3. **O(log n)**. `i` doubles each time, so it takes about log₂ n steps to pass `n`.
4. **O(n)**. The inner loop always runs exactly 5 times: a constant. 5n is O(n).
5. **O(n²)**. The inner loop runs 0 + 1 + 2 + … + (n−1) = n(n−1)/2 times.
6. **O(2ⁿ)**. Each call makes two calls on `n − 1`: 1 + 2 + 4 + … + 2ⁿ calls.
</details>

---

## Common mistakes

- **Counting lines instead of growth.** Ten lines of O(1) work is still O(1).
- **Forgetting the hidden loops** in `in`, slicing, `insert(0, …)`, `sum(...)` and `sorted(...)`.
- **Mixing up the input size.** If the input is a number `n` and you loop over its digits, the work is about the *number of digits* (log n), not `n`.
- **Saying "O(n) + O(n²) = O(n + n²)"** and stopping. Keep only the dominant term: O(n²).
- **Treating best case as the answer.** Quote the worst case unless asked otherwise.

---

## Practice

1. 🟢 What is the complexity of finding the maximum of an unsorted list? Of a sorted list (largest is last)?
2. 🟢 A function runs a loop of `n` steps and, inside, calls `sum(items)` where `items` has `n` elements. What is the total complexity?
3. 🟡 `for i in range(n): for j in range(i, n): for k in range(j, n): ...` How does the work grow? *(Draw the three loops as a pyramid.)*
4. 🟡 Count, by writing a counter, the number of times the innermost line runs for `i in range(1, n): j = i; while j < n: j *= 2`. Does it match n log n or n?
5. 🔴 Show with a counter that `steps(n) = n + n/2 + n/4 + ... + 1` is **O(n)**, not O(n log n).

<details>
<summary>Hints</summary>

1. Both O(n) if you do not know it is sorted; for a sorted list you can just read the last item: O(1).
2. `sum` is itself a loop of `n`, so it is `n × n`: O(n²).
3. It is O(n³). The exact count is about n³/6, a constant fraction of n³.
4. The inner loop doubles `j`, so it runs about log(n / i) times; adding over every `i` gives O(n) in total. Count it to see.
5. A geometric series: n + n/2 + n/4 + … adds up to less than 2n.
</details>

---

[← 2. Python You Need for DSA](02-python-for-dsa.md) · [Handbook contents](README.md) · [4. Space Complexity: Counting the Memory →](04-space-complexity.md)
