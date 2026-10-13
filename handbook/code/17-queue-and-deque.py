"""17. Queues and Deques

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 17-queue-and-deque.py
"""

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

from collections import deque

line = deque()
line.append("Asha")            # enqueue at the back
line.append("Ravi")
line.append("Meera")
print(line.popleft())          # dequeue from the front: O(1)
print(line)

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

def hot_potato(names, k):
    circle = deque(names)
    while len(circle) > 1:
        for _ in range(k - 1):
            circle.append(circle.popleft())     # pass the potato: move the front child to the back
        circle.popleft()                        # the k-th holder is out
    return circle[0]

print(hot_potato(["Asha", "Ravi", "Meera", "Karan", "Zoya", "Imran", "Priya"], 3))

print('\n[all code in this chapter ran successfully]')
