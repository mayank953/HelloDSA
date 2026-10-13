# 17. Queues and Deques

**Part 3: Data Structures** · Intermediate · about 6 minutes to read

> First in, first out: circular queues, deques, a queue from two stacks, and the sliding window maximum.
**In this repo:** [Queue notebook and notes](../dsa-topics/queue/)  
**Run the code from this chapter:** [`code/17-queue-and-deque.py`](code/17-queue-and-deque.py)  

---

## The line at the ticket counter

Stand in a queue at a cinema. The person who arrived **first** is served **first**. Newcomers join at the **back**; people leave from the **front**. Nobody is allowed to push in.

That rule is **FIFO**, *First In, First Out*, the mirror image of the stack's LIFO. A data structure that follows it is a **queue**. You meet queues everywhere: a print queue, customers waiting for support, tasks waiting for a worker, requests waiting for a server, and the search strategy called **BFS** (below).

> A queue's operations: **enqueue** (join at the back) · **dequeue** (leave from the front) · **front/peek** · **is_empty**. All should be **O(1)**.

---

## The obvious way is slow

A Python list is a natural candidate: `append` to enqueue, `pop(0)` to dequeue. It works, but remember chapter 14: removing from the **front** of an array makes *every other item shift one place left*. Let us count that shifting for a queue of 2,000 items that we then empty:

```python
class NaiveQueue:
    """An array queue that dequeues from index 0 and counts the shifts it performs."""
    def __init__(self):
        self.items = []
        self.shifts = 0

    def enqueue(self, value):
        self.items.append(value)

    def dequeue(self):
        value = self.items[0]
        for i in range(1, len(self.items)):      # everyone moves one place forward
            self.items[i - 1] = self.items[i]
            self.shifts += 1
        self.items.pop()
        return value

q = NaiveQueue()
for i in range(2000):
    q.enqueue(i)
while q.items:
    q.dequeue()
print(f"emptying a 2,000-item queue needed {q.shifts:,} shifts (n(n-1)/2 = {2000 * 1999 // 2:,})")
```

**Output**

```text
emptying a 2,000-item queue needed 1,999,000 shifts (n(n-1)/2 = 1,999,000)
```

Emptying the queue is **O(n²)**. That is a bug waiting for a busy day. We need dequeue to be O(1). Three standard ways follow.


---

## Way 1: a linked list with a head and a tail

Keep **two pointers**: `head` (the front, where we dequeue) and `tail` (the back, where we enqueue). Both operations touch only one end, so both are O(1). No shifting, ever.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedQueue:
    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def enqueue(self, value):
        node = Node(value)
        if self.tail is None:                 # the queue was empty
            self.head = self.tail = node
        else:
            self.tail.next = node             # hook the new node behind the current last one
            self.tail = node
        self.size += 1

    def dequeue(self):
        if self.head is None:
            raise IndexError("dequeue from an empty queue")
        value = self.head.data
        self.head = self.head.next
        if self.head is None:                 # we removed the last node
            self.tail = None
        self.size -= 1
        return value

queue = LinkedQueue()
for name in ["Asha", "Ravi", "Meera"]:
    queue.enqueue(name)
print(queue.dequeue(), queue.dequeue(), queue.size)
```

**Output**

```text
Asha Ravi 1
```


---

## Way 2: a circular array

A fixed-size array can work as a queue if we let the queue **wrap around**. We track the index of the `front` and the current `size`. The slot where the next item goes is `(front + size) % capacity`; the `%` makes the index wrap back to 0 after the last slot, as if the array were a ring.

```text
capacity 5, after enqueue A,B,C,D,E, dequeue, dequeue, enqueue F:

 index:   0    1    2    3    4
        +----+----+----+----+----+
        | F  |    | C  | D  | E  |        front = 2, size = 4
        +----+----+----+----+----+
                    ^ front              F went into index 0: it wrapped around!
```

```python
class CircularQueue:
    def __init__(self, capacity):
        self.slots = [None] * capacity
        self.front = 0
        self.size = 0

    def enqueue(self, value):
        if self.size == len(self.slots):
            raise OverflowError("queue is full")
        rear = (self.front + self.size) % len(self.slots)       # wrap around the end
        self.slots[rear] = value
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            raise IndexError("dequeue from an empty queue")
        value = self.slots[self.front]
        self.slots[self.front] = None
        self.front = (self.front + 1) % len(self.slots)         # move the front, wrapping if needed
        self.size -= 1
        return value

