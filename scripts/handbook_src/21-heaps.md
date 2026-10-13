## The emergency room

A hospital's emergency room does not treat patients in the order they arrived. A broken arm waits; a heart attack is seen **first**, even if it arrived last. The next patient to be served is always **the most urgent one waiting right now**, and new patients with new urgency keep arriving.

That is a **priority queue**: like a queue, but "who goes next" is decided by **priority**, not by arrival time. Operations:

- **push** an item with a priority,
- **peek** at the most urgent item,
- **pop** (remove) the most urgent item.

How would you build it? Two obvious attempts both fall short:

| Attempt | Find the most urgent | Insert a new one |
|---|---|---|
| Keep an **unsorted list** | scan everything: O(n) | append: O(1) |
| Keep a **sorted list** | the first item: O(1) | shift to place it: O(n) |

Somebody always pays O(n). A **heap** makes *both* operations **O(log n)** (and peeking O(1)), by being **only partly ordered**: just ordered enough to always know the winner.

> Throughout, we use a **min-heap**: the item with the **smallest** value is the most urgent. (A max-heap is the mirror image; see the Python section for the one-line trick.)

---

## The heap: a tree stored in an array

A heap is a **binary tree** with two properties:

1. **Shape.** It is *complete*: every level is full except possibly the last, which fills from the left. No gaps.
2. **Heap property (min-heap).** Every node is **less than or equal to its children**. So the **root is the smallest** item.

```text
            1
          /   \
         3     2
        / \   /
       9   5 8
```

Careful: this is **not** a sorted tree. `3` is on the left of `2`, and `9` is a child of `3` while `8` is a child of `2`. The only promise is "**a parent is never bigger than its children**". That is much weaker than a BST, and *that weakness is the secret of its speed*: it is cheap to maintain.

### Stored in a plain list

Because the shape is complete (no gaps), we do not need pointers. We store the tree **level by level in an array**, and arithmetic on indexes replaces pointers:

```text
 index:   0  1  2  3  4  5
 value: [ 1, 3, 2, 9, 5, 8 ]

 for the node at index i:
     left child   = 2*i + 1
     right child  = 2*i + 2
     parent       = (i - 1) // 2
```

Check: the node at index 1 (value 3) has children at indexes 3 and 4 (values 9 and 5) ✓, and its parent is at `(1 − 1) // 2 = 0` (value 1) ✓.

---

## Push: add at the end, then sift up

To add a value, put it in the next free spot (the end of the array, which keeps the shape), then fix the heap property: while the new item is **smaller than its parent**, **swap them**. It "bubbles up" (*sift up*) until it finds its place.

Pop is the trickier one. To remove the root (the minimum): take the **last** item and put it at the root (keeping the shape), then **sift down**: while it is **larger than a child**, swap it with the **smaller** child.

```python
class MinHeap:
    def __init__(self):
        self.items = []
        self.swaps = 0                                  # for our experiments

    def peek(self):
        return self.items[0]

    def push(self, value):
        self.items.append(value)                        # next free spot keeps the tree complete
        self._sift_up(len(self.items) - 1)

    def pop(self):
        if not self.items:
            raise IndexError("pop from an empty heap")
        smallest = self.items[0]
        last = self.items.pop()                         # remove the last leaf...
        if self.items:
            self.items[0] = last                        # ...and move it to the root
            self._sift_down(0)
        return smallest

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.items[i] < self.items[parent]:      # smaller than its parent: swap upward
                self.items[i], self.items[parent] = self.items[parent], self.items[i]
                self.swaps += 1
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self.items)
        while True:
            left, right, smallest = 2 * i + 1, 2 * i + 2, i
            if left < n and self.items[left] < self.items[smallest]:
                smallest = left
            if right < n and self.items[right] < self.items[smallest]:
                smallest = right
            if smallest == i:                           # heavier than neither child: done
                break
            self.items[i], self.items[smallest] = self.items[smallest], self.items[i]
            self.swaps += 1
            i = smallest

heap = MinHeap()
for value in [5, 3, 8, 1, 9, 2]:
    heap.push(value)
    print(f"push {value}: {heap.items}")
```

Walk through the pushes: `1` arrives last-but-two and bubbles all the way to the top; `2` rises one level.

Now pop everything and see the items come out **in sorted order**:

```python
order = []
while heap.items:
    order.append(heap.pop())
    print(f"pop -> {order[-1]},  heap is now {heap.items}")
```

```python hide
h = MinHeap()
for v in [5, 3, 8, 1, 9, 2]: h.push(v)
assert [h.pop() for _ in range(6)] == [1, 2, 3, 5, 8, 9]
import random, heapq
rng = random.Random(6)
for _ in range(100):
    data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
    m = MinHeap()
    for v in data: m.push(v)
    assert [m.pop() for _ in range(len(data))] == sorted(data)
```

**Why O(log n)?** The tree is complete, so its height is about `log₂ n`. Sifting up or down moves along **one path** from a leaf to the root (or back), so it makes at most `log n` swaps.

