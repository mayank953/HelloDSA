# 9. Recursion on Arrays

**Part 2: Recursion** · Intermediate · about 9 minutes to read

> Shrink the list by one, trust the recursive call, combine. Sum, sorted check, first and last index, and the four ways to return many answers.
**In the video:** [`2:50:40`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10240s) Recursion with arrays · [`3:00:55`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10855s) Sum of an array · [`3:30:15`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=12615s) Is it sorted? · [`4:20:06`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=15606s) All indices · [`5:04:55`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=18295s) Returning a new list  
**In this repo:** [Recursion and arrays: code, notes, notebooks](../recursion/02-recursion-and-arrays/)  
**Run the code from this chapter:** [`code/09-recursion-on-arrays.py`](code/09-recursion-on-arrays.py)  

---

## Recursion meets lists

Until now the input was a *number*, and "smaller" meant `n − 1` or `n // 10`. Now the input is a **list** (Python calls it a list; other languages call it an array; the idea is the same). What does "smaller" mean for a list?

> **Smaller list = the same list with one element taken out.**

We take the **first** element as *my own job*, and leave the **rest** as the smaller problem. In pictures:

```text
 [ 4 , 1 , 7 , 3 ]      the problem
   |   \___________/
 my job   the smaller problem: "the rest" -> hand it to recursion
```

The recipe from chapter 6 does not change:

1. **Base case.** An empty list (or a list with one item): answer directly.
2. **Assume.** The recursive call correctly solves the problem for *the rest*.
3. **My part.** Use my first element together with that answer.

Everything in this chapter is just that recipe, with different "my part"s.

### Two ways to shrink a list

```python
def with_slicing(items):
    if len(items) == 0:
        return
    print(items[0])
    with_slicing(items[1:])        # a NEW list, one item shorter (a copy: chapter 4)

def with_index(items, i=0):
    if i == len(items):            # "empty" now means: the index ran off the end
        return
    print(items[i])
    with_index(items, i + 1)       # the SAME list, a bigger starting index

with_slicing(["a", "b", "c"])
with_index(["a", "b", "c"])
```

**Output**

```text
a
b
c
a
b
c
```

Both are fine to *think* with. Slicing is shorter to write; the index version avoids copying. We will use slicing to learn the idea, then switch to indexes ("the optimisation") when we care about cost.

---

## Problem 1: the sum of a list

**Question.** `sum_array([4, 1, 7]) → 12`.

**Story: kids and notebooks.** A line of kids, each holding some notebooks. The teacher wants the total number. Instead of walking down the line, the teacher asks the first kid: *"How many do you and everyone behind you have?"* The first kid answers by asking the kid behind *"how many do you and everyone behind you have?"*, adds their own, and replies. The last kid has nobody behind, so replies with their own count.

**Smaller problem.** The rest of the list.

**Assume.** `sum_array(rest)` is correct.

**My part.** Add `items[0]`.

**Base case.** An empty list sums to `0`.

```python
def sum_array(items):
    if len(items) == 0:                 # base case
        return 0
    small_answer = sum_array(items[1:])  # assume: the sum of everything after me
    return items[0] + small_answer       # my part

print(sum_array([4, 1, 7]), sum_array([]))
```

**Output**

```text
12 0
```

Draw the recursion tree. It is a straight chain, because every call makes just one call:

```text
sum_array([4, 1, 7])        = 4 + 8 = 12
   sum_array([1, 7])        = 1 + 7 = 8
      sum_array([7])        = 7 + 0 = 7
         sum_array([])      = 0          <- base case
```

The same function, the **tail style** with an accumulator (chapter 8), and the **index** style that avoids slicing:

```python
def sum_tail(items, accumulator=0):
    if len(items) == 0:
        return accumulator                       # the answer was built on the way down
    return sum_tail(items[1:], accumulator + items[0])

def sum_index(items, i=0):
    if i == len(items):
        return 0
    return items[i] + sum_index(items, i + 1)

data = [4, 1, 7, 3, 9]
print(sum_array(data), sum_tail(data), sum_index(data))
```

**Output**

```text
24 24 24
```


**Cost.** `n + 1` calls, constant work each: **O(n) time**, **O(n) stack**. The slicing versions also copy lists of size `n − 1, n − 2, ...`, so they spend **O(n²) time on copying** and (we saw in chapter 4) hold O(n²) elements at once. The index version spends neither.

---

## Problem 2: is the list sorted?

**Question.** `True` if the list is in non-decreasing order.