ring = CircularQueue(5)
for letter in "ABCDE":
    ring.enqueue(letter)
print(ring.dequeue(), ring.dequeue())
ring.enqueue("F")
print(ring.slots, "front =", ring.front)
```

**Output**

```text
A B
['F', None, 'C', 'D', 'E'] front = 2
```


Every operation is O(1), and memory is fixed, which is why circular buffers are used in hardware and streaming systems.

---

## Way 3 (the practical one): `collections.deque`

Python ships a ready-made, optimised structure: **`deque`** (say "deck"), a *double-ended queue* with O(1) `append`, `appendleft`, `pop` and `popleft`. For queues in Python, just use it.

```python
from collections import deque

line = deque()
line.append("Asha")            # enqueue at the back
line.append("Ravi")
line.append("Meera")
print(line.popleft())          # dequeue from the front: O(1)
print(line)
```

**Output**

```text
Asha
deque(['Ravi', 'Meera'])
```

A deque can act as a queue (add right, remove left), as a stack (add and remove on the same side), or both ends at once. That flexibility is the "double ended" part.

**Don't** build a queue on `list.pop(0)`. Use `deque.popleft()`.

---

## A queue from two stacks

A favourite interview puzzle: *build a queue using only stacks.* It teaches a neat idea.

Imagine two piles of plates, an **inbox** and an **outbox**.

- **Enqueue:** push onto the inbox.
- **Dequeue:** if the outbox has plates, pop one. If it is **empty**, first **pour the whole inbox into the outbox**, one plate at a time. Pouring **reverses the order**, so the *oldest* plate ends up on top, exactly where a queue wants it.

```python
class QueueFromStacks:
    def __init__(self):
        self.inbox, self.outbox = [], []
        self.moves = 0                               # how many items we poured between stacks

    def enqueue(self, value):
        self.inbox.append(value)

    def dequeue(self):
        if not self.outbox:
            while self.inbox:                        # pour: the order gets reversed
                self.outbox.append(self.inbox.pop())
                self.moves += 1
        return self.outbox.pop()

qs = QueueFromStacks()
for i in range(1, 6):
    qs.enqueue(i)
print([qs.dequeue() for _ in range(5)])

big = QueueFromStacks()
for i in range(10_000):
    big.enqueue(i)
for _ in range(10_000):
    big.dequeue()
print(f"10,000 enqueues and 10,000 dequeues moved {big.moves:,} items in total")
```

**Output**

```text
[1, 2, 3, 4, 5]
10,000 enqueues and 10,000 dequeues moved 10,000 items in total
```

One dequeue may pour many items (slow), but **each item is poured at most once in its whole life**. So over `n` operations the total pouring is at most `n`: **amortised O(1)** per operation. It is the same accounting as the monotonic stack and the growing array.


---

## Breadth-first search: a queue's finest hour

Here is why queues matter so much. Suppose you want the **shortest path** through a maze where every step costs the same. Explore like ripples in a pond: first everything **1 step** away, then everything **2 steps** away, then 3, and so on. The first time you reach the goal, you got there by the fewest steps.

A queue gives exactly this order: nodes discovered **first** are explored **first**.

```python
def shortest_path(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, 0)])                 # (cell, steps taken to reach it)
    seen = {start}                              # never queue a cell twice
    while queue:
        (r, c), steps = queue.popleft()
        if (r, c) == goal:
            return steps
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "." and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append(((nr, nc), steps + 1))
    return -1                                   # the goal is unreachable

maze = ["...#",
        "##.#",
        "....",
        ".##."]
