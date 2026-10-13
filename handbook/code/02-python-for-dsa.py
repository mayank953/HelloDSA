"""02. Python You Need for DSA

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 02-python-for-dsa.py
"""

a = [1, 2, 3]
b = a            # NOT a copy. We stuck a second label on the SAME list.
b.append(4)

print("a =", a)
print("b =", b)
print("same object?", a is b)

a = [1, 2, 3]
c = a.copy()     # or a[:] or list(a): a brand new list with the same items
c.append(4)

print("a =", a)
print("c =", c)
print("same object?", a is c)

def add_item(item, bucket=[]):      # the [] is created ONCE, when the function is defined
    bucket.append(item)
    return bucket

print(add_item("pen"))
print(add_item("book"))    # surprise: the same bucket is reused

def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

print(add_item("pen"))
print(add_item("book"))

depth = 0

def trace(fn):
    """Wrap a function so every call and return is printed with indentation."""
    def wrapper(*args):
        global depth
        print("    " * depth + f"enter {fn.__name__}{args}")
        depth += 1
        result = fn(*args)
        depth -= 1
        print("    " * depth + f"leave {fn.__name__}{args} -> {result}")
        return result
    wrapper.__name__ = fn.__name__
    return wrapper

@trace
def cook(dish):
    return f"{dish} ready"

@trace
def prepare_meal():
    starter = cook("soup")
    main = cook("rice")
    return starter + " and " + main

prepare_meal()

def show(n):
    message = f"I am the call with n = {n}"
    return message

print(show(1))
print(show(2))

counter = 0

def count_calls():
    global counter          # without this line Python would create a new local 'counter'
    counter += 1

count_calls(); count_calls(); count_calls()
print("counter =", counter)

import sys
print("Python allows at most about", sys.getrecursionlimit(), "nested calls")

numbers = [10, 20, 30, 40]
rest = numbers[1:]

print(rest)
print("is rest the same list as numbers?", rest is numbers)

rest[0] = 999                     # changing the copy...
print("numbers is unchanged:", numbers)

# 1. enumerate: index and value together
for index, fruit in enumerate(["apple", "banana", "cherry"]):
    print(index, fruit)

# 2. swap two variables without a temporary
a, b = 3, 8
a, b = b, a
print(a, b)

# 3. sorted with a key (sort words by length, then alphabetically)
print(sorted(["pear", "fig", "banana", "kiwi"], key=lambda w: (len(w), w)))

# 4. integer division and remainder: the engine of many digit problems
print(1234 // 10, 1234 % 10)
print(divmod(1234, 10))

# 5. negative numbers behave differently in // and %
print(-7 // 2, -7 % 2)

from collections import Counter, defaultdict, deque
import heapq, bisect

print(Counter("banana"))                       # 6. count things
groups = defaultdict(list)                     # 7. a dict that creates missing lists
for word in ["eat", "tea", "tan", "ate"]:
    groups["".join(sorted(word))].append(word)
print(dict(groups))

queue = deque([1, 2, 3])                       # 8. a double-ended queue
queue.appendleft(0); queue.pop()
print(queue)

heap = [5, 1, 4]                               # 9. a min-heap on a plain list
heapq.heapify(heap)
print(heapq.heappop(heap))

print(bisect.bisect_left([1, 3, 5, 7], 5))     # 10. binary search for a position

# A tiny, honest test harness: one line per check
def check(label, got, expected):
    status = "ok " if got == expected else "FAIL"
    print(f"{status} {label}: got {got!r}, expected {expected!r}")

check("sum of empty", sum([]), 0)
check("sum of three", sum([4, 1, 7]), 12)

print('\n[all code in this chapter ran successfully]')