**Smaller problem.** The rest of the list.

**Assume.** `is_sorted(rest)` correctly answers whether the rest is sorted.

**My part.** Check that my first element is not larger than the second. The list is sorted exactly when *both* are true: my pair is in order **and** the rest is sorted.

**Base case.** A list of 0 or 1 items is sorted.

```python
def is_sorted(items):
    if len(items) <= 1:
        return True
    rest_is_sorted = is_sorted(items[1:])
    return items[0] <= items[1] and rest_is_sorted

print(is_sorted([1, 2, 2, 5]), is_sorted([1, 3, 2]), is_sorted([]))
```

**Output**

```text
True False True
```

It is correct. But think: if the list is `[9, 1, 2, 3, ..., 99999]`, **do we need to look at the other 99,997 items?** No! The first two already tell us it is not sorted. The code above recurses all the way down *before* it checks anything. We can check **first**, and only call if the pair passes:

```python
calls = 0

def is_sorted_slow(items):
    global calls
    calls += 1
    if len(items) <= 1:
        return True
    rest_is_sorted = is_sorted_slow(items[1:])       # always goes all the way down
    return items[0] <= items[1] and rest_is_sorted

def is_sorted_fast(items):
    global calls
    calls += 1
    if len(items) <= 1:
        return True
    if items[0] > items[1]:                            # check my pair FIRST
        return False                                    # no need to look any further
    return is_sorted_fast(items[1:])

unsorted = [9] + list(range(1, 200))                   # the very first pair is already wrong

calls = 0; is_sorted_slow(unsorted); print("slow version calls:", calls)
calls = 0; is_sorted_fast(unsorted); print("fast version calls:", calls)
```

**Output**

```text
slow version calls: 200
fast version calls: 1
```

Same answer, but one version stops immediately. **Whenever your "my part" can already decide the answer, do it before the recursive call.** This idea (return early) makes many recursive solutions faster, and in interviews it is exactly the kind of thought that impresses.


---

## Problem 3: where is the first (and last) `x`?

**Question.** Return the index of the first occurrence of `x`, or `-1` if it is not there.

Start with the index version, which is the cleanest:

```python
def first_index(items, x, i=0):
    if i == len(items):             # ran off the end: x is not here
        return -1
    if items[i] == x:               # found it: my part answers the question right away
        return i
    return first_index(items, x, i + 1)    # not me: let the rest search

print(first_index([5, 3, 8, 3, 1], 3), first_index([5, 3, 8], 7))
```

**Output**

```text
1 -1
```

### The slicing trap: the answer is *relative*

Now try it with slicing, where the "smaller list" is `items[1:]`. The recursive call returns an index **inside the smaller list**. In the smaller list everything has moved one position to the left, so the answer must be shifted:

```python
def first_index_slicing(items, x):
    if len(items) == 0:
        return -1
    if items[0] == x:
        return 0
    small_answer = first_index_slicing(items[1:], x)
    if small_answer == -1:           # not in the rest: still not found
        return -1
    return small_answer + 1          # the rest started one place later, so add 1

print(first_index_slicing([5, 3, 8, 3, 1], 3))
```

**Output**

```text
1
```

Forgetting that `+ 1` is the **most common** bug here. (And forgetting to treat `-1` specially gives `-1 + 1 = 0`, a false "found at position 0".) The index version never has this problem because it keeps the **original** positions, which is another reason to prefer it.

### The last index

The first match is easy because we stop at once. For the **last** match, a nice trick: ask the *rest* first. If the rest has an `x`, its **last** occurrence is also the overall last. Only if the rest has none should I check myself.

```python
def last_index(items, x, i=0):
    if i == len(items):
        return -1
    in_the_rest = last_index(items, x, i + 1)      # assume: the last index of x at positions after me
    if in_the_rest != -1:
        return in_the_rest
    return i if items[i] == x else -1              # nothing after me, so is it me?

print(last_index([5, 3, 8, 3, 1], 3), last_index([5, 3, 8], 7))
```

**Output**

```text
3 -1
```


---

## Problem 4: *all* the indices of `x`: the teacher's diary

This is the problem that makes recursion on lists click. Now there may be **many** answers. The question is: *how do we hand them back?*

There are exactly four styles. Learn all four, because the same choice appears in every "find all" question (subsets, permutations, paths, ...).

**The story.** A teacher wants to know which kids did not do their homework. The kids stand in a line. There are four ways the teacher can find out:

