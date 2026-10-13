# 10. Searching and Sorting with Recursion

**Part 2: Recursion** · Intermediate · about 10 minutes to read

> Linear and binary search, merge sort (divide, conquer, merge) and quick sort (pivot and partition), with the recurrences that give their running time.
**In the video:** [`5:35:08`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=20108s) Linear search · [`5:50:54`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=21054s) Binary search · [`6:12:30`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=22350s) Merge sort · [`7:11:17`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=25877s) Quick sort  
**In this repo:** [Searching and sorting: code and notebooks](../recursion/03-searching-and-sorting/)  
**Run the code from this chapter:** [`code/10-searching-and-sorting-with-recursion.py`](code/10-searching-and-sorting-with-recursion.py)  

---

## Two jobs every program does

Almost every program, sooner or later, has to **find** something in a collection and **put a collection in order**. Searching and sorting are the two oldest problems in computing, and the way we solve them with recursion shows the second great shape of recursion: **divide and conquer**.

> **Divide and conquer.** Split the problem into smaller pieces, solve each piece by recursion (trusting it, as always), and combine the answers.

In this chapter: **linear search**, **binary search**, **merge sort** and **quick sort**, each from the intuition up, with the cost counted exactly.

---

## 1. Linear search with recursion

**Question.** Is `x` somewhere in the list?

This is the "first index" problem from chapter 9, simplified. The recursive idea: *look at the first item; if it is not `x`, ask the rest.*

```python
def linear_search(items, x, i=0):
    if i == len(items):             # base case: ran off the end, x is not here
        return False
    if items[i] == x:               # found it: no need to look any further
        return True
    return linear_search(items, x, i + 1)

print(linear_search([4, 9, 2, 7], 2), linear_search([4, 9, 2, 7], 5))
```

**Output**

```text
True False
```

Worst case it looks at all `n` items: **O(n)**. Linear search has one great advantage: it works on **any** list, sorted or not. When the list *is* sorted we can do dramatically better.

---

## 2. Binary search: the dictionary story

You want the word **"mango"** in a printed dictionary. Do you start at page 1? Of course not. You open the book in the middle, see "kiwi", and think: *m comes after k, so mango is in the second half.* You ignore the first half completely. Open the middle of the second half... and repeat. Within a few flips you are there.

That is **binary search**. Every step looks at the middle and **throws away half**. Its power: a dictionary of a million words needs about **twenty** looks.

**It only works on a sorted list**, because "mango comes after kiwi, so look right" needs the order.

### The recipe

- **Smaller problem.** The left half or the right half of the current range.
- **Assume.** The recursive call correctly searches that half.
- **My part.** Look at the middle element and decide *which* half to hand over (or answer directly if the middle is the target).
- **Base case.** The range is empty (`low > high`): the target is not here.

```python
def binary_search(items, target, low=0, high=None):
    if high is None:
        high = len(items) - 1
    if low > high:                      # base case: an empty range
        return -1
    mid = low + (high - low) // 2       # the middle position
    if items[mid] == target:
        return mid                      # found
    if items[mid] < target:             # target is bigger, so it can only be to the right
        return binary_search(items, target, mid + 1, high)
    return binary_search(items, target, low, mid - 1)   # target is smaller: look left

numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(numbers, 23), binary_search(numbers, 7), binary_search([], 1))
```

**Output**

```text
5 -1 -1
```

### Trace it

Search for `23` in `[2, 5, 8, 12, 16, 23, 38, 56, 72, 91]` (positions 0 to 9):

```text
low=0 high=9  mid=4  items[4]=16  16 < 23  -> go right: low=5
low=5 high=9  mid=7  items[7]=56  56 > 23  -> go left : high=6
low=5 high=6  mid=5  items[5]=23  found!   -> return 5
```

Three looks for a ten-item list. Let the computer count for much bigger lists:

