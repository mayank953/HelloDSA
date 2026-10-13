# 15. Linked Lists

**Part 3: Data Structures** · Intermediate · about 8 minutes to read

> Nodes and pointers, insert and delete, reversing, the slow and fast pointer trick, cycle detection and merging, with the recursion view.
**In this repo:** [Linked list notes, notebooks and PDFs](../dsa-topics/linked-list/)  
**Run the code from this chapter:** [`code/15-linked-list.py`](code/15-linked-list.py)  

---

## The problem with arrays, and a different idea

In chapter 14 we saw that an array keeps its items in **one continuous block**. That gives instant access by index, but it makes **inserting or deleting in the middle expensive** (everyone shifts), and growing means copying.

What if the items did **not** have to sit next to each other?

### The scavenger hunt

Think of a treasure hunt. You are given a clue. That clue contains an item (*"you found 7"*) **and the location of the next clue**. You walk there, read the next clue, which holds another item and **another location**, and so on, until a clue says *"that's all"*.

Nothing forces the clues to be in neighbouring places. They can be scattered all over the city. What holds the chain together is the **address written on each clue**.

That is a **linked list**:

- Each item lives in a small box called a **node**.
- A node holds **the data** and a **pointer** (a reference) to the **next node**.
- The list itself is just a pointer to the **first node**, called the **head**.
- The last node points to nothing (`None`), which marks the end.

```text
 head
  |
  v
+------+---+    +------+---+    +------+---+    +------+------+
|  7   | *-+--> |  2   | *-+--> |  9   | *-+--> |  4   | None |
+------+---+    +------+---+    +------+---+    +------+------+
  node 1          node 2          node 3          node 4
```

```python
class Node:
    def __init__(self, data, next=None):
        self.data = data          # the value stored in this node
        self.next = next          # the next node (or None at the end)

# Build 7 -> 2 -> 9 by hand, from the back to the front.
third = Node(9)
second = Node(2, third)
head = Node(7, second)

print(head.data, head.next.data, head.next.next.data, head.next.next.next)
```

**Output**

```text
7 2 9 None
```

To get to the third item you **must walk**: head, then next, then next. There is no "go straight to item 3". That is the price, and we will measure it.

Let us add helpers that convert to and from Python lists, so we can see our lists easily:

```python
def from_list(items):
    head = None
    for value in reversed(items):          # build from the back so each new node points at the rest
        head = Node(value, head)
    return head

def to_list(head):
    items = []
    while head is not None:                # walk until we fall off the end
        items.append(head.data)
        head = head.next
    return items

def show(head):
    parts = []
    while head is not None:
        parts.append(str(head.data))
        head = head.next
    print(" -> ".join(parts + ["None"]))

show(from_list([7, 2, 9, 4]))
```

**Output**

```text
7 -> 2 -> 9 -> 4 -> None
```


---

## Walking the list: length and search

**Iteratively**, we hold a pointer `current` and keep moving it:

```python
def length(head):
    count, current = 0, head
    while current is not None:
        count += 1
        current = current.next
    return count

def get_at(head, index):
    """Walk `index` steps to find a value, and count the steps taken."""
    steps, current = 0, head
    while current is not None and steps < index:
        current = current.next
        steps += 1
    return (current.data if current else None), steps

big = from_list(list(range(1, 100_001)))
print("length:", length(big))
print("value at index 99,999 needed", get_at(big, 99_999)[1], "steps (an array needs 1)")
```

**Output**

```text
length: 100000
value at index 99,999 needed 99999 steps (an array needs 1)
```

So **reading by index is O(n)**, where an array gives O(1). Remember that cost; it is the main weakness.

### The recursive view: the rest of the list is a list

Here is the beautiful part. Look at the picture again: everything after the head, starting from `head.next`, is **itself a linked list**. The "smaller problem" is `head.next`. Linked lists and recursion fit together perfectly: no slicing, no copying, no index.

- **Base case.** `head is None`: the empty list.
- **Assume.** The recursive call handles `head.next` (the rest).
- **My part.** Do something with this node's data.

