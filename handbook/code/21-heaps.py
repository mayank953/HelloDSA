"""21. Heaps and Priority Queues

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 21-heaps.py
"""

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

order = []
while heap.items:
    order.append(heap.pop())
    print(f"pop -> {order[-1]},  heap is now {heap.items}")

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

import heapq

numbers = [5, 3, 8, 1, 9, 2]
heapq.heapify(numbers)                  # O(n), in place
heapq.heappush(numbers, 0)              # O(log n)
print(heapq.heappop(numbers))           # O(log n): the smallest
print(numbers[0])                       # O(1): peek at the new smallest
print(heapq.nsmallest(3, numbers), heapq.nlargest(2, numbers))

max_heap = []
for value in [5, 3, 8]:
    heapq.heappush(max_heap, -value)
print(-heapq.heappop(max_heap))         # 8: the largest

import itertools
order = itertools.count()
queue = []
for priority, task in [(2, "write report"), (1, "fix outage"), (2, "reply to email"), (1, "call client")]:
    heapq.heappush(queue, (priority, next(order), task))        # (priority, arrival number, task)

while queue:
    priority, _, task = heapq.heappop(queue)
    print(priority, task)

def heap_sort(items):
    heap = items[:]
    heapq.heapify(heap)                                   # O(n)
    return [heapq.heappop(heap) for _ in range(len(heap))]   # n pops of O(log n)

print(heap_sort([9, 4, 7, 1, 8, 2, 6]))

def k_largest(numbers, k):
    heap = []                                       # the k largest so far (a MIN-heap)
    for x in numbers:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:                           # better than the weakest of our top k
            heapq.heapreplace(heap, x)              # pop the root and push x in one step
    return sorted(heap, reverse=True)

print(k_largest([4, 9, 1, 7, 3, 8, 2, 10, 5], 3))

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

print('\n[all code in this chapter ran successfully]')