```python
checks = 0

def binary_search_counted(items, target, low, high):
    global checks
    if low > high:
        return -1
    checks += 1
    mid = low + (high - low) // 2
    if items[mid] == target:
        return mid
    if items[mid] < target:
        return binary_search_counted(items, target, mid + 1, high)
    return binary_search_counted(items, target, low, mid - 1)

for n in [1_000, 1_000_000, 10_000_000]:
    data = list(range(n))
    checks = 0
    binary_search_counted(data, -1, 0, n - 1)        # worst case: not present
    print(f"n = {n:>10,}: {checks} looks (a linear scan would need up to {n:,})")
```

**Output**

```text
n =      1,000: 9 looks (a linear scan would need up to 1,000)
n =  1,000,000: 19 looks (a linear scan would need up to 1,000,000)
n = 10,000,000: 23 looks (a linear scan would need up to 10,000,000)
```


**Cost.** `T(n) = T(n/2) + O(1)`: **O(log n)** time. The recursion depth is also `log n`, so the stack is **O(log n)**. (Chapter 3 told you a million items need about twenty halvings. Here it is.)

### The slicing trap, again

What if we write binary search with slicing, `items[:mid]` and `items[mid + 1:]`? It still *works*, but each call copies half the list. The copying alone costs `n/2 + n/4 + n/8 + ... ≈ n`, so we have thrown away the whole point:

```python
copied = 0

def binary_search_slicing(items, target):
    global copied
    if len(items) == 0:
        return False
    mid = len(items) // 2
    if items[mid] == target:
        return True
    half = items[mid + 1:] if items[mid] < target else items[:mid]
    copied += len(half)
    return binary_search_slicing(half, target)

data = list(range(1_000_000))
copied = 0
binary_search_slicing(data, -1)
print(f"slicing binary search copied {copied:,} items to search {len(data):,}")
```

**Output**

```text
slicing binary search copied 999,993 items to search 1,000,000
```

So: **binary search must use indexes**, not slicing. That is why the helper carries `low` and `high`.

### Bugs people actually make

- **`mid = (low + high) / 2`** gives a float. Use `//`. (In languages with fixed-size integers, `low + high` can overflow, so write `low + (high - low) // 2` as a habit.)
- **Off by one**: `mid` has already been checked, so recurse with `mid + 1` or `mid - 1`, never `mid`. Using `mid` can loop forever.
- **Using it on an unsorted list**. It returns wrong answers silently.

---

## 3. Merge sort: the police story

Sorting a list of eight numbers is a lot to handle. Sorting two lists of four is easier. Sorting four lists of two, easier still. A list of **one** is already sorted, because there is nothing to compare. What if we split all the way down, then **combine** the pieces back in order?

**The story.** A crime has eight witnesses. The police separate them into two rooms of four. Each room is told: *"Sort out your statements among yourselves."* Each room splits again. Eventually single witnesses give single statements. Then the police begin merging statements: two statements become one consistent account, two accounts become a bigger account, until there is one account that is in order.

The recursion recipe falls out immediately:

1. **Base case.** A list of 0 or 1 items is already sorted.
2. **Assume.** Both halves, sorted by the recursive call, come back **sorted**.
3. **My part.** **Merge** two sorted halves into one sorted list.

All the cleverness lives in the **merge**.

### The merge step

Two sorted lists, `left = [2, 5, 9]` and `right = [3, 4, 8]`. Put a finger on the first item of each. *Take the smaller of the two fingers' items*, put it in the result, and move that finger. Repeat. When one list runs out, copy the rest of the other.

```text
left  = [2, 5, 9]     right = [3, 4, 8]        result
 ^                      ^
 2 <= 3 -> take 2                              [2]
    ^                   ^
 5 >  3 -> take 3                              [2, 3]
    ^                      ^
 5 >  4 -> take 4                              [2, 3, 4]
    ^                         ^
 5 <= 8 -> take 5                              [2, 3, 4, 5]
       ^                      ^
 9 >  8 -> take 8                              [2, 3, 4, 5, 8]
       ^                      (right is empty) copy the rest: 9
                                               [2, 3, 4, 5, 8, 9]
```

