# 23. Sorting Algorithms Compared

**Part 4: Algorithms** · Intermediate · about 8 minutes to read

> Bubble, selection, insertion, merge, quick and counting sort side by side: how they work, what they cost, which are stable.
**In this repo:** [Merge sort and quick sort code](../recursion/03-searching-and-sorting/)  
**Run the code from this chapter:** [`code/23-sorting-compared.py`](code/23-sorting-compared.py)  

---

## Why are there so many sorting algorithms?

You have already met three: bubble sort (chapter 3), merge sort and quick sort (chapter 10), and heap sort (chapter 21). If one of them were simply the best, we would only study that one. Instead, each wins in some situation, because **there is no perfect sorting algorithm, only trade-offs.** This chapter puts them side by side so you can choose, and so you can answer the interview question *"which sort would you use here, and why?"*

Five properties decide:

| Property | Question it answers |
|---|---|
| **Time** (best / average / worst) | How many steps? |
| **Extra space** | Does it need a second array? |
| **Stable?** | Do equal items keep their original order? |
| **In place?** | Can it sort within the same array? |
| **Adaptive?** | Is it faster when the input is already nearly sorted? |

---

## Stability: the property people forget

Imagine a list of students already sorted by **name**. Now you sort it by **class**. Within a class, do the students stay in name order? If yes, the sort is **stable**: *equal items keep their original relative order.* If not, the names within each class may come out scrambled.

Stability matters whenever you sort by one key and then another ("sort by city, then by name within each city"). Let us see a stable sort next to an unstable one:

```python
students = [("Asha", 2), ("Ravi", 2), ("Meera", 1), ("Karan", 2), ("Zoya", 1)]   # (name, class), already by name

def selection_sort_by_class(items):
    items = items[:]
    for i in range(len(items) - 1):
        smallest = min(range(i, len(items)), key=lambda j: items[j][1])    # the first smallest class from i onward
        items[i], items[smallest] = items[smallest], items[i]               # a long-distance swap
    return items

print("stable (Python sorted):", sorted(students, key=lambda s: s[1]))
print("unstable (selection)  :", selection_sort_by_class(students))
```

**Output**

```text
stable (Python sorted): [('Meera', 1), ('Zoya', 1), ('Asha', 2), ('Ravi', 2), ('Karan', 2)]
unstable (selection)  : [('Meera', 1), ('Zoya', 1), ('Asha', 2), ('Karan', 2), ('Ravi', 2)]
```

In the stable result, within class 2 we still have Asha, Ravi, Karan, the original order. In the selection-sort result, a long-distance swap has pushed Asha behind Ravi.


---

## The cast of characters

Each algorithm below returns `(sorted list, comparisons made)` so we can *measure* instead of guess.

### Bubble sort (with an early exit)

Repeatedly sweep the list, swapping neighbours that are out of order; the largest value "bubbles" to the end each sweep. **Optimisation:** if a whole sweep makes no swap, the list is already sorted: stop.

```python
def bubble_sort(items):
    a, comparisons = items[:], 0
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for i in range(end):
            comparisons += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            break
    return a, comparisons
```

### Selection sort

Find the smallest item in the unsorted part and swap it to the front. Always does about `n²/2` comparisons, but **at most `n − 1` swaps**, which matters if swapping is expensive.

```python
def selection_sort(items):
    a, comparisons = items[:], 0
    for i in range(len(a) - 1):
        smallest = i
        for j in range(i + 1, len(a)):
            comparisons += 1
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
    return a, comparisons
```

### Insertion sort

Like sorting playing cards in your hand: take the next card and **slide it left** into its place among the cards already sorted. Wonderful on nearly-sorted data, and the fastest choice for very small lists.

```python
def insertion_sort(items):
    a, comparisons = items[:], 0
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]          # shift larger items one place to the right
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comparisons
```

### Merge sort and quick sort (from chapter 10)