| # | Style | The story |
|---|---|---|
| 1 | **Print** | Each defaulter stands up and shouts *"I didn't do it!"* The teacher just hears them. Nothing is collected. |
| 2 | **Pass a list down** | The teacher hands a **diary** to the first kid. Each kid writes their name in the diary if needed, then passes the *same diary* to the next kid. |
| 3 | **Global list** | A diary lies on the teacher's **desk**. Every kid walks to the desk and writes into it. |
| 4 | **Return a new list** | The teacher asks the first kid: *"Give me a paper listing every defaulter from you onward."* Each kid asks the one behind them for *their* paper, adds themselves, and returns it. |

We will find all indices of `x = 2` in `[3, 2, 5, 2, 8, 2, 1]` (the answer is `[1, 3, 5]`).

### Style 1: print

```python
def print_indices(items, x, i=0):
    if i == len(items):
        return
    if items[i] == x:
        print(i)                       # the kid stands up and shouts
    print_indices(items, x, i + 1)

print_indices([3, 2, 5, 2, 8, 2, 1], 2)
```

**Output**

```text
1
3
5
```

Simple and fine **if the question says "print"**. But nothing is *kept*: you cannot use the answers afterwards.

### Style 2: pass the diary down

```python
def collect_indices(items, x, i, diary):
    if i == len(items):
        return
    if items[i] == x:
        diary.append(i)                      # write into the diary we were handed
    collect_indices(items, x, i + 1, diary)  # pass the SAME diary onward

diary = []
collect_indices([3, 2, 5, 2, 8, 2, 1], 2, 0, diary)
print(diary)
```

**Output**

```text
[1, 3, 5]
```

This works because (chapter 2) a list passed to a function is a **reference**: every call is writing into the very same list. The function returns nothing; the *caller* owns the diary and reads it afterwards.

### Style 3: the global diary on the desk

```python
desk_diary = []                              # lives outside every function

def global_indices(items, x, i=0):
    if i == len(items):
        return
    if items[i] == x:
        desk_diary.append(i)
    global_indices(items, x, i + 1)

global_indices([3, 2, 5, 2, 8, 2, 1], 2)
print(desk_diary)
```

**Output**

```text
[1, 3, 5]
```

It works, but it is the **dangerous** one. Call it a second time and watch:

```python
global_indices([3, 2, 5, 2, 8, 2, 1], 2)
print(desk_diary)
```

**Output**

```text
[1, 3, 5, 1, 3, 5]
```

The old entries are still sitting on the desk. Every caller shares the same global list, so you must remember to clear it before each use, and it breaks the moment two parts of a program use the function at once. **In real code, avoid it.** (It does appear in older tutorials, which is why you should recognise it.)

### Style 4: return a new list (the clean one)

This is the style to prefer, because it follows the recipe exactly:

- **Smaller problem:** the same question for the rest of the list.
- **Assume:** `return_indices(items, x, i + 1)` returns a list of *all* indices of `x` at positions after me. (The kid behind hands me a paper.)
- **My part:** if I am an `x`, put my index at the front of that paper.
- **Base case:** past the end, nobody is left: an empty list.

```python
def return_indices(items, x, i=0):
    if i == len(items):
        return []                                  # base case: an empty paper
    small_answer = return_indices(items, x, i + 1) # assume: the paper from everyone behind me
    if items[i] == x:
        return [i] + small_answer                  # my part: I add myself to the front
    return small_answer                            # not me: pass the paper up unchanged

print(return_indices([3, 2, 5, 2, 8, 2, 1], 2))
print(return_indices([3, 2, 5, 2, 8, 2, 1], 9))
```

**Output**

```text
[1, 3, 5]
[]
```

No shared state, no cleanup, nothing to forget. Call it a hundred times and every call is independent.


### Choosing a style

| Style | Use it when | Danger |
|---|---|---|
| **Print** | The question says "print all..." | Nothing is stored |
| **Pass a list down** | You want to *fill* a structure and the caller can own it | Easy to forget that all calls share it |
| **Global list** | Quick hack only | Leaks between calls; hard to test |
| **Return a new list** | **Almost always** | Slight extra copying of the answer (fine) |

The **same four styles** will come back for subsequences, permutations and phone-keypad words in chapters 11 and 12. If you remember the diary story, you will not get confused.

---

## Slicing again: the cost, with numbers

Return-style with slicing needs the shift trick too (`small_answer` holds indices *relative to the sliced list*):