```python
def length_recursive(head):
    if head is None:                          # base case: the empty list has length 0
        return 0
    return 1 + length_recursive(head.next)    # my node, plus the length of the rest

def sum_recursive(head):
    if head is None:
        return 0
    return head.data + sum_recursive(head.next)

def print_reversed(head):
    if head is None:
        return
    print_reversed(head.next)                 # the rest FIRST (chapter 8: work after the call)
    print(head.data, end=" ")                 # then me, on the way back up

values = from_list([7, 2, 9, 4])
print(length_recursive(values), sum_recursive(values))
print_reversed(values)
print()
```

**Output**

```text
4 22
4 9 2 7 
```


All the head-versus-tail ideas from chapter 8 apply directly: printing *before* the call walks forward; printing *after* the call prints the list backwards, with no extra memory for reversing.

---

## Inserting and deleting: the pointer surgery

This is where linked lists shine. To insert a node **in the middle**, we only change **two pointers**. No shifting.

**Insert `5` after the node `2`** in `7 -> 2 -> 9`:

```text
Before:   7 --> 2 --> 9
                \
New node:        5

Step 1: make 5 point to what 2 points to (9):    5 --> 9
Step 2: make 2 point to 5:                        2 --> 5

After:    7 --> 2 --> 5 --> 9
```

**Order matters!** If you do step 2 first (`2.next = 5`), you lose the only pointer to `9`, and the rest of the list is gone forever. Always **connect the new node to the rest first**, then connect the front to the new node.

```python
def insert_at_head(head, value):
    return Node(value, head)                   # O(1): the new node points at the old head

def insert_at_tail(head, value):
    new_node = Node(value)
    if head is None:
        return new_node
    current = head
    while current.next is not None:            # walk to the last node: O(n)
        current = current.next
    current.next = new_node
    return head

def insert_at(head, index, value):
    if index == 0:
        return Node(value, head)
    current = head
    for _ in range(index - 1):                 # stop at the node just BEFORE the spot
        if current is None:
            raise IndexError("index out of range")
        current = current.next
    if current is None:
        raise IndexError("index out of range")
    current.next = Node(value, current.next)   # new node -> rest, THEN front -> new node (one line, safe)
    return head

lst = from_list([7, 2, 9])
lst = insert_at_head(lst, 1)
lst = insert_at_tail(lst, 4)
lst = insert_at(lst, 2, 5)
show(lst)
```

**Output**

```text
1 -> 7 -> 5 -> 2 -> 9 -> 4 -> None
```

Notice every function returns the **head**. The head can change (when we insert at the front), so the caller must use the returned value: `lst = insert_at_head(lst, 1)`.

### The recursive insert

With recursion, "go to the right spot" is just "ask the rest to insert at index − 1":

```python
def insert_recursive(head, index, value):
    if index == 0:                                         # this is the spot
        return Node(value, head)
    if head is None:
        raise IndexError("index out of range")
    head.next = insert_recursive(head.next, index - 1, value)   # assume: the rest handles it
    return head                                            # my node stays; reconnect to the updated rest

demo = from_list([7, 2, 9])
demo = insert_recursive(demo, 1, 5)
show(demo)
```

**Output**

```text
7 -> 5 -> 2 -> 9 -> None
```


### Deleting

To delete a node, make the **previous** node skip over it:

```text
Delete 2 from  7 --> 2 --> 9
Make 7 point to 9:    7 --------> 9      (the node 2 is unreachable, and Python frees it)
```

```python
def delete_at(head, index):
    if head is None:
        raise IndexError("index out of range")
    if index == 0:
        return head.next                       # the head is removed: the next node becomes the head
    current = head
    for _ in range(index - 1):
        current = current.next
        if current is None:
            raise IndexError("index out of range")
    if current.next is None:
        raise IndexError("index out of range")
    current.next = current.next.next           # skip over the doomed node
    return head

def delete_value(head, value):
    """Recursive: remove the first node holding `value`."""
    if head is None:
        return None
    if head.data == value:
        return head.next
    head.next = delete_value(head.next, value)
    return head

lst2 = from_list([7, 2, 9, 4])
lst2 = delete_at(lst2, 1)
lst2 = delete_value(lst2, 4)
show(lst2)
```

**Output**

```text
7 -> 9 -> None
```


