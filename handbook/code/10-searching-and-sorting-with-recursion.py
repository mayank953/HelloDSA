"""10. Searching and Sorting with Recursion

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 10-searching-and-sorting-with-recursion.py
"""

def linear_search(items, x, i=0):
    if i == len(items):             # base case: ran off the end, x is not here
        return False
    if items[i] == x:               # found it: no need to look any further
        return True
    return linear_search(items, x, i + 1)

print(linear_search([4, 9, 2, 7], 2), linear_search([4, 9, 2, 7], 5))

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

def merge_sort(items):
    if len(items) <= 1:                          # base case
        return items[:]
    mid = len(items) // 2
    sorted_left = merge_sort(items[:mid])        # assume: the left half, sorted
    sorted_right = merge_sort(items[mid:])       # assume: the right half, sorted
    return merge(sorted_left, sorted_right)      # my part

print(merge_sort([5, 2, 4, 7, 1, 3, 2, 6]))

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

def partition_is_correct(items, low, high):
    p = partition(items, low, high)
    pivot = items[p]
    return all(x <= pivot for x in items[low:p]) and all(x > pivot for x in items[p + 1:high + 1])

print(partition_is_correct([7, 1, 8, 3, 3, 9, 4], 0, 6))

print('\n[all code in this chapter ran successfully]')
