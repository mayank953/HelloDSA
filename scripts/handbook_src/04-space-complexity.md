## Time is not the only thing you pay for

An algorithm that is fast but needs 50 GB of memory is useless on a phone. And an algorithm that is lean but takes a week is useless anywhere. Every solution pays in **two currencies**: time and **space** (memory).

**Space complexity** answers: *"How much extra memory does the algorithm need as the input grows?"*

Notice the word **extra**. The input already exists; we usually do not count it. We count what the algorithm **adds**. This extra memory is called **auxiliary space**.

> **Story.** You are marking 500 answer sheets. Marking each sheet and adding the score to one running total needs *one notebook line*, however many sheets there are. Photocopying every sheet before you start needs *500 sheets of paper*. Same job, very different space.

---

## The basics: O(1) space versus O(n) space

```python
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
```

Two more shapes you will meet: a **2D grid** of size `n × n` costs **O(n²)** space, and a **set of every value you have seen** costs **O(n)**.

**In-place** algorithms change the input directly and need only O(1) extra space. Compare:

```python
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
```

The price of in-place is that you destroy the original. If the caller still needs it, you must copy first, and now you are back to O(n). There is always a trade-off.

```python hide
a = [1, 2, 3, 4, 5]; reverse_in_place(a); assert a == [5, 4, 3, 2, 1]
assert reversed_copy([1, 2, 3]) == [3, 2, 1]
```

---

## The memory you cannot see: the call stack

Here is the part that surprises people. **A recursive call is not free memory-wise.** Every call that is still waiting for an answer keeps its **frame** alive (chapter 2): its parameters, its local variables, its return address.

So the space a recursion uses is, at least:

> **(deepest chain of calls waiting at the same time) × (memory per frame)**

Let us measure the depth instead of guessing:

```python
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
```

`factorial(n)` keeps `n` frames alive at the deepest point. So it uses **O(n) space**, even though it never creates a list. A loop computing the same factorial would use **O(1)**.

```python hide
current_depth = deepest = 0
factorial(30)
assert deepest == 30
```

### Depth for the usual suspects

| Recursion | Deepest chain | Stack space |
|---|---|---|
| `factorial(n)`, `sum(n)`, linear search on a list | n | **O(n)** |
| Binary search (halve each time) | log₂ n | **O(log n)** |
| Merge sort | log₂ n levels | **O(log n)** stack, but the merging needs **O(n)** extra array |
| Quick sort, *good* pivots | log₂ n | **O(log n)** |
| Quick sort, *worst* pivots (already sorted, last element as pivot) | n | **O(n)** |
| Naive Fibonacci | n | **O(n)** stack, even though the *time* is exponential |
| Subsets, permutations (depth = input length) | n | **O(n)** stack, plus the answer list itself |

The last two rows teach something important: **time and space are independent.** Naive Fibonacci takes exponential *time* but only linear *space*, because only one chain of calls is alive at a time: when one branch of the tree finishes, its frames are gone before the next branch starts.

```python
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
```

A million items and a stack of only about twenty frames. That is why recursive binary search is perfectly safe.

```python hide
assert binary_search_depth(list(range(1_000_000)), -1, 0, 999_999) <= 21
```

---

## The hidden cost of slicing in recursion

Remember from chapter 2 that `l[1:]` builds a new list. In a *recursive* function that is far worse than it looks, because **every waiting frame holds on to its own slice**.

Look at the usual way to sum a list recursively:

```python
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
```