print(shortest_path(maze, (0, 0), (3, 3)))
print(shortest_path(["..#.", "##.."], (0, 0), (1, 3)))
```

**Output**

```text
6
-1
```


If you swapped the queue for a **stack** the same code would explore deep first (depth-first search). Queue versus stack is the *only* difference between BFS and DFS. We use this in the graphs chapter (22).

---

## The deque as a monotonic queue: sliding window maximum

**Question.** For every window of `k` consecutive numbers, report the **maximum**. For `[1, 3, -1, -3, 5, 3, 6, 7]` and `k = 3` the answers are `[3, 3, 5, 5, 6, 7]`.

*Slow way:* take `max` of each window: `n × k` work.

**Idea.** Keep a deque of **indices** whose values are in **decreasing** order. The **front** is always the maximum of the current window. For each new number: pop smaller items off the **back** (they can never be a maximum again, because the new number is bigger *and* will stay in the window longer), push the new index, and drop the front if it has slid out of the window.

```python
def sliding_window_max(numbers, k):
    window = deque()                              # indices; their values decrease from front to back
    result = []
    for i, value in enumerate(numbers):
        while window and numbers[window[-1]] <= value:
            window.pop()                          # these can never be the maximum again
        window.append(i)
        if window[0] <= i - k:                    # the front slid out of the window
            window.popleft()
        if i >= k - 1:
            result.append(numbers[window[0]])     # the front is the maximum
    return result

print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
```

**Output**

```text
[3, 3, 5, 5, 6, 7]
```

Each index enters the deque once and leaves at most once: **O(n)** overall, however big `k` is.


---

## Round-robin with a queue: the hot-potato game

Children sit in a circle. They pass a potato `k` times; whoever holds it then is **out**. Repeat until one child remains. A queue models the circle: *dequeue from the front and enqueue at the back* to pass the potato along.

```python
def hot_potato(names, k):
    circle = deque(names)
    while len(circle) > 1:
        for _ in range(k - 1):
            circle.append(circle.popleft())     # pass the potato: move the front child to the back
        circle.popleft()                        # the k-th holder is out
    return circle[0]

print(hot_potato(["Asha", "Ravi", "Meera", "Karan", "Zoya", "Imran", "Priya"], 3))
```

**Output**

```text
Karan
```

(This is the famous **Josephus problem**.)


---

## Stack versus queue at a glance

| | **Stack** | **Queue** |
|---|---|---|
| Rule | LIFO: last in, first out | FIFO: first in, first out |
| Real life | Plates, undo, back button | Ticket line, print jobs |
| Operations | push, pop (same end) | enqueue (back), dequeue (front) |
| Natural fit | **Recursion**, nesting, backtracking, **DFS** | Fairness, scheduling, **BFS** |
| In Python | `list` with `append`/`pop()` | `collections.deque` with `append`/`popleft()` |

---

## Common mistakes

- **Using `list.pop(0)`** as a dequeue: O(n) each time.
- **Forgetting the tail** when the last node is removed (`tail` must become `None`).
- **Off-by-one in circular queues:** the rear is `(front + size) % capacity`, not `front + size`.
- **Confusing the two ends of a deque** (`append`/`pop` use the right, `appendleft`/`popleft` the left).
- **Marking nodes as visited too late in BFS**, so the same cell is queued many times. Mark when you *enqueue*, not when you dequeue.
- **Forgetting that the queue can be empty**: check before `dequeue`.

---

## Practice

1. 🟢 Implement a queue with `deque` and a method `peek_back()`.
2. 🟢 *Number of recent requests:* keep a queue of timestamps and report how many fall in the last 3,000 milliseconds.
3. 🟡 Reverse the first `k` elements of a queue (use a stack).
4. 🟡 Generate the first `n` binary numbers (`1, 10, 11, 100, ...`) using a queue.
5. 🟡 Implement a **stack using two queues**.
6. 🟡 Level-order traversal of a tree (you will meet it in chapter 19).
7. 🔴 *Rotting oranges:* a grid where rotten oranges rot their neighbours every minute. How many minutes until none are fresh? *(Multi-source BFS.)*
8. 🔴 *Design a circular deque* with a fixed capacity.

<details>
<summary>Hints</summary>

2. Each new request goes at the back; pop from the front while the front is older than 3,000 ms; the answer is the queue's length.
4. Start with `"1"`. Each time you dequeue `s`, output it and enqueue `s + "0"` and `s + "1"`.
7. Start the BFS from *all* rotten oranges at once, with time 0, and track the level you reach.
</details>

---

[← 16. Stacks](16-stack.md) · [Handbook contents](README.md) · [18. Hashmaps →](18-hashmaps.md)
