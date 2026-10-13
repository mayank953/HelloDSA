## Why a whole chapter on Python?

Because DSA is not really about Python. It is about *what happens inside the computer*. Python just happens to be a language where you can watch it happen without drowning in syntax.

If you understand four things (**names and references, the call stack, scope, and what slicing costs**) then recursion, linked lists, trees and dynamic programming all stop being mysterious. Most "I don't get recursion" problems are actually "I don't get what a function call does" problems.

> This chapter is the *prerequisite* the video asks for. If any part feels new, the free [Hello Python course](https://github.com/mayank953/python-ai-crash-course) covers functions, scope and slicing in depth.

---

## 1. A variable is a label, not a box

Most beginners imagine `a = 5` as "a box called `a` containing 5". For numbers that picture is harmless. For lists it quietly causes bugs.

A better picture: **the list lives somewhere in memory, and `a` is a sticky label with that address written on it.**

```python
a = [1, 2, 3]
b = a            # NOT a copy. We stuck a second label on the SAME list.
b.append(4)

print("a =", a)
print("b =", b)
print("same object?", a is b)
```

Two labels, one list. Change it through either label and both see the change. This is the exact trap behind the "teacher's diary" idea we use in recursion: when you **pass a list into a function, you pass the label, not a copy**, so the function can write into your list.

To really copy:

```python
a = [1, 2, 3]
c = a.copy()     # or a[:] or list(a): a brand new list with the same items
c.append(4)

print("a =", a)
print("c =", c)
print("same object?", a is c)
```

**Numbers, strings and tuples are immutable** (they cannot be changed in place), so you cannot spoil them through a second label. Lists, dictionaries and sets are **mutable**: they can.

```python hide
x = [1]; y = x; y.append(2)
assert x == [1, 2] and x is y
z = x.copy(); z.append(3)
assert x == [1, 2] and z == [1, 2, 3]
```

### The classic trap: the mutable default argument

```python
def add_item(item, bucket=[]):      # the [] is created ONCE, when the function is defined
    bucket.append(item)
    return bucket

print(add_item("pen"))
print(add_item("book"))    # surprise: the same bucket is reused
```

The fix is to use `None` as the default and create the list inside:

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

print(add_item("pen"))
print(add_item("book"))
```

You will meet this in recursion whenever you want an optional "answer so far" list. Remember the fix.

---

## 2. What a function call really does

When Python calls a function it creates a **frame**: a small private workspace that holds that call's parameters and local variables, plus a note of *where to come back to*. Frames are stacked one on top of the other. This pile is the **call stack**.

Think of a pile of plates in a canteen. The newest call goes on top. A call can only finish when it is on top. When it finishes, its plate is removed and Python returns to the plate underneath, **exactly at the line where that call was made**.

Watch it happen. This little tracer prints a line every time a function is entered and left, indented by how deep we are:

```python
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
```

Read it slowly. `prepare_meal` enters first and **waits** while `cook("soup")` runs completely. Only after `cook("soup")` has left does `prepare_meal` continue to its next line. At no point are two `cook` calls alive at the same time here, but `prepare_meal` is alive during both. That is the stack: **callers wait for callees**.

### Each frame has its own variables

```python
def show(n):
    message = f"I am the call with n = {n}"
    return message

print(show(1))
print(show(2))
```

Two calls, two separate `message` variables. They never touch each other. This is the reason recursion works at all: when a function calls itself, the new call gets its **own** `n`, its own everything.

### Scope: local, global and the one-way mirror

A variable made inside a function is **local**: it disappears when the frame is removed. A variable made outside is **global** and can be *read* anywhere. To *rebind* a global from inside a function you must say `global`.

```python
counter = 0

def count_calls():
    global counter          # without this line Python would create a new local 'counter'
    counter += 1

count_calls(); count_calls(); count_calls()
print("counter =", counter)
```

```python hide
assert counter == 3
```

Global variables are the "diary lying on the desk" approach we compare in the arrays chapter. They work, but they are shared by every call, so they are easy to forget to reset.

---

## 3. Python's built-in safety net: the recursion limit

Stack frames take memory, so Python does not let the stack grow forever. It stops you at a fixed depth.

```python
import sys
print("Python allows at most about", sys.getrecursionlimit(), "nested calls")
```

Go past that depth and you get a `RecursionError`. The famous website *Stack Overflow* is named after exactly this error, "stack overflow".

```python expect-error
def go_deeper(n):
    return go_deeper(n + 1)        # no way to stop

go_deeper(0)
```

You can raise the limit with `sys.setrecursionlimit(...)`, but that only delays the problem. If a solution needs a depth of a million, the fix is a better algorithm, not a bigger limit.

---

## 4. Slicing makes a copy (and copies cost time)

`numbers[1:]` looks like "everything except the first item". What Python actually does is **build a brand new list** and copy `n - 1` items into it.

```python
numbers = [10, 20, 30, 40]
rest = numbers[1:]

print(rest)
print("is rest the same list as numbers?", rest is numbers)

rest[0] = 999                     # changing the copy...
print("numbers is unchanged:", numbers)
```

That is why recursive solutions that slice a list at every step (`f(l[1:])`) are easy to write but cost extra time and memory. In the video the "better" versions pass an **index** instead of slicing. We measure exactly how much this matters in the next two chapters.

```python hide
assert rest is not numbers and numbers == [10, 20, 30, 40]
```

---

## 5. Python tools you will use all the time

You do not need many. These ten cover almost everything in this handbook.

```python
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
```

```python
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
```

```python hide
assert divmod(1234, 10) == (123, 4)
assert -7 // 2 == -4 and -7 % 2 == 1
assert Counter("banana")["a"] == 3
```

---

## 6. Habits that save hours

- **Test on tiny inputs first.** Empty list, one item, two items. If it works there you have usually found the shape of the solution.
- **Use `assert` as a seatbelt.** `assert total([1, 2]) == 3` takes five seconds to write and catches silly mistakes forever.
- **Print the inputs of each call** when a recursion misbehaves. The tracer above does this for you.
- **Name things for what they mean.** `small_answer`, `taken_so_far`, `remaining` read like the story. `x1`, `tmp2` do not.
- **Return, do not just print**, unless the question says "print". Returned values can be tested, combined and reused.

```python
# A tiny, honest test harness: one line per check
def check(label, got, expected):
    status = "ok " if got == expected else "FAIL"
    print(f"{status} {label}: got {got!r}, expected {expected!r}")

check("sum of empty", sum([]), 0)
check("sum of three", sum([4, 1, 7]), 12)
```

---

## Common mistakes

- **Thinking `b = a` copies a list.** It does not. Use `.copy()`.
- **Using `[]` or `{}` as a default argument.** Use `None`.
- **Forgetting `global`** and wondering why the counter stays 0.
- **Slicing inside a loop or a recursion** and not realising each slice is a full copy.
- **Hitting `RecursionError` and raising the limit** instead of questioning the approach.

---

## Practice

1. 🟢 Predict the output, then run it: `x = [1, 2]; y = x; y = y + [3]; print(x)`. Why is `x` unchanged this time? *(Hint: `+` builds a new list.)*
2. 🟢 Write a function `swap_first_last(items)` that swaps in place and returns nothing. Then write a version that returns a new list and leaves the original alone.
3. 🟡 Decorate a function that returns the sum of a list recursively with `@trace` and read the indentation. What is the maximum depth for a list of 5 items?
4. 🟡 Without running it, say what this prints and why: `def f(n, seen=[]): seen.append(n); return seen` followed by `f(1)` and `f(2)`.
5. 🔴 Find out (by experiment) how deep a plain recursive function can go on your machine before `RecursionError`. Is it exactly `sys.getrecursionlimit()`? Why not?

<details>
<summary>Hints</summary>

1. `y = y + [3]` creates a new list and moves the `y` label to it. `x` still labels the old list.
2. In place: `items[0], items[-1] = items[-1], items[0]`. New list: copy first, then swap.
3. Maximum depth is 6 frames for 5 items: one per item plus the call on the empty list.
4. The default list is shared, so the second call prints `[1, 2]`.
5. Some frames are already in use before your function starts (the interpreter, the notebook, your own caller), so you get slightly fewer than the limit.
</details>
