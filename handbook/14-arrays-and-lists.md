# 14. Arrays and Lists

**Part 3: Data Structures** · Beginner · about 8 minutes to read

> How a dynamic array works, why append is cheap on average, and the patterns every array question uses: prefix sums, two pointers, sliding window, Kadane.
**In this repo:** [Arrays notes and notebook](../dsa-topics/arrays/)  
**Run the code from this chapter:** [`code/14-arrays-and-lists.py`](code/14-arrays-and-lists.py)  

---

## The structure you already use every day

A list (or *array*) is the first data structure everyone meets, and the foundation of nearly every other one. Linked lists, stacks, queues, heaps and hash tables are often built *on top of* arrays. So it pays to know exactly how they behave.

In this chapter: how an array lives in memory, why some operations are instant and others slow, how a growing list manages its space, and then the **five patterns** that solve most array questions.

---

## How an array lives in memory

An array is a **row of equal-sized slots, side by side** in memory, like seats in one row of a cinema.

```text
 address:   1000   1008   1016   1024   1032
          +------+------+------+------+------+
          |  7   |  2   |  9   |  4   |  1   |
          +------+------+------+------+------+
 index:      0      1      2      3      4
```

Because the slots are the same size and sit next to each other, the computer finds item `i` with one calculation, no searching:

> **address of item i = start address + i × slot size**

That is why **reading or writing `items[i]` takes O(1)** time, whether the list has ten items or ten million. It is a jump straight to the seat.

