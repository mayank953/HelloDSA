"""14. Arrays and Lists

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 14-arrays-and-lists.py
"""

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

grid = [[0] * 3] * 3          # looks like 3 rows of 3 zeros...
grid[0][0] = 7
print(grid)                    # ...but we changed every row!

grid = [[0] * 3 for _ in range(3)]    # a fresh row each time
grid[0][0] = 7
print(grid)

def build_prefix(items):
    prefix = [0]
    for value in items:
        prefix.append(prefix[-1] + value)       # each entry = the previous entry + one more item
    return prefix

data = [3, 1, 4, 1, 5, 9, 2, 6]
prefix = build_prefix(data)
print(prefix)
print("sum of data[2..5] =", prefix[6] - prefix[2], "  (check:", sum(data[2:6]), ")")

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

def max_window_sum(items, k):
    window = sum(items[:k])               # the first window
    best = window
    for right in range(k, len(items)):
        window += items[right] - items[right - k]     # slide: add the new, remove the old
        best = max(best, window)
    return best

print(max_window_sum([2, 1, 5, 1, 3, 2], 3))

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

def max_subarray(items):
    current = best = items[0]
    for value in items[1:]:
        current = max(value, current + value)    # extend the stretch, or start over from here
        best = max(best, current)
    return best

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), max_subarray([-3, -1, -2]))

def two_sum(items, target):
    seen = {}                                        # value -> index where we saw it
    for i, value in enumerate(items):
        need = target - value
        if need in seen:                             # have we already met the partner?
            return seen[need], i
        seen[value] = i
    return None

print(two_sum([2, 7, 11, 15], 9), two_sum([3, 2, 4], 6), two_sum([1, 2], 10))

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

print('\n[all code in this chapter ran successfully]')