```python
def return_indices_slicing(items, x):
    if len(items) == 0:
        return []
    small_answer = return_indices_slicing(items[1:], x)
    shifted = [i + 1 for i in small_answer]       # every index moves one place right
    return ([0] + shifted) if items[0] == x else shifted

print(return_indices_slicing([3, 2, 5, 2, 8, 2, 1], 2))
```

**Output**

```text
[1, 3, 5]
```

Now there are *two* costs per call: copying the slice and rebuilding the shifted answer list. Let us **measure** them on a list of 399 elements (about one in seven is a match):

```python
copied = shifted = 0

def return_indices_slicing_counted(items, x):
    global copied, shifted
    if len(items) == 0:
        return []
    rest = items[1:]
    copied += len(rest)                        # the slice we just built
    small_answer = return_indices_slicing_counted(rest, x)
    shifted += len(small_answer)               # every index in the answer is touched again
    shifted_answer = [i + 1 for i in small_answer]
    return ([0] + shifted_answer) if items[0] == x else shifted_answer

big = [3, 2, 5, 2, 8, 2, 1] * 57
result = return_indices_slicing_counted(big, 2)
print(f"slicing version: {copied:,} items copied and {shifted:,} indices re-shifted for {len(big)} elements")
print(f"matches found: {len(result)}")
print(f"index version  : 0 items copied, 0 indices re-shifted")
```

**Output**

```text
slicing version: 79,401 items copied and 34,029 indices re-shifted for 399 elements
matches found: 171
index version  : 0 items copied, 0 indices re-shifted
```


Moral: **use the index parameter** for lists, and slicing only when clarity matters more than speed.

---

## Splitting in halves (a preview)

Recursion on lists can also cut the list in *two halves* instead of removing one item. We will use this in binary search and merge sort. As a taste, here is the **maximum** of a list found by halves:

```python
def max_by_halves(items, low=0, high=None):
    if high is None:
        high = len(items) - 1
    if low == high:                              # one item: it is the maximum
        return items[low]
    mid = (low + high) // 2
    left_max = max_by_halves(items, low, mid)        # assume: the maximum of the left half
    right_max = max_by_halves(items, mid + 1, high)  # assume: the maximum of the right half
    return left_max if left_max > right_max else right_max   # my part: the bigger of the two

print(max_by_halves([4, 9, 2, 7, 5, 11, 3]))
```

**Output**

```text
11
```


The depth is only `log n` here, although the work is still `n`. This **divide and conquer** shape powers binary search, merge sort and quick sort (chapter 10).

---

## Common mistakes

- **Off by one in the base case.** With an index, the base case is `i == len(items)`, not `len(items) - 1`.
- **Forgetting the `+ 1` shift** with slicing, or forgetting that `-1` ("not found") must not be shifted.
- **Using a global list** and getting leftovers from a previous call.
- **Mutating the input** by accident (`items.pop(0)` inside a recursion) and breaking the caller's list.
- **Not returning the recursive result** (`first_index(...)` without `return` gives `None`).
- **Recursing before checking the easy answer** (the `is_sorted` lesson).

---

## Practice

1. 🟢 `max_of_list(items)` with the first-element-plus-rest recipe.
2. 🟢 `count_occurrences(items, x)`.
3. 🟢 `contains(items, x)` that returns `True`/`False`. Make it stop as soon as it finds `x`.
4. 🟡 `reverse_list(items)` that returns a new reversed list. Then write one that reverses **in place** with two indices.
5. 🟡 `remove_all(items, x)` that returns a new list without any `x`.
6. 🟡 `indices_greater_than(items, k)`: return a new list of positions whose value exceeds `k`.
7. 🔴 `second_largest(items)`, recursively. *(Hint: carry the largest and second-largest found so far.)*
8. 🔴 Write all four styles for "print / fill / global / return the **values** greater than 10" and compare them.

<details>
<summary>Hints</summary>

1. `max(items[0], max_of_list(rest))`, with a base case for one item.
3. `if items[i] == x: return True` before the recursive call, so the search stops early.
4. In place: swap `items[low]` and `items[high]`, then recurse on `(low + 1, high - 1)`; stop when `low >= high`.
7. Use an index helper `go(i, largest, second)` and update both values as you go. The base case returns `second`.
</details>

These are the same ideas the video's checkpoint notebook tests: [Checkpoint 2](../assignments/A2-recursion-and-arrays.ipynb).

---

[← 8. Head vs Tail Recursion and the Order of Work](08-head-vs-tail-recursion.md) · [Handbook contents](README.md) · [10. Searching and Sorting with Recursion →](10-searching-and-sorting-with-recursion.md)