```python
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:            # <= keeps equal items in their original order (stable)
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])                # one of these two is empty; the other has the leftovers
    result.extend(right[j:])
    return result

print(merge([2, 5, 9], [3, 4, 8]))
print(merge([], [1, 2]), merge([1, 1], [1]))
```

**Output**

```text
[2, 3, 4, 5, 8, 9]
[1, 2] [1, 1, 1]
```

Merging two lists of total size `n` takes **O(n)**: each item is taken exactly once.

### The whole algorithm

```python
def merge_sort(items):
    if len(items) <= 1:                          # base case
        return items[:]
    mid = len(items) // 2
    sorted_left = merge_sort(items[:mid])        # assume: the left half, sorted
    sorted_right = merge_sort(items[mid:])       # assume: the right half, sorted
    return merge(sorted_left, sorted_right)      # my part

print(merge_sort([5, 2, 4, 7, 1, 3, 2, 6]))
```

**Output**

```text
[1, 2, 2, 3, 4, 5, 6, 7]
```


### Watch it divide and merge

```python
def merge_sort_verbose(items, depth=0):
    pad = "    " * depth
    print(f"{pad}split  {items}")
    if len(items) <= 1:
        return items[:]
    mid = len(items) // 2
    left = merge_sort_verbose(items[:mid], depth + 1)
    right = merge_sort_verbose(items[mid:], depth + 1)
    merged = merge(left, right)
    print(f"{pad}merge  {left} + {right} -> {merged}")
    return merged

merge_sort_verbose([5, 2, 4, 7, 1, 3, 2, 6])
```

**Output**

```text
split  [5, 2, 4, 7, 1, 3, 2, 6]
    split  [5, 2, 4, 7]
        split  [5, 2]
            split  [5]
            split  [2]
        merge  [5] + [2] -> [2, 5]
        split  [4, 7]
            split  [4]
            split  [7]
        merge  [4] + [7] -> [4, 7]
    merge  [2, 5] + [4, 7] -> [2, 4, 5, 7]
    split  [1, 3, 2, 6]
        split  [1, 3]
            split  [1]
            split  [3]
        merge  [1] + [3] -> [1, 3]
        split  [2, 6]
            split  [2]
            split  [6]
        merge  [2] + [6] -> [2, 6]
    merge  [1, 3] + [2, 6] -> [1, 2, 3, 6]
merge  [2, 4, 5, 7] + [1, 2, 3, 6] -> [1, 2, 2, 3, 4, 5, 6, 7]
```

Read it like the police story: split down to single statements, then merge up. The recursion tree has **`log n` levels** (we halve until size 1). On *every* level, all the merges together touch each of the `n` items exactly once: `n` work per level.

> **Total = n work per level × log n levels = O(n log n).** The depth is `log n`; the merging needs a helper list, so extra space is **O(n)**.

Let us count real comparisons against the worst a quadratic sort would need:

```python
def merge_sort_counting(items):
    """Returns (sorted list, number of comparisons)."""
    if len(items) <= 1:
        return items[:], 0
    mid = len(items) // 2
    left, c1 = merge_sort_counting(items[:mid])
    right, c2 = merge_sort_counting(items[mid:])
    result, i, j, c = [], 0, 0, 0
    while i < len(left) and j < len(right):
        c += 1
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result += left[i:] + right[j:]
    return result, c1 + c2 + c

print(f"{'n':>7} | {'merge sort comparisons':>22} | {'n log2 n':>10} | {'quadratic n(n-1)/2':>19}")
for n in [256, 1024, 4096]:
    data = [(i * 7919) % n for i in range(n)]
    _, comparisons = merge_sort_counting(data)
    print(f"{n:>7} | {comparisons:>22,} | {n * (n.bit_length() - 1):>10,} | {n * (n - 1) // 2:>19,}")
```

