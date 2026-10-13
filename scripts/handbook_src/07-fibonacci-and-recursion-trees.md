## Why Fibonacci keeps showing up

You have seen the sequence: `0, 1, 1, 2, 3, 5, 8, 13, 21, ...`. Each number is the sum of the two before it. It appears in nature, in art, in interviews, and, most usefully for us, **it is the simplest example of a recursion that calls itself twice**.

That "twice" changes everything. Until now, each call made *one* smaller call, so the calls formed a straight line. With two calls, they form a **tree**. Learning to **draw and read a recursion tree** is one of the most valuable skills in this handbook. The video says it plainly: *"every recursive function: write the recurrence, then draw the recursion tree."*

---

## The recipe, with two assumptions

`F(n) = F(n − 1) + F(n − 2)`. Run the recipe from chapter 6:

1. **Base case.** `F(0) = 0` and `F(1) = 1`. **Two** base cases, because the rule needs two previous values and there is nothing before `F(0)` and `F(1)`.
2. **Assume.** Both `F(n − 1)` and `F(n − 2)` are correct.
3. **My part.** Add them.

In PMI language we **assume the statement for *two* earlier values** (`k` and `k − 1`) to prove it for `k + 1`. (This version is called *strong induction*, and it is why you need two base cases: the first step needs two dominoes already standing.)

```python
def fib(n):
    if n <= 1:                 # base cases: F(0) = 0, F(1) = 1
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(n) for n in range(12)])
```

```python hide
assert [fib(n) for n in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

Correct. Beautiful. And, as we are about to see, *terrible*.

---

## Draw the recursion tree

How does `fib(5)` actually run? Each call spawns two child calls, until the base cases. Let the computer draw the tree for us, indenting by depth:

```python
def print_tree(n, depth=0):
    print("    " * depth + f"fib({n})")
    if n <= 1:
        return n
    left = print_tree(n - 1, depth + 1)       # first child
    right = print_tree(n - 2, depth + 1)      # second child
    return left + right

print_tree(5)
```

Read it as a family tree, top to bottom: `fib(5)` has two children `fib(4)` and `fib(3)`. `fib(4)` has `fib(3)` and `fib(2)`, and so on. The leaves are the base cases `fib(1)` and `fib(0)`.

Notice something immediately: **`fib(3)` appears twice, `fib(2)` three times.** The same question is being answered again and again. That is wasted work, and it gets dramatically worse as `n` grows.

### How the tree is drawn on paper

For small cases, draw it as boxes and arrows:

```text
                    fib(5)
                  /        \
             fib(4)          fib(3)
            /      \         /     \
        fib(3)    fib(2)   fib(2)  fib(1)
        /   \      /  \     /  \
    fib(2) fib(1) f(1) f(0) f(1) f(0)
    /   \
 f(1)  f(0)
```

Tip from the video: when you draw a recursion tree for an exam or interview, **write the argument in each box, and write the return value beside it.** You will find the bug before the interviewer does.

---

## Count the calls

How many calls does `fib(n)` make in total? Let us stop guessing and count:

```python
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
```

Look at the last column. From `n = 20` to `n = 25`, the number of calls is about **11 times larger**. The cost does not grow by an amount; it grows by a **multiplier**. That is the signature of an **exponential** algorithm.

There is even an exact rule, which we can verify:

```python
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
```

```python hide
for n in range(0, 18):
    calls = 0
    fib_counted(n)
    assert calls == 2 * fib_value(n + 1) - 1
```

Because Fibonacci numbers grow by a factor of about **1.618** each step (the golden ratio), the number of calls does too. So the time is roughly **O(1.618ⁿ)**, usually just written **O(2ⁿ)**. At `n = 50` that is about **forty billion** calls. Your laptop would be busy for hours computing a number a pocket calculator finds instantly.

---

## Where is the waste?

How many times does each value of `n` get computed during `fib(10)`?

```python
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
```

`fib(2)` computed 34 times to answer *one* question, `fib(10)`. Each is the same question with the same answer. This is called **overlapping subproblems**, and it is the key to the next idea.

---

## The fix: remember what you have already answered

If the same question keeps coming back, **write the answer down the first time**. A dictionary (a notebook of answers) is enough. This is **memoization**.

```python
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
```

Count the calls to see the difference:

```python
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
```

For `n = 25` the plain version needed about 243,000 calls; the memoized one needs 49. The tree has been **pruned**: a branch that repeats an already-answered question stops immediately. The cost becomes **O(n) time** (each value of `n` is computed once) and **O(n) space** (the notebook, plus the stack).

Python even ships the notebook for free:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n):
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

print(fib_cached(100))
```

```python hide
assert fib_memo(50) == fib_value(50) == fib_cached(50) == 12586269025
assert fib_cached(100) == fib_value(100)
```