---

## Heapify: building a heap in O(n)

Given a ready-made list, we could push the items one at a time: `n` pushes of `log n` each is **O(n log n)**. There is a cleverer way, **heapify**, that does it in **O(n)**: treat the list as a tree already, then fix it **bottom-up**. Start at the **last parent** and *sift down* each node, moving backwards to the root. (Leaves are already valid one-node heaps, so we skip the second half of the array.)

```python
def heapify(items):
    """Turn a list into a min-heap in place; return the number of swaps made."""
    swaps = 0
    n = len(items)
    for start in range(n // 2 - 1, -1, -1):            # from the last parent down to the root
        i = start
        while True:
            left, right, smallest = 2 * i + 1, 2 * i + 2, i
            if left < n and items[left] < items[smallest]:
                smallest = left
            if right < n and items[right] < items[smallest]:
                smallest = right
            if smallest == i:
                break
            items[i], items[smallest] = items[smallest], items[i]
            swaps += 1
            i = smallest
    return swaps

# Worst-case input for a min-heap: the biggest values first.
n = 4096
descending = list(range(n, 0, -1))

by_pushing = MinHeap()
for value in descending:
    by_pushing.push(value)

ready_made = descending[:]
heapify_swaps = heapify(ready_made)

print(f"n = {n}: building by {n} pushes needs {by_pushing.swaps:,} swaps")
print(f"n = {n}: heapify needs                {heapify_swaps:,} swaps")
```

Why is heapify cheaper? Half the nodes are leaves and need **no** work; a quarter can move at most **one** level; an eighth at most two; and so on. The total is `n/4·1 + n/8·2 + n/16·3 + ... < n`, a convergent series: **O(n)**.

```python hide
assert heapify_swaps < n and by_pushing.swaps > 10 * n
check = [5, 3, 8, 1, 9, 2]; heapify(check)
assert all(check[(i - 1) // 2] <= check[i] for i in range(1, len(check)))
```

---

## Python's `heapq`

You will use the standard library, not your own class, in real programs. `heapq` works on a **plain list** that it keeps in heap order.

```python
import heapq

numbers = [5, 3, 8, 1, 9, 2]
heapq.heapify(numbers)                  # O(n), in place
heapq.heappush(numbers, 0)              # O(log n)
print(heapq.heappop(numbers))           # O(log n): the smallest
print(numbers[0])                       # O(1): peek at the new smallest
print(heapq.nsmallest(3, numbers), heapq.nlargest(2, numbers))
```

**There is no max-heap**, but there is a standard trick: store the **negated** values, since the smallest negative is the largest original.

```python
max_heap = []
for value in [5, 3, 8]:
    heapq.heappush(max_heap, -value)
print(-heapq.heappop(max_heap))         # 8: the largest
```

**Priorities and ties.** Push **tuples** `(priority, item)`. Tuples compare element by element, so the smallest priority wins. If two priorities tie, Python then compares the *items*, which may not be comparable. Insert a counter as a tiebreaker:

```python
import itertools
order = itertools.count()
queue = []
for priority, task in [(2, "write report"), (1, "fix outage"), (2, "reply to email"), (1, "call client")]:
    heapq.heappush(queue, (priority, next(order), task))        # (priority, arrival number, task)

while queue:
    priority, _, task = heapq.heappop(queue)
    print(priority, task)
```

Equal priorities come out in **arrival order**, thanks to the counter.

```python hide
assert heapq.nsmallest(3, [5, 3, 8, 1, 9, 2]) == [1, 2, 3]
mh = []
for v in [5, 3, 8]: heapq.heappush(mh, -v)
assert -heapq.heappop(mh) == 8
```

---

## Heap sort

Push everything into a heap and pop everything out: the items emerge in sorted order. Time **O(n log n)** in every case, and (with an in-place variant) **O(1)** extra space.

```python
def heap_sort(items):
    heap = items[:]
    heapq.heapify(heap)                                   # O(n)
    return [heapq.heappop(heap) for _ in range(len(heap))]   # n pops of O(log n)

print(heap_sort([9, 4, 7, 1, 8, 2, 6]))
```

```python hide
assert heap_sort([9, 4, 7, 1, 8, 2, 6]) == [1, 2, 4, 6, 7, 8, 9] and heap_sort([]) == []
```

It is a solid worst-case guarantee, but quick sort is usually faster in practice (better memory behaviour), and merge sort is stable. We compare them all in chapter 23.

---

## The heap's best work: top-k problems

**Question.** From a stream of a million numbers, find the **k largest**. (Sorting everything costs O(n log n).)

**Idea.** Keep a **min-heap of size k** holding the *k largest seen so far*. Its root is the **smallest of those k**: the one "on the bubble". For each new number: if it beats the root, replace the root with it. Otherwise ignore it.