---

## Arrays versus linked lists

| Operation | Array (Python list) | Singly linked list |
|---|---|---|
| Read by index | **O(1)** | O(n) |
| Insert / delete at the **front** | O(n) | **O(1)** |
| Insert / delete at the **end** | **O(1)** amortised | O(n) (O(1) if you also keep a `tail` pointer, and delete still needs the previous node) |
| Insert / delete in the middle, *once you are there* | O(n) (shifting) | **O(1)** (pointers) |
| Find a value | O(n) | O(n) |
| Memory | Compact | Extra pointer per node; scattered in memory |
| Growing | Occasional big copy | Never copies: just add a node |

**There is no winner.** If you read by index all the time, use an array. If you constantly insert and remove at one end, or splice pieces together, a linked structure shines. (In Python, `collections.deque` is the practical answer for queues.)

---

## Classic linked list problems

These are favourites in interviews, and every one is a pointer trick.

### 1. Reverse a linked list

**Idea.** Walk down the list and flip each arrow to point **backwards**. You need three pointers: `previous` (what is behind), `current` (where you are), and `following` (saved before you break the link, or you lose the rest).

```text
None <-- 1    2 --> 3 --> None       flip 1's arrow
         p    c
None <-- 1 <-- 2    3 --> None       flip 2's arrow
              p     c
None <-- 1 <-- 2 <-- 3               flip 3's arrow; previous is the new head
```

```python
def reverse(head):
    previous, current = None, head
    while current is not None:
        following = current.next        # save the rest BEFORE we break the link
        current.next = previous         # flip the arrow
        previous = current              # move both pointers forward
        current = following
    return previous                     # the old tail is the new head

show(reverse(from_list([1, 2, 3, 4])))
```

**Output**

```text
4 -> 3 -> 2 -> 1 -> None
```

The recursive version is a lovely use of the recipe: **assume the rest is already reversed**, then attach yourself at its end.

```python
def reverse_recursive(head):
    if head is None or head.next is None:         # base case: 0 or 1 nodes are already reversed
        return head
    new_head = reverse_recursive(head.next)       # assume: the rest, reversed. head.next is now its LAST node
    head.next.next = head                         # my part: make that last node point back at me
    head.next = None                              # I am now the tail
    return new_head

show(reverse_recursive(from_list([1, 2, 3, 4])))
```

**Output**

```text
4 -> 3 -> 2 -> 1 -> None
```


### 2. The middle of the list: the tortoise and the hare

**Question.** Find the middle node in **one pass**, without knowing the length.

**Idea.** Two runners start together. The **tortoise** moves one step at a time, the **hare** two steps. When the hare reaches the end, the tortoise has covered half the distance: **it is at the middle**.

```python
def middle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next                 # one step
        fast = fast.next.next            # two steps
    return slow

print(middle(from_list([1, 2, 3, 4, 5])).data, middle(from_list([1, 2, 3, 4])).data)
```

**Output**

```text
3 3
```

For an even number of nodes this gives the **second** of the two middles.

### 3. Detect a cycle (Floyd's algorithm)

Imagine the last node points **back** to an earlier one, so the list loops forever. Walking would never end.

Use the same two runners on a circular track: the fast one **must eventually lap** the slow one, so they meet. If there is no loop, the hare just reaches the end.

```python
def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:                  # they met: there must be a loop
            return True
    return False

looped = from_list([1, 2, 3, 4, 5])
tail = looped
while tail.next:
    tail = tail.next
tail.next = looped.next.next              # link the last node back to node "3"
print(has_cycle(looped), has_cycle(from_list([1, 2, 3])))
```

**Output**

```text
True False
```

**Cost.** **O(n)** time and **O(1)** space. (Storing every visited node in a set also works, but costs O(n) space.)


### 4. Merge two sorted lists

Exactly the merge step of merge sort (chapter 10), but with pointers and **no copying of values**: we simply re-link existing nodes. A **dummy head** node avoids special-casing the first node.

