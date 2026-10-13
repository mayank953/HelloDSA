"""09. Recursion on Arrays

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 09-recursion-on-arrays.py
"""

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

def sum_array(items):
    if len(items) == 0:                 # base case
        return 0
    small_answer = sum_array(items[1:])  # assume: the sum of everything after me
    return items[0] + small_answer       # my part

print(sum_array([4, 1, 7]), sum_array([]))

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

def is_sorted(items):
    if len(items) <= 1:
        return True
    rest_is_sorted = is_sorted(items[1:])
    return items[0] <= items[1] and rest_is_sorted

print(is_sorted([1, 2, 2, 5]), is_sorted([1, 3, 2]), is_sorted([]))

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

def first_index(items, x, i=0):
    if i == len(items):             # ran off the end: x is not here
        return -1
    if items[i] == x:               # found it: my part answers the question right away
        return i
    return first_index(items, x, i + 1)    # not me: let the rest search

print(first_index([5, 3, 8, 3, 1], 3), first_index([5, 3, 8], 7))

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

def last_index(items, x, i=0):
    if i == len(items):
        return -1
    in_the_rest = last_index(items, x, i + 1)      # assume: the last index of x at positions after me
    if in_the_rest != -1:
        return in_the_rest
    return i if items[i] == x else -1              # nothing after me, so is it me?

print(last_index([5, 3, 8, 3, 1], 3), last_index([5, 3, 8], 7))

def print_indices(items, x, i=0):
    if i == len(items):
        return
    if items[i] == x:
        print(i)                       # the kid stands up and shouts
    print_indices(items, x, i + 1)

print_indices([3, 2, 5, 2, 8, 2, 1], 2)

def collect_indices(items, x, i, diary):
    if i == len(items):
        return
    if items[i] == x:
        diary.append(i)                      # write into the diary we were handed
    collect_indices(items, x, i + 1, diary)  # pass the SAME diary onward

diary = []
collect_indices([3, 2, 5, 2, 8, 2, 1], 2, 0, diary)
print(diary)

desk_diary = []                              # lives outside every function

def global_indices(items, x, i=0):
    if i == len(items):
        return
    if items[i] == x:
        desk_diary.append(i)
    global_indices(items, x, i + 1)

global_indices([3, 2, 5, 2, 8, 2, 1], 2)
print(desk_diary)

global_indices([3, 2, 5, 2, 8, 2, 1], 2)
print(desk_diary)

def return_indices(items, x, i=0):
    if i == len(items):
        return []                                  # base case: an empty paper
    small_answer = return_indices(items, x, i + 1) # assume: the paper from everyone behind me
    if items[i] == x:
        return [i] + small_answer                  # my part: I add myself to the front
    return small_answer                            # not me: pass the paper up unchanged

print(return_indices([3, 2, 5, 2, 8, 2, 1], 2))
print(return_indices([3, 2, 5, 2, 8, 2, 1], 9))

def return_indices_slicing(items, x):
    if len(items) == 0:
        return []
    small_answer = return_indices_slicing(items[1:], x)
    shifted = [i + 1 for i in small_answer]       # every index moves one place right
    return ([0] + shifted) if items[0] == x else shifted

print(return_indices_slicing([3, 2, 5, 2, 8, 2, 1], 2))

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

print('\n[all code in this chapter ran successfully]')