> **This is the seed of dynamic programming.** Recursion plus a notebook of answers = memoization. Chapter 25 builds on it fully. Right now, just notice the two-step thought: *"are there overlapping subproblems? then remember."*

### Or build it bottom-up with a loop

We do not even need recursion. `F(n)` depends only on the last two values. Start from the bottom and walk up:

```python
def fib_loop(n):
    a, b = 0, 1                  # F(0), F(1)
    for _ in range(n):
        a, b = b, a + b          # slide the window forward by one
    return a

print(fib_loop(10), fib_loop(200))
```

**O(n) time, O(1) space.** Same answers, no stack at all. In DP language, this is the *tabulation* approach with only the part of the table we need.

```python hide
assert fib_loop(10) == 55 and fib_loop(200) == fib_cached(200)
```

---

## Reading time and space off a recursion tree

This is the general method, and worth memorising. For **any** recursive function, draw the tree and answer:

| Question | For naive Fibonacci |
|---|---|
| **How many nodes (calls) are in the tree?** | About 1.6ⁿ. This is the **time**. |
| **How much work does each node do** besides calling? | A single addition: constant. |
| **How deep does the tree go?** | `n` levels (always following `n − 1`). This is the **stack space**: O(n). |

Time is the number of nodes times the work per node. Space is the **depth**, because only one root-to-leaf path is alive at any moment: when a branch finishes, its frames are gone.

The same method on two other shapes:

- **Linear chain** (`sum_to`): `n` nodes, constant work each, depth `n`. **O(n)** time, **O(n)** space.
- **Halving** (`fast_power`, binary search): `log n` nodes in one path. **O(log n)** time and space.
- **Merge sort** (`2T(n/2) + n`): the tree has `log n` levels, and the *total* work on each level is `n` (the pieces together always add up to `n`). So **n × log n**. (Chapter 10.)

---

## A second example: counting paths up a staircase

**Question.** You climb a staircase of `n` steps, taking 1 or 2 steps at a time. In how many ways can you reach the top?

**Smaller problem.** Your *last* move was a 1-step (you came from step `n − 1`) or a 2-step (you came from step `n − 2`).

**Assume.** `ways(n − 1)` and `ways(n − 2)` are correct.

**My part.** Add them (the two cases do not overlap).

**Base cases.** `ways(1) = 1`, `ways(2) = 2`.

```python
def ways(n):
    if n <= 2:
        return n                      # 1 step: 1 way; 2 steps: 2 ways (1+1 or 2)
    return ways(n - 1) + ways(n - 2)

print([ways(n) for n in range(1, 11)])
```

Look at that list: it is `1, 2, 3, 5, 8, 13...`, Fibonacci again, shifted. Different story, same shape. **Recognising that two problems have the same recurrence is the whole game in DP.**

```python hide
assert [ways(n) for n in range(1, 8)] == [1, 2, 3, 5, 8, 13, 21]
```

---

## Common mistakes

- **Only one base case** (`if n == 0`). `fib(1)` would call `fib(0)` and `fib(-1)`, and never stop. You need both `0` and `1`.
- **Using the naive version in real code** (or in an interview) without mentioning the exponential cost.
- **Forgetting that the memo dictionary must be shared.** Creating a fresh `{}` on every call defeats the purpose. Pass it down, or use `lru_cache`.
- **Mutable default** (`def fib(n, memo={})`): it works by accident but carries state between unrelated calls. Use `None`.
- **Confusing the number of calls with the depth.** Time = nodes. Space = depth.

---

## Practice

1. 🟢 Draw the recursion tree of `fib(4)` on paper and count the leaves.
2. 🟢 Predict, then verify with a counter, how many times `fib(1)` is called while computing `fib(8)`.
3. 🟡 Write `tribonacci(n)`, where each term is the sum of the previous **three**. How many base cases do you need?
4. 🟡 Count the ways to climb `n` stairs taking 1, 2 or 3 steps at a time.
5. 🟡 Write the memoized version of the stairs function and compare the number of calls for `n = 30`.
6. 🔴 Write `fib_pair(n)` that returns the pair `(F(n), F(n+1))` using **one** recursive call. This makes a plain recursion O(n) without any memo.

<details>
<summary>Hints</summary>

1. `fib(4)` has `fib(3)` and `fib(2)` below it. The leaves are the base cases: count the `fib(1)` and `fib(0)` boxes.
3. Three base cases: `T(0)`, `T(1)`, `T(2)`.
4. `ways(n) = ways(n−1) + ways(n−2) + ways(n−3)`.
6. `fib_pair(0) = (0, 1)`. For `n > 0`: take `(a, b) = fib_pair(n − 1)` and return `(b, a + b)`.
</details>

Next, [chapter 8](08-head-vs-tail-recursion.md) asks a subtle question: *does it matter whether the recursive call comes before or after your own work?*