**Output**

```text
      n | merge sort comparisons |   n log2 n |  quadratic n(n-1)/2
    256 |                  1,594 |      2,048 |              32,640
   1024 |                  8,929 |     10,240 |             523,776
   4096 |                 41,369 |     49,152 |           8,386,560
```

**Properties to remember:** merge sort is **O(n log n) in every case** (best, average, worst), it is **stable** (equal items keep their order), and it uses **O(n) extra space**. That reliability is why many standard libraries use a merge-based sort.

### The index-based version (as in the video)

Real implementations avoid slicing: they carry `start` and `end` indexes and merge within one list.

```python
def merge_range(items, start, mid, end):
    """Merge the sorted ranges items[start..mid] and items[mid+1..end] in place."""
    left = items[start:mid + 1]
    right = items[mid + 1:end + 1]
    i = j = 0
    k = start
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            items[k] = left[i]; i += 1
        else:
            items[k] = right[j]; j += 1
        k += 1
    while i < len(left):
        items[k] = left[i]; i += 1; k += 1
    while j < len(right):
        items[k] = right[j]; j += 1; k += 1

def merge_sort_inplace(items, start=0, end=None):
    if end is None:
        end = len(items) - 1
    if start >= end:                          # base case: zero or one item
        return
    mid = start + (end - start) // 2
    merge_sort_inplace(items, start, mid)
    merge_sort_inplace(items, mid + 1, end)
    merge_range(items, start, mid, end)

numbers = [12, 5, 6, 9, 10, 1]
merge_sort_inplace(numbers)
print(numbers)
```

**Output**

```text
[1, 5, 6, 9, 10, 12]
```


---

## 4. Quick sort: the pivot story

A teacher has a class standing in a messy line and wants them in height order.

She picks **one student** and calls them the **pivot**. Then she says:

> *"Everyone shorter than the pivot, stand to the pivot's left. Everyone taller, stand to the right."*

After that single step, something wonderful is true: **the pivot is already in its final position.** Nobody to its left will ever need to be to its right. The pivot is done forever.

What remains are two smaller messy groups: the shorter group on the left and the taller group on the right. Each can be sorted *independently*, with exactly the same method. That is a recursion.

1. **Base case.** A group of 0 or 1 is sorted.
2. **My part.** **Partition** around a pivot so the pivot lands in its final place.
3. **Assume.** The recursive calls sort the left group and the right group.

Notice the contrast with merge sort: **merge sort splits easily and works hard when combining; quick sort works hard when splitting and combines for free** (the pieces are already in the right order).

### Partition: the heart of quick sort

We use the last element as the pivot. We keep a boundary `i`: everything to the left of `i` is **at most the pivot**. We scan with `j`; whenever `items[j]` is small enough, we swap it to the boundary and move the boundary forward. At the end, the pivot swaps into the boundary place.

```python
def partition(items, low, high):
    pivot = items[high]            # the last element is the pivot
    boundary = low                 # items[low:boundary] are all <= pivot
    for j in range(low, high):
        if items[j] <= pivot:
            items[boundary], items[j] = items[j], items[boundary]
            boundary += 1
    items[boundary], items[high] = items[high], items[boundary]   # place the pivot
    return boundary                # the pivot's final position

demo = [3, 6, 7, 2, 1, 4, 5]
position = partition(demo, 0, len(demo) - 1)
print("after partition:", demo, " pivot 5 now sits at index", position)
```

**Output**

```text
after partition: [3, 2, 1, 4, 5, 6, 7]  pivot 5 now sits at index 4
```

Everything left of index 4 is `<= 5`, everything right is `> 5`, and `5` is exactly where it will be in the final sorted list.