```python
def merge_sorted(a, b):
    dummy = Node(0)                       # a placeholder to hang the result on
    tail = dummy
    while a is not None and b is not None:
        if a.data <= b.data:
            tail.next, a = a, a.next      # take the smaller node
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a is not None else b # attach whatever is left
    return dummy.next

show(merge_sorted(from_list([1, 4, 6]), from_list([2, 3, 7, 9])))
```

**Output**

```text
1 -> 2 -> 3 -> 4 -> 6 -> 7 -> 9 -> None
```

The **dummy-head trick** (a throwaway first node so the real head is never a special case) is worth remembering: it makes many linked list programs simpler.

### 5. Remove the n-th node from the end

**Idea.** Use two pointers **n nodes apart**. Move both forward; when the front one reaches the end, the back one stands just before the node to delete. One pass, no length needed.

```python
def remove_nth_from_end(head, n):
    dummy = Node(0, head)
    front = back = dummy
    for _ in range(n + 1):                # get `front` n+1 steps ahead
        front = front.next
    while front is not None:              # move both until front falls off the end
        front = front.next
        back = back.next
    back.next = back.next.next            # `back` is just before the doomed node
    return dummy.next

show(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2))
```

**Output**

```text
1 -> 2 -> 3 -> 5 -> None
```


### 6. Is the list a palindrome?

Combine three tools: find the **middle** (tortoise and hare), **reverse** the second half, then **compare** the two halves.

```python
def is_palindrome_list(head):
    if head is None or head.next is None:
        return True
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow, fast = slow.next, fast.next.next
    second_half = reverse(slow.next)           # reverse everything after the middle
    first, second, answer = head, second_half, True
    while second is not None:
        if first.data != second.data:
            answer = False
            break
        first, second = first.next, second.next
    slow.next = reverse(second_half)           # put the list back the way we found it
    return answer

print(is_palindrome_list(from_list([1, 2, 3, 2, 1])), is_palindrome_list(from_list([1, 2, 3])))
```

**Output**

```text
True False
```


---

## Other kinds of linked lists

- **Doubly linked list.** Each node has `next` **and** `previous`. You can walk both ways and delete a node in O(1) if you already hold it. The cost: one more pointer per node and more careful updates. (This is what powers an LRU cache, chapter 28.)
- **Circular linked list.** The last node points back to the first. Handy for round-robin turns.
- **Tail pointer.** Keep a second pointer to the last node, and appending becomes O(1).
- **Sentinel / dummy node.** A fake head (and sometimes tail) that removes special cases, as in the merge example.

---

## Common mistakes

- **Losing the rest of the list** by overwriting a pointer before saving it (`current.next = previous` before saving `following`).
- **Not handling `None`:** the empty list, one node, deleting the head, inserting at the very end.
- **Forgetting to return the new head** after an operation that can change it.
- **Walking past the end:** `while current.next.next` without checking `current.next` first.
- **Accidentally creating a cycle**, then looping forever when printing.
- **Confusing the node with its data:** `current` is a node; `current.data` is the value.

---

## Practice

1. 🟢 Count how many times a value appears in a linked list (iteratively, then recursively).
2. 🟢 Return the last node's data without computing the length.
3. 🟡 Remove all nodes with a given value.
4. 🟡 Delete the middle node of a list.
5. 🟡 Find the node where two lists **merge** (they share a common tail).
6. 🟡 Find the node where a cycle **begins**. *(Hint: after the runners meet, restart one from the head and move both one step at a time.)*
7. 🔴 Reverse the list in groups of `k` nodes.
8. 🔴 Add two numbers stored as digit lists (least significant digit first).
9. 🔴 Sort a linked list in O(n log n) with merge sort. *(Use the middle finder and `merge_sorted`.)*

<details>
<summary>Hints</summary>

3. Use a dummy head so removing the first node is not a special case.
5. Let one pointer walk list A then list B, the other list B then list A: they meet at the junction after the same total distance.
7. Reverse `k` nodes, then recurse on the remainder and connect.
9. Split at the middle with slow/fast, sort each half recursively, then merge.
</details>

You have also met the repo's notebooks on this topic in [`dsa-topics/linked-list`](../dsa-topics/linked-list/).

---

[← 14. Arrays and Lists](14-arrays-and-lists.md) · [Handbook contents](README.md) · [16. Stacks →](16-stack.md)