```python
def merge_sort(items):
    if len(items) <= 1:
        return items[:], 0
    mid = len(items) // 2
    left, c1 = merge_sort(items[:mid])
    right, c2 = merge_sort(items[mid:])
    merged, i, j, c = [], 0, 0, 0
    while i < len(left) and j < len(right):
        c += 1
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    return merged + left[i:] + right[j:], c1 + c2 + c

def quick_sort(items):
    a, comparisons = items[:], 0

    def sort(low, high):
        nonlocal comparisons
        if low >= high:
            return
        mid = (low + high) // 2
        a[mid], a[high] = a[high], a[mid]            # a middle pivot dodges the sorted-input worst case
        pivot, boundary = a[high], low
        for j in range(low, high):
            comparisons += 1
            if a[j] <= pivot:
                a[boundary], a[j] = a[j], a[boundary]
                boundary += 1
        a[boundary], a[high] = a[high], a[boundary]
        sort(low, boundary - 1)
        sort(boundary + 1, high)

    sort(0, len(a) - 1)
    return a, comparisons
```

### Heap sort (from chapter 21, in place)

Build a **max-heap** in the array, then repeatedly swap the largest to the end and shrink the heap.

```python
def heap_sort(items):
    a, comparisons = items[:], 0
    n = len(a)

    def sift_down(i, size):
        nonlocal comparisons
        while True:
            left, right, largest = 2 * i + 1, 2 * i + 2, i
            if left < size:
                comparisons += 1
                if a[left] > a[largest]:
                    largest = left
            if right < size:
                comparisons += 1
                if a[right] > a[largest]:
                    largest = right
            if largest == i:
                return
            a[i], a[largest] = a[largest], a[i]
            i = largest

    for i in range(n // 2 - 1, -1, -1):              # build the max-heap in O(n)
        sift_down(i, n)
    for end in range(n - 1, 0, -1):                  # move the biggest to the end, then repair
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)
    return a, comparisons
```


---

## The big measurement

Now run every algorithm on **four kinds of input**, each of 400 items, and count comparisons:

```python
n = 400
inputs = {
    "scrambled": [(i * 7919) % n for i in range(n)],
    "sorted": list(range(n)),
    "reversed": list(range(n, 0, -1)),
    "few distinct": [i % 5 for i in range(n)],
}
names = ["bubble", "selection", "insertion", "merge", "quick", "heap"]
algorithms = [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort]

print(f"{'input':>13} | " + " | ".join(f"{name:>9}" for name in names))
print("-" * 80)
results = {}
for label, data in inputs.items():
    row = []
    for name, algorithm in zip(names, algorithms):
        sorted_data, comparisons = algorithm(data)
        assert sorted_data == sorted(data)
        row.append(comparisons)
        results[(label, name)] = comparisons
    print(f"{label:>13} | " + " | ".join(f"{c:>9,}" for c in row))
```

**Output**

```text
        input |    bubble | selection | insertion |     merge |     quick |      heap
--------------------------------------------------------------------------------
    scrambled |    79,764 |    79,800 |    41,400 |     2,977 |     3,366 |     5,694
       sorted |       399 |    79,800 |       399 |     1,664 |     2,698 |     5,984
     reversed |    79,800 |    79,800 |    79,800 |     1,824 |     2,856 |     5,352
 few distinct |    76,397 |    79,800 |    31,999 |     2,784 |    17,394 |     4,992
```

Read the table by columns and by rows:

- **Selection** never changes: always `n(n−1)/2 = 79,800`. It does not notice that the data is sorted.
- **Bubble (with the early exit)** and **insertion** are tiny on `sorted` (about `n` comparisons): they are **adaptive**.
- On `reversed`, bubble and insertion are at their **worst**: about `n²/2`.
- **Merge** and **heap** are steady and modest on every input: they have **no bad input**.
- **Quick** is in the same league as merge on most inputs (our middle-pivot trick keeps `sorted` and `reversed` cheap; the textbook last-element pivot would cost `n²/2` on `sorted`, as we measured in chapter 10). But look at the last row: on **few distinct values** it needs about five times more comparisons than merge. When many items are *equal* to the pivot, a two-way partition (`<=` versus `>`) sends them all to one side and the split becomes lopsided. Production quick sorts use a **three-way partition** (less / equal / greater) for exactly this reason.
- Comparison counts are not the whole story: quick sort's inner loop is very cache-friendly, which is why it often wins on the clock even when it makes more comparisons.