```text
[3, 6, 7, 2, 1, 4, 5]   pivot = 5
 j=0: 3 <= 5 -> swap with boundary (itself), boundary=1
 j=1: 6 >  5 -> leave
 j=2: 7 >  5 -> leave
 j=3: 2 <= 5 -> swap items[1] and items[3]  [3, 2, 7, 6, 1, 4, 5], boundary=2
 j=4: 1 <= 5 -> swap items[2] and items[4]  [3, 2, 1, 6, 7, 4, 5], boundary=3
 j=5: 4 <= 5 -> swap items[3] and items[5]  [3, 2, 1, 4, 7, 6, 5], boundary=4
 finally swap the pivot into index 4:       [3, 2, 1, 4, 5, 6, 7]
```


### The whole algorithm

```python
def quick_sort(items, low=0, high=None):
    if high is None:
        high = len(items) - 1
    if low >= high:                                 # base case: nothing to sort
        return
    pivot_index = partition(items, low, high)       # my part: the pivot is now in its final place
    quick_sort(items, low, pivot_index - 1)         # assume: the left group gets sorted
    quick_sort(items, pivot_index + 1, high)        # assume: the right group gets sorted

numbers = [3, 6, 7, 2, 1, 4, 5]
quick_sort(numbers)
print(numbers)
```

**Output**

```text
[1, 2, 3, 4, 5, 6, 7]
```


### The catch: the quality of the pivot

If the pivot splits the group nearly in half every time, the recursion tree has `log n` levels with `n` work each: **O(n log n)**. But if the pivot is always the smallest or largest item, one side is empty and the other has `n − 1` items. The tree becomes a straight chain `n` deep, and the work is `n + (n−1) + (n−2) + ...`: **O(n²)**.

When does that happen? With "last element as pivot", on an **already sorted** list, which is a very common input!

```python
comparisons = 0

def partition_counting(items, low, high):
    global comparisons
    pivot = items[high]
    boundary = low
    for j in range(low, high):
        comparisons += 1
        if items[j] <= pivot:
            items[boundary], items[j] = items[j], items[boundary]
            boundary += 1
    items[boundary], items[high] = items[high], items[boundary]
    return boundary

def quick_sort_counting(items, low, high):
    if low >= high:
        return
    p = partition_counting(items, low, high)
    quick_sort_counting(items, low, p - 1)
    quick_sort_counting(items, p + 1, high)

n = 500
sorted_input = list(range(n))
scrambled = [(i * 7919) % n for i in range(n)]

comparisons = 0; quick_sort_counting(sorted_input[:], 0, n - 1); worst = comparisons
comparisons = 0; quick_sort_counting(scrambled[:], 0, n - 1); typical = comparisons

print(f"already sorted : {worst:>7,} comparisons  (n(n-1)/2 = {n * (n - 1) // 2:,})")
print(f"scrambled input: {typical:>7,} comparisons  (n log2 n ~ {int(n * 8.97):,})")
```

**Output**

```text
already sorted : 124,750 comparisons  (n(n-1)/2 = 124,750)
scrambled input:   5,322 comparisons  (n log2 n ~ 4,485)
```


**The standard fixes:** pick a **random** pivot, or the **median of three** (first, middle, last). Then no particular input is consistently bad.

```python
def median_of_three(items, low, high):
    mid = (low + high) // 2
    candidates = sorted([(items[low], low), (items[mid], mid), (items[high], high)])
    return candidates[1][1]                       # the index of the middle value

def quick_sort_median(items, low=0, high=None):
    global comparisons
    if high is None:
        high = len(items) - 1
    if low >= high:
        return
    m = median_of_three(items, low, high)
    items[m], items[high] = items[high], items[m]         # move the chosen pivot to the end
    p = partition_counting(items, low, high)
    quick_sort_median(items, low, p - 1)
    quick_sort_median(items, p + 1, high)

comparisons = 0
quick_sort_median(sorted_input[:])
print(f"already sorted, median-of-three pivot: {comparisons:,} comparisons")
```

**Output**

```text
already sorted, median-of-three pivot: 3,498 comparisons
```