(Python's `list` stores *references* to objects in those slots, so it can hold mixed types. The idea is the same.)

### What is slow? Moving things.

Seats are contiguous, so making room costs. Insert a new item at the **front** and *everyone* must shift one seat to the right. Delete from the front and everyone shifts left.

```python
def insert_with_shifts(items, position, value):
    """Insert like an array would, and count how many items had to move."""
    items.append(None)                          # make room at the end
    shifts = 0
    for i in range(len(items) - 1, position, -1):
        items[i] = items[i - 1]                 # slide one item to the right
        shifts += 1
    items[position] = value
    return shifts

data = list(range(1000))
print("insert at the END   :", insert_with_shifts(data[:], len(data), -1), "shifts")
print("insert in the MIDDLE:", insert_with_shifts(data[:], 500, -1), "shifts")
print("insert at the FRONT :", insert_with_shifts(data[:], 0, -1), "shifts")
```

**Output**

```text
insert at the END   : 0 shifts
insert in the MIDDLE: 500 shifts
insert at the FRONT : 1000 shifts
```


| Operation on a list of `n` items | Cost | Why |
|---|---|---|
| Read / write `items[i]` | **O(1)** | Address arithmetic |
| `append(x)` at the end | **O(1)** on average | See below |
| `pop()` from the end | **O(1)** | Nothing moves |
| `insert(i, x)`, `pop(i)` in the middle | **O(n)** | Items shift |
| `insert(0, x)`, `pop(0)` at the front | **O(n)** | Everything shifts |
| Search for a value (`x in items`) | **O(n)** | Must look at each |
| Search in a **sorted** list (binary search) | **O(log n)** | Halve each time |

If you need to add and remove at the *front* often, an array is the wrong structure. Use a **deque** (chapter 17) or a **linked list** (chapter 15).

---

## What happens when the list is full?

Arrays have a fixed size when created. But Python lists grow when you `append`. How?

The list keeps **spare capacity**. When it fills up, it allocates a **bigger block** (about double), **copies** everything across, and carries on. Copying costs `O(n)`, but it happens rarely. Let us simulate it and count the copies:

```python
class DynamicArray:
    def __init__(self):
        self.capacity = 1
        self.size = 0
        self.slots = [None] * self.capacity
        self.copies = 0                               # how many items we copied while growing

    def append(self, value):
        if self.size == self.capacity:                # full: grow
            self.capacity *= 2                        # double the room
            bigger = [None] * self.capacity
            for i in range(self.size):                # copy everything across
                bigger[i] = self.slots[i]
                self.copies += 1
            self.slots = bigger
        self.slots[self.size] = value
        self.size += 1

arr = DynamicArray()
for value in range(1_000_000):
    arr.append(value)

print(f"appended {arr.size:,} items, final capacity {arr.capacity:,}")
print(f"items copied while growing: {arr.copies:,}  (about one copy per append, never more than two)")
```

**Output**

```text
appended 1,000,000 items, final capacity 1,048,576
items copied while growing: 1,048,575  (about one copy per append, never more than two)
```

For a million appends we copied about a million items in total: roughly **one extra copy per append**, and always less than two. Each individual growth step is expensive, but the **average cost per append stays a small constant**. We call this **amortised O(1)**: expensive moments are rare enough that, spread over all the appends, each one costs a constant amount.

**Why doubling and not "add 10 more"?** Growing by a fixed amount means a copy every 10 appends: total copying becomes quadratic. Growing by a **multiplier** makes the copies add up like `1 + 2 + 4 + ... + n/2 + n`, which is less than `2n`. That is a geometric series (we met one in chapter 3).


---

## A trap with 2D lists

A grid in Python is a list of lists. Here is the classic bug:

```python
grid = [[0] * 3] * 3          # looks like 3 rows of 3 zeros...
grid[0][0] = 7
print(grid)                    # ...but we changed every row!
```

**Output**

```text
[[7, 0, 0], [7, 0, 0], [7, 0, 0]]
```

`[[0] * 3] * 3` does not create three rows. It creates **one** row and puts the *same label* in three places (chapter 2: labels, not boxes). The correct way creates a **new** list for each row:

```python
grid = [[0] * 3 for _ in range(3)]    # a fresh row each time
grid[0][0] = 7
print(grid)
```

**Output**

```text
[[7, 0, 0], [0, 0, 0], [0, 0, 0]]
```


---

## Five patterns that solve most array questions

You do not need to memorise hundreds of solutions. A handful of **patterns** appear again and again. For each one we show the slow way, then the pattern, and **count** the difference.

### Pattern 1: prefix sums (answer many range questions fast)

**Question.** Many times you are asked: *"what is the sum of items from `i` to `j`?"* The slow way adds them up every time: O(n) per question.

**Idea.** Build **once** a table where `prefix[k]` is the sum of the first `k` items. Then any range sum is **one subtraction**:

> sum of items `i` to `j` = `prefix[j + 1] − prefix[i]`

```python
def build_prefix(items):
    prefix = [0]
    for value in items:
        prefix.append(prefix[-1] + value)       # each entry = the previous entry + one more item
    return prefix

data = [3, 1, 4, 1, 5, 9, 2, 6]
prefix = build_prefix(data)
print(prefix)
print("sum of data[2..5] =", prefix[6] - prefix[2], "  (check:", sum(data[2:6]), ")")
```

**Output**

```text
[0, 3, 4, 8, 9, 14, 23, 25, 31]
sum of data[2..5] = 19   (check: 19 )
```

**Cost.** O(n) to build once, then **O(1)** per question. For 100,000 questions on 100,000 numbers: about 10¹⁰ steps the slow way, versus about 2 × 10⁵ with a prefix table.


### Pattern 2: two pointers

Use **two indexes** that move through the list, usually from the two ends or at different speeds, instead of a nested loop.

**Question.** In a **sorted** list, find two numbers that add to a target.

*Slow way:* check every pair: O(n²).

*Pattern:* put a pointer at each end. If the sum is too small, move the left pointer right (to get a bigger number). If too big, move the right pointer left. Every step discards one candidate.

```python
def pair_with_sum(sorted_items, target):
    left, right, steps = 0, len(sorted_items) - 1, 0
    while left < right:
        steps += 1
        total = sorted_items[left] + sorted_items[right]
        if total == target:
            return (sorted_items[left], sorted_items[right]), steps
        if total < target:
            left += 1                 # need something bigger
        else:
            right -= 1                # need something smaller
    return None, steps

numbers = list(range(1, 100_001))
print(pair_with_sum(numbers, 100_001 + 50_000))
print("a nested loop would need up to", len(numbers) * (len(numbers) - 1) // 2, "pair checks")
```

**Output**

```text
((50001, 100000), 50001)
a nested loop would need up to 4999950000 pair checks
```

**Cost.** **O(n)**: each pointer only moves one way, so at most `n` steps in total.

Two pointers also removes duplicates **in place** from a sorted list (a "slow" pointer writes, a "fast" pointer reads):

```python
def remove_duplicates_in_place(sorted_items):
    if not sorted_items:
        return 0
    write = 1                                          # next slot to write a new unique value
    for read in range(1, len(sorted_items)):           # scan with the fast pointer
        if sorted_items[read] != sorted_items[read - 1]:
            sorted_items[write] = sorted_items[read]
            write += 1
    return write                                       # the first `write` items are the unique ones

values = [1, 1, 2, 2, 2, 3, 5, 5]
count = remove_duplicates_in_place(values)
print(values[:count])
```

**Output**

```text
[1, 2, 3, 5]
```


### Pattern 3: the sliding window

**Question.** What is the largest sum of **`k` consecutive** items?

*Slow way:* for every starting position, add up `k` items: O(n·k).

*Pattern:* keep a **window** of `k` items. To move it one step, **add the new item on the right and subtract the old item on the left**. Never recompute the whole window.

```python
def max_window_sum(items, k):
    window = sum(items[:k])               # the first window
    best = window
    for right in range(k, len(items)):
        window += items[right] - items[right - k]     # slide: add the new, remove the old
        best = max(best, window)
    return best

print(max_window_sum([2, 1, 5, 1, 3, 2], 3))
```

**Output**

```text
9
```

**Cost.** **O(n)**: each item enters the window once and leaves once.

The window can also *grow and shrink* to fit a rule. **Longest substring without repeating characters:** expand the right edge; if a repeat appears, shrink from the left until the window is valid again.

```python
def longest_unique_substring(text):
    last_seen = {}                              # character -> the index where we last saw it
    start, best = 0, 0
    for end, ch in enumerate(text):
        if ch in last_seen and last_seen[ch] >= start:
            start = last_seen[ch] + 1            # shrink: jump past the previous copy
        last_seen[ch] = end
        best = max(best, end - start + 1)
    return best

print(longest_unique_substring("abcabcbb"), longest_unique_substring("bbbb"), longest_unique_substring("pwwkew"))
```

**Output**

```text
3 1 3
```


### Pattern 4: Kadane's algorithm (best subarray)

**Question.** Find the contiguous sub-list with the **largest sum**. `[−2, 1, −3, 4, −1, 2, 1, −5, 4]` has the answer `4 + (−1) + 2 + 1 = 6`.

*Slow way:* try every start and end: O(n²) (or O(n³)).

**The idea (a story).** You walk along the road collecting coins and paying tolls (positive and negative numbers). You keep a running total of **your current stretch**. If your running total ever goes *negative*, that stretch is just dragging you down: **drop it and start fresh** from the next item. Remember the best total you ever saw.

```python
def max_subarray(items):
    current = best = items[0]
    for value in items[1:]:
        current = max(value, current + value)    # extend the stretch, or start over from here
        best = max(best, current)
    return best

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), max_subarray([-3, -1, -2]))
```

**Output**

```text
6 -1
```

**Cost.** **O(n)** time, **O(1)** space. It is also your first taste of **dynamic programming**: `current` is "the best answer ending exactly here", built from the previous one.


### Pattern 5: counting with a dictionary

When a question asks *"how many of each?"* or *"have I seen this before?"*, a dictionary (chapter 18) turns an O(n²) search into O(n).

**Question.** Return the index of two numbers that add to a target (the list is **not** sorted): the famous **Two Sum**.

```python
def two_sum(items, target):
    seen = {}                                        # value -> index where we saw it
    for i, value in enumerate(items):
        need = target - value
        if need in seen:                             # have we already met the partner?
            return seen[need], i
        seen[value] = i
    return None

print(two_sum([2, 7, 11, 15], 9), two_sum([3, 2, 4], 6), two_sum([1, 2], 10))
```

**Output**

```text
(0, 1) (1, 2) None
```

**Cost.** **O(n)** time and O(n) space: one trip through the list, one O(1) lookup per item. This is the space-for-time trade from chapter 4.


---

## A bonus: rotate a list with three reversals

Rotate `[1, 2, 3, 4, 5, 6, 7]` to the right by 3 to get `[5, 6, 7, 1, 2, 3, 4]`, **in place**, with O(1) extra space. The trick: *reverse everything, then reverse the first `k`, then reverse the rest.*

```python
def reverse_range(items, low, high):
    while low < high:
        items[low], items[high] = items[high], items[low]
        low += 1
        high -= 1

def rotate_right(items, k):
    n = len(items)
    k %= n                                   # rotating by n changes nothing
    reverse_range(items, 0, n - 1)
    reverse_range(items, 0, k - 1)
    reverse_range(items, k, n - 1)

numbers = [1, 2, 3, 4, 5, 6, 7]
rotate_right(numbers, 3)
print(numbers)
```

**Output**

```text
[5, 6, 7, 1, 2, 3, 4]
```


---

## Choosing the pattern

| The question smells like... | Try |
|---|---|
| "sum / count in a range", many queries | **Prefix sums** |
| Sorted list, pairs, or "from both ends" | **Two pointers** |
| "best / longest **contiguous** stretch of length k or with a rule" | **Sliding window** |
| "maximum sum / best ending here" | **Kadane / running best** |
| "have I seen it?", "how many of each?", "find the partner" | **Dictionary or set** |

---

## Common mistakes

- **Off-by-one in ranges.** `range(k, len(items))`, `prefix[j + 1] - prefix[i]`: draw a tiny example.
- **Modifying a list while looping over it.** Loop over a copy or use two pointers.
- **`[[0] * m] * n`** for grids.
- **Assuming a list is sorted** before using two pointers or binary search.
- **Forgetting empty and single-element lists**, and all-negative lists (Kadane).
- **`insert(0, ...)` in a loop.** It makes the loop O(n²); use a deque or build in reverse.

---

## Practice

1. 🟢 Find the second largest distinct number in one pass.
2. 🟢 Move all zeros to the end, keeping the order of the others, **in place**.
3. 🟡 Given a list and `k`, find the first non-repeating element in every window of size `k`.
4. 🟡 Return the product of all other elements for each position **without division** (use prefix and suffix products).
5. 🟡 Find the length of the longest run of 1s if you may flip at most one 0 (a sliding window).
6. 🔴 Find the smallest sub-list whose sum is at least `target` (a growing and shrinking window).
7. 🔴 Sort a list containing only 0, 1 and 2 in one pass and O(1) space (the Dutch national flag).

<details>
<summary>Hints</summary>

2. A "write" pointer for the next non-zero; a "read" pointer scanning.
4. `answer[i] = (product of everything before i) * (product of everything after i)`; two passes.
5. Keep a window that contains at most one zero; shrink from the left when a second zero enters.
6. Expand the right edge adding items; while the sum is enough, record the length and shrink from the left.
7. Three regions with pointers `low`, `mid`, `high`: swap 0s to the front, 2s to the back.
</details>

---

[← 13. Backtracking: Choose, Explore, Undo](13-backtracking.md) · [Handbook contents](README.md) · [15. Linked Lists →](15-linked-list.md)