Every frame at depth `k` holds a list of length `n − k`. All of them are alive at once at the bottom of the recursion, so the memory is `n + (n−1) + … + 1`, which is **O(n²)**. (The first list is the caller's own list, which is why we are slightly generous in counting it.)

Now the same function with an **index** instead of slicing:

```python
def sum_with_index(items, i=0):
    if i == len(items):
        return 0
    return items[i] + sum_with_index(items, i + 1)    # nothing copied: same list, new index
```

Each frame holds one integer `i`, so the total is `n` small frames: **O(n)** space. The list is never copied.

This is exactly the "optimisation" moment from the video: *pass an index instead of slicing*. Same recursion idea, one factor of `n` less memory (and less copying time too).

```python hide
t = {"alive": 0, "peak": 0}
assert sum_with_slicing(list(range(50)), t) == sum(range(50)) and t["peak"] == 50 * 51 // 2
assert sum_with_index(list(range(50))) == sum(range(50))
```

---

## Trading space for time (and the other way round)

Sometimes spending memory **buys** speed. Naive Fibonacci recomputes the same values over and over. If we **remember** each answer (memoization), we spend O(n) space on a table, and the time drops from exponential to linear.

```python
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
```

```python hide
c1, c2 = [0], [0]
assert fib_plain(20, c1) == fib_memo(20, c2) == 6765 and c2[0] < 60 < c1[0]
```

This is the doorway to **dynamic programming**, a whole chapter later. The rule of thumb is worth remembering:

> **If you are doing the same work again and again, remember the answer. It costs memory but saves time.**

The reverse trade also exists. A tiny-memory approach may recompute things or scan the data more than once. Competitions and interviews often ask for "O(1) extra space": the problem is telling you to find the in-place trick.

---

## Where sorting algorithms sit

| Algorithm | Time (worst) | Extra space | Note |
|---|---|---|---|
| Bubble, selection, insertion | O(n²) | **O(1)** | In place |
| Merge sort | O(n log n) | **O(n)** | Needs a helper array to merge |
| Quick sort | O(n²) worst, O(n log n) typical | **O(log n)** typical stack, O(n) worst | In place; depth depends on the pivots |
| Heap sort | O(n log n) | **O(1)** | In place |
| Counting sort | O(n + k) | **O(k)** | For small ranges of integers |

There is no free lunch. Merge sort's guarantee of O(n log n) time costs O(n) memory. Quick sort saves memory but gambles on its pivots.

---

## What "O(1) space" really means

It means the extra memory does **not grow with the input**. A few variables, a pointer or two, a fixed-size table. Be careful with these false friends:

- Returning a **new list** of size n is **O(n)** auxiliary space, even if you only "loop once".
- `sorted(items)` makes a copy: **O(n)**. `items.sort()` sorts in place (Python's sort still uses some temporary space internally, so we simply say it is "in place from your point of view").
- A **recursion with depth n** is **O(n)** space even if it creates no data structure.
- Building a **string by repeated concatenation** creates many intermediate strings. Use `"".join(parts)`.

---

## Common mistakes

- **Forgetting the stack.** "No extra list, so O(1)" is wrong for a recursion of depth n.
- **Counting the input** as extra space, or the output (conventions vary; in interviews, state which you mean).
- **Slicing inside recursion** and silently paying O(n²) memory.
- **Raising the recursion limit** to "fix" a stack that is too deep, instead of switching to a loop or a better algorithm.
- **Believing time and space always move together.** They do not: naive Fibonacci is slow and lean; memoized Fibonacci is fast and heavier.

---

## Practice

1. 🟢 What is the auxiliary space of: (a) summing a list with a loop, (b) building a list of squares, (c) recursive `factorial(n)`?
2. 🟢 A function checks whether a string is a palindrome with `s == s[::-1]`. What is its time and space? Rewrite it with two indices to make the space O(1).
3. 🟡 A recursive function has depth `n` but also creates a new list of size `n` at each level. What is the peak space?
4. 🟡 Why does naive recursive Fibonacci use only O(n) space even though it makes about 2ⁿ calls?
5. 🔴 Quick sort on an *already sorted* list with "last element as pivot" has recursion depth `n`. Run it with a counter to see, then explain why picking a random pivot fixes it on average.

<details>
<summary>Hints</summary>

1. (a) O(1). (b) O(n). (c) O(n), because of the stack.
2. Time O(n) and space O(n), because the reversed string is a copy. Compare `s[i]` with `s[n - 1 - i]` for `i` up to the middle instead.
3. O(n²). Each of the n live frames holds a list of size about n.
4. Only one chain of calls is alive at a time. When a branch returns, its frames are freed before the next branch starts.
5. With a sorted list the pivot is always the largest item, so one side is empty and the other holds n − 1 items: depth n. A random pivot splits the list into reasonable parts most of the time.
</details>