---

## The scorecard

| Algorithm | Best | Average | Worst | Extra space | Stable | Adaptive | Notes |
|---|---|---|---|---|---|---|---|
| **Bubble** | O(n) with early exit | O(n²) | O(n²) | O(1) | Yes | Yes | Mostly for teaching |
| **Selection** | O(n²) | O(n²) | O(n²) | O(1) | No | No | At most n − 1 swaps |
| **Insertion** | **O(n)** | O(n²) | O(n²) | O(1) | **Yes** | **Yes** | Great for small or nearly sorted input |
| **Merge** | O(n log n) | O(n log n) | **O(n log n)** | O(n) | **Yes** | No | Reliable; ideal for linked lists and external data |
| **Quick** | O(n log n) | **O(n log n)** | O(n²) | O(log n) | No | No | Usually the fastest in practice |
| **Heap** | O(n log n) | O(n log n) | **O(n log n)** | **O(1)** | No | No | Worst-case guarantee with no extra memory |
| **Counting** | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes | No | Only for small integer ranges |

---

## Can we beat n log n?

Every algorithm above sorts by **comparing** items. There is a beautiful argument that *no* comparison-based sort can do better than about `n log n` in the worst case.

Think of the sorter as playing **twenty questions**: each comparison is a yes/no question. A list of `n` items could be in `n!` different orders, and the sorter must work out which one. Each question at best halves the possibilities, so it needs **at least `log₂(n!)` questions**.

```python
import math

print(f"{'n':>6} | {'log2(n!)':>12} | {'n * log2(n)':>12}")
for n in [10, 100, 1000, 10_000]:
    print(f"{n:>6} | {math.log2(math.factorial(n)):>12,.0f} | {n * math.log2(n):>12,.0f}")
```

**Output**

```text
     n |     log2(n!) |  n * log2(n)
    10 |           22 |           33
   100 |          525 |          664
  1000 |        8,529 |        9,966
 10000 |      118,458 |      132,877
```

`log₂(n!)` grows like `n log₂ n`. So **O(n log n) is the best any comparison sort can do**, and merge sort and heap sort achieve it.


### The escape hatch: don't compare

If the keys are **small integers**, we can sort without comparing at all. **Counting sort:** count how many times each value occurs, then write the values out in order. With values in `0..k` it takes **O(n + k)**, faster than n log n when `k` is not huge. The version below is **stable**: it counts how many items are *at most* each value, then places items from the back.

```python
def counting_sort(items, max_value):
    count = [0] * (max_value + 1)
    for x in items:
        count[x] += 1                         # how many of each value
    for v in range(1, max_value + 1):
        count[v] += count[v - 1]              # now count[v] = number of items <= v (the end position + 1)
    output = [None] * len(items)
    for x in reversed(items):                 # going backwards keeps equal items in order (stable)
        count[x] -= 1
        output[count[x]] = x
    return output

exam_scores = [87, 42, 99, 42, 15, 87, 63, 99, 0, 42]
print(counting_sort(exam_scores, 100))
```

**Output**

```text
[0, 15, 42, 42, 42, 63, 87, 87, 99, 99]
```

Use it for ages, exam marks, letters of the alphabet: anywhere the range of values is small compared with the number of items. (A cousin, **radix sort**, sorts large integers digit by digit using counting sort at each step.)


---

## Sorting in Python

In practice you call the built-ins, which use **Timsort**: a hybrid of merge sort and insertion sort that is **stable**, O(n log n) in the worst case, and **O(n)** on already-sorted data. You have three tools:

```python
words = ["pear", "fig", "banana", "kiwi", "apple"]

print(sorted(words))                              # a new sorted list
print(sorted(words, key=len))                     # sort by a key (stable, so ties keep input order)
print(sorted(words, key=len, reverse=True))       # biggest key first
words.sort()                                      # sorts in place, returns None
print(words)
```

**Output**

```text
['apple', 'banana', 'fig', 'kiwi', 'pear']
['fig', 'pear', 'kiwi', 'apple', 'banana']
['banana', 'apple', 'pear', 'kiwi', 'fig']
['apple', 'banana', 'fig', 'kiwi', 'pear']
```