**Properties to remember:** quick sort is **O(n log n) on average**, **O(n²) in the worst case**, sorts **in place** (the stack is **O(log n)** on average), and is **not stable**. In practice it is usually the fastest general sort, which is why it is so popular, but you must know the worst case.

---

## Merge sort versus quick sort

| | Merge sort | Quick sort |
|---|---|---|
| Idea | Split in the middle, **merge** the sorted halves | **Partition** around a pivot, then sort the sides |
| Where the hard work is | In the **merge** (combining) | In the **partition** (splitting) |
| Time, worst case | **O(n log n)** always | **O(n²)** (bad pivots) |
| Time, typical | O(n log n) | **O(n log n)**, small constants |
| Extra space | **O(n)** | **O(log n)** (in place) |
| Stable? | **Yes** | No |
| Great for | Linked lists, huge data on disk, when stability matters | Arrays in memory, general use |

In Python you will normally call `sorted(...)` or `list.sort()`. That uses **Timsort**, a hybrid of merge sort and insertion sort, which is stable and O(n log n) in the worst case. We study the full family of sorts in chapter 23.

---

## Debugging recursive algorithms

The video's habit: **test each building block on its own**.

- Test `merge` alone with tiny sorted lists, including empty ones.
- Test `partition` alone and *check the invariant*: everything left of the returned index is `<=` the pivot, everything right is greater.
- Only then trust the recursion.

```python
def partition_is_correct(items, low, high):
    p = partition(items, low, high)
    pivot = items[p]
    return all(x <= pivot for x in items[low:p]) and all(x > pivot for x in items[p + 1:high + 1])

print(partition_is_correct([7, 1, 8, 3, 3, 9, 4], 0, 6))
```

**Output**

```text
True
```


---

## Common mistakes

- **Binary search on an unsorted list.** Always sort first, or use linear search.
- **Slicing inside binary search**, which costs O(n) and defeats the purpose.
- **Merge sort**: forgetting to copy the leftover items after one side runs out.
- **Quick sort**: recursing on `pivot_index` instead of `pivot_index ± 1` (infinite recursion), and ignoring the worst case.
- **Assuming a sort is stable** when it is not, then being surprised by the order of equal items.
- **Mixing up `low > high` and `low >= high`** in the two base cases. Searching needs `low > high` (empty range); sorting stops at `low >= high` (one item or none).

---

## Practice

1. 🟢 Find the **first** element `>= target` in a sorted list with binary search (the "lower bound").
2. 🟢 Write `is_sorted` and use it to test your merge sort on many random lists.
3. 🟡 Count how many times the middle element is examined for a list of 1,000,000 when searching for the **last** item.
4. 🟡 Merge **three** sorted lists using your `merge` function. What is the cost?
5. 🟡 Sort a list of `(name, age)` pairs by age with a stable merge sort, and show that equal ages keep their original name order.
6. 🔴 **Count inversions** (pairs `i < j` with `items[i] > items[j]`) in `O(n log n)` by changing `merge` to count while it merges.
7. 🔴 **Quickselect:** find the k-th smallest element using `partition`, recursing into only *one* side. What is the average cost?

<details>
<summary>Hints</summary>

1. Same loop as binary search, but when you find a match keep searching to the left.
4. `merge(merge(a, b), c)` costs `O(n)` per merge, with the largest merge touching all items.
6. Every time you take an item from the **right** half before the remaining items of the left half, add `len(left) - i` to the counter.
7. If the pivot lands at index `p`: if `p == k` you are done, if `k < p` recurse left, otherwise right. The average cost is `n + n/2 + n/4 + ... = O(n)`.
</details>

Practice these on your own, then take the auto-checked [Checkpoint 3](../assignments/A3-searching-and-sorting.ipynb).

---

[← 9. Recursion on Arrays](09-recursion-on-arrays.md) · [Handbook contents](README.md) · [11. Recursion on Strings →](11-recursion-on-strings.md)
