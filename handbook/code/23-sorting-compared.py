"""23. Sorting Algorithms Compared

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 23-sorting-compared.py
"""

students = [("Asha", 2), ("Ravi", 2), ("Meera", 1), ("Karan", 2), ("Zoya", 1)]   # (name, class), already by name

def selection_sort_by_class(items):
    items = items[:]
    for i in range(len(items) - 1):
        smallest = min(range(i, len(items)), key=lambda j: items[j][1])    # the first smallest class from i onward
        items[i], items[smallest] = items[smallest], items[i]               # a long-distance swap
    return items

print("stable (Python sorted):", sorted(students, key=lambda s: s[1]))
print("unstable (selection)  :", selection_sort_by_class(students))

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

import math

print(f"{'n':>6} | {'log2(n!)':>12} | {'n * log2(n)':>12}")
for n in [10, 100, 1000, 10_000]:
    print(f"{n:>6} | {math.log2(math.factorial(n)):>12,.0f} | {n * math.log2(n):>12,.0f}")

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

words = ["pear", "fig", "banana", "kiwi", "apple"]

print(sorted(words))                              # a new sorted list
print(sorted(words, key=len))                     # sort by a key (stable, so ties keep input order)
print(sorted(words, key=len, reverse=True))       # biggest key first
words.sort()                                      # sorts in place, returns None
print(words)

rows = [("Asha", 2, 88), ("Ravi", 1, 92), ("Meera", 2, 95), ("Karan", 1, 92), ("Zoya", 2, 88)]

by_tuple = sorted(rows, key=lambda r: (r[1], -r[2]))          # class ascending, marks descending
two_pass = sorted(sorted(rows, key=lambda r: -r[2]), key=lambda r: r[1])   # marks first, then class: stable!
print([r[0] for r in by_tuple])
print([r[0] for r in two_pass])

from functools import cmp_to_key

def largest_number(numbers):
    pieces = [str(x) for x in numbers]
    pieces.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)))
    return "".join(pieces).lstrip("0") or "0"

print(largest_number([3, 30, 34, 5, 9]))

print('\n[all code in this chapter ran successfully]')