**Sorting by two keys** (ascending class, then descending marks): either use a tuple key (negate the number that must go descending), or exploit stability with **two passes, least important key first**.

```python
rows = [("Asha", 2, 88), ("Ravi", 1, 92), ("Meera", 2, 95), ("Karan", 1, 92), ("Zoya", 2, 88)]

by_tuple = sorted(rows, key=lambda r: (r[1], -r[2]))          # class ascending, marks descending
two_pass = sorted(sorted(rows, key=lambda r: -r[2]), key=lambda r: r[1])   # marks first, then class: stable!
print([r[0] for r in by_tuple])
print([r[0] for r in two_pass])
```

**Output**

```text
['Ravi', 'Karan', 'Meera', 'Asha', 'Zoya']
['Ravi', 'Karan', 'Meera', 'Asha', 'Zoya']
```

**A custom comparison** (rare, but a favourite puzzle): arrange numbers so that joining them gives the **largest possible number**. `[3, 30, 34, 5, 9]` gives `9534330`. The rule: `a` comes before `b` if `a + b > b + a` as strings.

```python
from functools import cmp_to_key

def largest_number(numbers):
    pieces = [str(x) for x in numbers]
    pieces.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)))
    return "".join(pieces).lstrip("0") or "0"

print(largest_number([3, 30, 34, 5, 9]))
```

**Output**

```text
9534330
```


---

## Which sort should I use?

| Situation | Reach for |
|---|---|
| General purpose in Python | **`sorted()` / `.sort()`** (Timsort) |
| Need a guaranteed O(n log n) and stability | **Merge sort** |
| Memory is very tight, worst-case guarantee needed | **Heap sort** |
| Speed on average, in-memory arrays | **Quick sort** |
| Tiny list, or data that is *almost* sorted | **Insertion sort** |
| Integers in a small range | **Counting sort** |
| Data too big for memory | **External merge sort** |
| Only need the smallest *k* items | A **heap** (chapter 21), not a full sort |
| Only need the k-th item | **Quickselect** (average O(n)) |

> **Interview habit.** When asked to sort, first ask: *how big is the input? Are the values bounded? Does stability matter? Is it nearly sorted? How much memory may I use?* Those five questions pick the algorithm.

---

## Common mistakes

- **Writing your own sort when `sorted()` will do.** In real code, use the built-in.
- **Forgetting stability** when sorting by several keys.
- **Assuming quick sort is always O(n log n).** Know the worst case and how to avoid it.
- **Sorting just to find the minimum or the top k.** A heap or a single scan is cheaper.
- **`list.sort()` returns `None`**: `x = items.sort()` is a classic bug.
- **Comparing mixed types** (`int` and `str`) in Python 3: it raises a `TypeError`.

---

## Practice

1. 🟢 Sort the colours `0, 1, 2` in one pass (the Dutch flag) and compare with counting sort.
2. 🟢 Sort the characters of a string by frequency.
3. 🟡 **Merge overlapping intervals**: `[[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]]`.
4. 🟡 Return the `k` **closest points** to the origin.
5. 🟡 Sort an array of 0s, 1s and 2s without using a sort function.
6. 🟡 Implement **bubble sort that stops early** and **count the passes** it needs on nearly-sorted data.
7. 🔴 Implement **radix sort** for non-negative integers using counting sort per digit.
8. 🔴 **Count inversions** in O(n log n) with merge sort (revisited from chapter 10).
9. 🔴 Prove (informally) why the stable counting sort places items from the **back** of the input.

<details>
<summary>Hints</summary>

3. Sort by start. Walk through; if the next interval starts before the current one ends, extend the end; otherwise begin a new interval.
4. Use `heapq.nsmallest(k, points, key=...)` or a max-heap of size k.
7. For each digit position (units, tens, hundreds, ...) run a stable counting sort keyed on that digit.
9. Going backwards, the **last** occurrence of a value gets the **highest** slot among its equals, so earlier occurrences get earlier slots: original order preserved.
</details>

---

[← 22. Graphs](22-graphs.md) · [Handbook contents](README.md) · [24. Binary Search Beyond Sorted Arrays →](24-binary-search-beyond.md)