```python
def k_largest(numbers, k):
    heap = []                                       # the k largest so far (a MIN-heap)
    for x in numbers:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:                           # better than the weakest of our top k
            heapq.heapreplace(heap, x)              # pop the root and push x in one step
    return sorted(heap, reverse=True)

print(k_largest([4, 9, 1, 7, 3, 8, 2, 10, 5], 3))
```

**Cost.** Each number costs at most O(log k), so **O(n log k)** overall, and only **O(k) memory**: it works on data that does not even fit in memory, because you only ever look at one item at a time.

### Merge k sorted lists

Remember merging two sorted lists (chapters 10 and 15). For `k` lists, keep a heap holding **the current front item of each list**. Pop the smallest, then push the *next* item from the same list.

```python
def merge_k_sorted(lists):
    heap = []
    for list_index, items in enumerate(lists):
        if items:
            heapq.heappush(heap, (items[0], list_index, 0))        # (value, which list, position)
    merged = []
    while heap:
        value, list_index, position = heapq.heappop(heap)
        merged.append(value)
        if position + 1 < len(lists[list_index]):
            heapq.heappush(heap, (lists[list_index][position + 1], list_index, position + 1))
    return merged

print(merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9, 10]]))
```

Total cost **O(N log k)** for `N` items overall. The heap never holds more than `k` entries.

### Running median with two heaps

**Question.** Numbers arrive one at a time. After each, report the **median**. Re-sorting each time is O(n log n) per step.

**Idea (a story).** Split the numbers at the median into two halves: the **lower half** and the **upper half**. We only need the **largest of the lower half** and the **smallest of the upper half**, so keep the lower half in a **max-heap** and the upper half in a **min-heap**. Keep their sizes equal (or the lower half one bigger). The median is at the tops.

```python
class MedianFinder:
    def __init__(self):
        self.low = []        # max-heap (stored negated): the smaller half
        self.high = []       # min-heap: the larger half

    def add(self, number):
        heapq.heappush(self.low, -number)                           # 1. put it in the lower half...
        heapq.heappush(self.high, -heapq.heappop(self.low))         # 2. ...then move the lower half's largest across
        if len(self.high) > len(self.low):                          # 3. keep the lower half at least as big
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2

finder = MedianFinder()
for number in [5, 15, 1, 3, 8]:
    finder.add(number)
    print(f"after {number:>2}: median = {finder.median()}")
```

Each `add` is **O(log n)** and each `median` is **O(1)**.

```python hide
assert k_largest([4, 9, 1, 7, 3, 8, 2, 10, 5], 3) == [10, 9, 8] and k_largest([1], 3) == [1]
assert merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9, 10]]) == list(range(1, 11)) and merge_k_sorted([[], []]) == []
import statistics
rng = random.Random(11)
mf, seen = MedianFinder(), []
for _ in range(200):
    x = rng.randint(-100, 100); mf.add(x); seen.append(x)
    assert mf.median() == statistics.median(seen)
```

---

## Where heaps hide

- **Dijkstra's shortest path** and **A\*** search (chapter 22): always expand the closest unexplored node.
- **Operating-system schedulers** and **event simulations**: the next event is the soonest one.
- **Huffman coding** for compression: repeatedly merge the two lightest nodes.
- **"Top k"** features everywhere: trending items, leaderboards, nearest neighbours (chapter 28).

---

## Common mistakes

- **Thinking a heap is sorted.** Only the root is guaranteed to be the minimum. `heap[1]` is *not* the second smallest.
- **Forgetting `heapq` is a min-heap only.** Negate values for a max-heap, and remember to negate back.
- **Pushing tuples whose second elements cannot be compared.** Add a tiebreaker counter.
- **Iterating a heap list and expecting sorted output.** Pop to get order.
- **Calling `heapq.heappush` on a list that has not been heapified** (when it was filled by other means). Heapify first.
- **Using a sorted list to emulate a priority queue** and paying O(n) per insert.

---

## Practice

1. 🟢 Find the **k-th largest** element of a list (use a min-heap of size k).
2. 🟢 Given a list of stone weights, repeatedly smash the two heaviest (if equal both vanish, else the difference remains). What is the last stone?
3. 🟡 Return the **k most frequent** words (a Counter plus a heap).
4. 🟡 *Task scheduler:* tasks with cooldowns. How long does it take to run them all?
5. 🟡 Sort a list in which every element is **at most k positions away** from its sorted place, in O(n log k).
6. 🟡 Connect ropes with minimum total cost (always join the two shortest).
7. 🔴 Implement a **max-heap class** without negation, and a **heap with decrease-key** (you will need it for Dijkstra).
8. 🔴 *Meeting rooms II:* the minimum number of rooms needed for a list of `(start, end)` meetings.

<details>
<summary>Hints</summary>

2. Use a max-heap (negate) and pop twice per round.
5. Keep a min-heap of the next `k + 1` elements; pop the smallest each time and push the next.
6. Pop two, add them, push the sum, repeat; the total of all sums is the cost.
8. Sort by start time; keep a min-heap of end times; reuse a room if the earliest end is not after the new start.
</details>
