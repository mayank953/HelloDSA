# 20. Binary Search Trees

**Part 3: Data Structures** · Intermediate · about 8 minutes to read

> Search, insert and delete in a BST, validating one, finding the lowest common ancestor, and why balance matters.
**In this repo:** [BST notebook and notes](../dsa-topics/trees/)  
**Run the code from this chapter:** [`code/20-binary-search-trees.py`](code/20-binary-search-trees.py)  

---

## Putting order into a tree

A plain binary tree has no rules about *where* values go, so finding a value means checking every node: O(n). But suppose we add **one rule**:

> **Binary Search Tree (BST) rule.** For every node, **all** values in its **left** subtree are **smaller**, and **all** values in its **right** subtree are **larger**.

```text
              8
            /   \
           3     10
          / \      \
         1   6      14
            / \     /
           4   7   13
```

Now look at what that buys us. Looking for `7`? Start at the root `8`. `7 < 8`, so it can only be in the **left** subtree: the whole right side is ruled out. At `3`: `7 > 3`, go **right**. At `6`: `7 > 6`, go right. Found `7` after only **four** looks, never touching the other half of the tree.

It is **binary search from chapter 10, built into the shape of the data**. Each comparison discards a whole subtree, and when the tree is bushy the number of steps is about `log n`.

> **A common slip.** The rule is about *all* nodes in a subtree, not just the immediate children. A node `6` on the left side of `5`'s left child would be wrong even if it is bigger than its parent `3`, because it must also be smaller than `5`. We will use this in "validating a BST" below.

---

## The node and the three basic operations

```python
class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
```

### Search

At each node compare, then go left or right. This is binary search by walking down.

```python
def search(node, target):
    if node is None:                     # fell off the tree: not present
        return False
    if target == node.value:
        return True
    if target < node.value:
        return search(node.left, target)        # smaller: only the left can hold it
    return search(node.right, target)           # bigger: only the right can hold it
```

### Insert

Walk down exactly as if searching. When you fall off the tree (`None`), that is **the place where the value belongs**: put a new node there. The recursive version is a lovely use of the *assume* step: "insert into the child subtree, and reattach whatever comes back".

```python
def insert(node, value):
    if node is None:
        return BSTNode(value)                              # found the empty spot
    if value < node.value:
        node.left = insert(node.left, value)               # assume: the left subtree takes care of it
    elif value > node.value:
        node.right = insert(node.right, value)
    return node                                            # (equal values are ignored here)

root = None
for number in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    root = insert(root, number)

print(search(root, 7), search(root, 5))
```

**Output**

```text
True False
```

### Inorder gives sorted order

Chapter 19 hinted at this. Visit left, me, right: because everything on the left is smaller and everything on the right is larger, you get the values **in increasing order**.

```python
def inorder(node, out):
    if node:
        inorder(node.left, out)
        out.append(node.value)
        inorder(node.right, out)
    return out

print(inorder(root, []))
```

**Output**

```text
[1, 3, 4, 6, 7, 8, 10, 13, 14]
```

That is a sorting algorithm (insert everything, read in order, "tree sort"), and it is the reason BSTs are the foundation of ordered collections.

### Smallest and largest

The smallest value is the **leftmost** node, the largest is the **rightmost**.

```python
def minimum(node):
    while node.left is not None:
        node = node.left
    return node

def maximum(node):
    while node.right is not None:
        node = node.right
    return node

print(minimum(root).value, maximum(root).value)
```

**Output**

```text
1 14
```


---

## Deleting a node: three cases

Deletion is where BSTs get interesting, because removing a node must **not break the rule**. Look at how many children the doomed node has.

**Case 1: a leaf (no children).** Just remove it.

**Case 2: one child.** Remove it and let the child take its place (like skipping a node in a linked list).

**Case 3: two children.** We cannot simply delete it: two subtrees are hanging from it. Instead, **replace its value** with a value that keeps the rule intact, and delete *that* node instead. The right choice is the **inorder successor**: the smallest value in the **right** subtree. (It is bigger than everything on the left and smaller than everything else on the right.) That node has no left child, so deleting it falls into case 1 or 2.

```text
Delete 3 (two children):          1.  find the smallest in the right subtree: 4
          3                       2.  copy 4 into the node
        /   \                     3.  delete the original 4 from the right subtree
       1     6                            4
            / \                         /   \
           4   7                       1     6
                                              \
                                               7
```

```python
def delete(node, value):
    if node is None:
        return None
    if value < node.value:
        node.left = delete(node.left, value)
    elif value > node.value:
        node.right = delete(node.right, value)
    else:                                              # this is the node to remove
        if node.left is None:
            return node.right                          # cases 1 and 2: zero or one (right) child
        if node.right is None:
            return node.left                           # case 2: one (left) child
        successor = minimum(node.right)                # case 3: two children
        node.value = successor.value                   # take the successor's value...
        node.right = delete(node.right, successor.value)   # ...and delete the successor node
    return node

for doomed in [4, 3, 8]:                               # a leaf, a node with two children, the root
    root = delete(root, doomed)
    print(f"after deleting {doomed}: {inorder(root, [])}")
```

**Output**

```text
after deleting 4: [1, 3, 6, 7, 8, 10, 13, 14]
after deleting 3: [1, 6, 7, 8, 10, 13, 14]
after deleting 8: [1, 6, 7, 10, 13, 14]
```


After every deletion the inorder list is still sorted, which is the proof that the rule survived.

---

## Validating a BST (the classic trap)

**Question.** Given a binary tree, is it a valid BST?

The tempting solution: *"at every node, check that the left child is smaller and the right child is bigger."* **That is wrong**, and here is a counterexample:

```text
        5
       / \
      3   8
     / \
    1   6      <- 6 is bigger than its parent 3, but it is on the LEFT of 5, so it should be < 5
```

Every parent-child pair looks fine locally (`3 < 5`, `1 < 3`, `6 > 3`), yet `6` breaks the rule for `5`. The fix is to pass **bounds** down: each node must lie strictly between a `low` and a `high` that the ancestors above it set.

```python
def is_valid_bst(node, low=float("-inf"), high=float("inf")):
    if node is None:
        return True
    if not (low < node.value < high):                      # outside the allowed range: invalid
        return False
    return (is_valid_bst(node.left, low, node.value) and   # left side: must stay below me
            is_valid_bst(node.right, node.value, high))    # right side: must stay above me

def local_check_only(node):
    if node is None:
        return True
    if node.left and node.left.value >= node.value:
        return False
    if node.right and node.right.value <= node.value:
        return False
    return local_check_only(node.left) and local_check_only(node.right)

bad = BSTNode(5)
bad.left, bad.right = BSTNode(3), BSTNode(8)
bad.left.left, bad.left.right = BSTNode(1), BSTNode(6)     # the sneaky 6

print("naive local check says:", local_check_only(bad))
print("bounds check says     :", is_valid_bst(bad))
print("a real BST            :", is_valid_bst(root))
```

**Output**

```text
naive local check says: True
bounds check says     : False
a real BST            : True
```

An equivalent test: **do an inorder walk and check that the values are strictly increasing**.


---

## More BST problems

### A fresh sample tree

The tree we started with has lost some nodes to our deletions, so let us rebuild the original for the next examples:

```python
sample = None
for number in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    sample = insert(sample, number)
```

### k-th smallest

Inorder visits values in order, so the k-th value visited is the k-th smallest. Stop as soon as you reach it, using the iterative inorder from chapter 19:

```python
def kth_smallest(root, k):
    stack, current = [], root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        k -= 1
        if k == 0:
            return current.value
        current = current.right
    return None

print(kth_smallest(sample, 1), kth_smallest(sample, 3), kth_smallest(sample, 99))
```

**Output**

```text
1 4 None
```

### Lowest common ancestor in a BST

In a plain binary tree we searched both sides (chapter 19). With the ordering rule we can **walk down one path**: if both values are smaller than the node, go left; if both are larger, go right; otherwise *this* is where they split.

```python
def bst_lca(node, a, b):
    while node:
        if a < node.value and b < node.value:
            node = node.left
        elif a > node.value and b > node.value:
            node = node.right
        else:
            return node.value
    return None

print(bst_lca(sample, 1, 7), bst_lca(sample, 6, 7), bst_lca(sample, 10, 14))
```

**Output**

```text
3 6 10
```

### Sorted array to a balanced BST

If you insert sorted values one by one, you get a skewed tree (next section). But if you already have a sorted list, you can build a **balanced** tree directly: the **middle** value is the root, and recursion builds the left half and right half. (Divide and conquer, chapter 10.)

```python
def sorted_to_bst(values, low=0, high=None):
    if high is None:
        high = len(values) - 1
    if low > high:
        return None
    mid = (low + high) // 2
    node = BSTNode(values[mid])
    node.left = sorted_to_bst(values, low, mid - 1)
    node.right = sorted_to_bst(values, mid + 1, high)
    return node

def tree_height(node):
    if node is None:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))

balanced = sorted_to_bst(list(range(1, 1024)))
print("1023 values, height", tree_height(balanced))
```

**Output**

```text
1023 values, height 10
```


---

## Why balance matters

Every operation walks one root-to-leaf path, so its cost is the tree's **height**. A *bushy* tree has height about `log₂ n`. But insert values in **sorted order** and every new value goes to the right of the previous one: the tree becomes a **stick**, a linked list in disguise, and every operation is O(n).

Let us measure, with 500 keys inserted in two different orders. (We use an iterative insert so the experiment itself does not hit the recursion limit.)

```python
def insert_iterative(root, value):
    if root is None:
        return BSTNode(value)
    node = root
    while True:
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value); break
            node = node.left
        elif value > node.value:
            if node.right is None:
                node.right = BSTNode(value); break
            node = node.right
        else:
            break
    return root

def height_iterative(root):
    if root is None:
        return 0
    levels, queue = 0, deque([root])
    while queue:
        levels += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
    return levels

from collections import deque
n = 500
sorted_keys = list(range(n))
scrambled_keys = [(i * 7919) % n for i in range(n)]       # the same keys, in a scattered order

for label, keys in [("sorted order   ", sorted_keys), ("scrambled order", scrambled_keys)]:
    tree = None
    for key in keys:
        tree = insert_iterative(tree, key)
    print(f"{label}: height {height_iterative(tree):>3}   (a perfectly balanced tree of {n} would be {n.bit_length()})")
```

**Output**

```text
sorted order   : height 500   (a perfectly balanced tree of 500 would be 9)
scrambled order: height  18   (a perfectly balanced tree of 500 would be 9)
```

The same 500 keys give a tree 500 levels tall or only about twenty, depending on insertion order. A real system cannot rely on luck. The answer: **self-balancing trees**.


---

## Self-balancing trees: AVL in one page

An **AVL tree** (named after its inventors) is a BST that **repairs itself** after every insert so that, at every node, the heights of the two subtrees differ by **at most 1**. The repair is a **rotation**: a local rearrangement of three nodes that keeps the BST rule intact but moves weight from the heavy side to the light side.

```text
Right rotation around y  (the left side is too tall):

        y                         x
       / \                       / \
      x   C        ----->       A   y
     / \                           / \
    A   B                         B   C

The BST rule survives: A < x < B < y < C in both pictures. Only the shape changed.
```

```python
class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = self.right = None
        self.height = 1

def h(node):
    return node.height if node else 0

def update(node):
    node.height = 1 + max(h(node.left), h(node.right))

def rotate_right(y):
    x = y.left
    y.left, x.right = x.right, y        # B moves across, y drops below x
    update(y); update(x)
    return x                            # x is the new root of this subtree

def rotate_left(x):
    y = x.right
    x.right, y.left = y.left, x
    update(x); update(y)
    return y

def avl_insert(node, value):
    if node is None:
        return AVLNode(value)
    if value < node.value:
        node.left = avl_insert(node.left, value)
    elif value > node.value:
        node.right = avl_insert(node.right, value)
    else:
        return node
    update(node)
    balance = h(node.left) - h(node.right)          # positive: leaning left, negative: leaning right
    if balance > 1:                                 # too heavy on the left
        if value > node.left.value:                 # the "zig-zag" case: straighten it first
            node.left = rotate_left(node.left)
        return rotate_right(node)
    if balance < -1:                                # too heavy on the right
        if value < node.right.value:
            node.right = rotate_right(node.right)
        return rotate_left(node)
    return node

avl = None
for key in range(1, 1001):                          # sorted order: the worst case for a plain BST
    avl = avl_insert(avl, key)

print("1000 sorted inserts, AVL height:", avl.height, "(a plain BST would be 1000 tall)")
```

**Output**

```text
1000 sorted inserts, AVL height: 10 (a plain BST would be 1000 tall)
```

Insert the sorted keys 1 to 1000 (the *worst* input for an ordinary BST) and the AVL tree stays only about ten levels tall. The rotations did that. Every operation stays **O(log n)** in the worst case.


Real-world self-balancing trees:

- **AVL** and **Red-Black** trees: in-memory ordered maps and sets (C++ `std::map`, Java `TreeMap`).
- **B-trees**: a wide, shallow variation used by databases and file systems to minimise disk reads.

You will rarely write these yourself, but you should know **why** they exist and what they guarantee.

---

## BST versus the alternatives

| Need | Sorted array | Hash map | BST (balanced) |
|---|---|---|---|
| Lookup | O(log n) (binary search) | **O(1)** average | O(log n) |
| Insert / delete | O(n) (shifting) | **O(1)** average | O(log n) |
| Items **in sorted order** | **O(n)** (already sorted) | O(n log n) (must sort) | **O(n)** (inorder walk) |
| Smallest / largest | O(1) | O(n) | O(log n) |
| "Next bigger value" / **range queries** | O(log n) | O(n) | **O(log n)** |

A hash map wins when you only need lookups. A balanced BST wins when you need **order**: ranges, predecessors, "all keys between a and b".

---

## Common mistakes

- **Checking only parent and child** when validating a BST. Pass bounds down.
- **Forgetting that the BST rule covers whole subtrees**, not just immediate children.
- **Not handling duplicates** on purpose. Decide (ignore, count, or go consistently to one side) and document it.
- **Deleting a node with two children** without choosing the inorder successor (or predecessor).
- **Assuming a BST is balanced.** Sorted insertions create a stick.
- **Recursion depth on a skewed tree.** A tree of 5,000 sorted inserts will overflow Python's stack: use iteration or a self-balancing tree.

---

## Practice

1. 🟢 Find the **floor** (largest value ≤ x) and **ceiling** (smallest value ≥ x) of a number in a BST.
2. 🟢 Count the nodes whose value lies in a range `[low, high]` without visiting subtrees that cannot qualify (pruning, chapter 13).
3. 🟡 Insert and delete using an **iterative** approach.
4. 🟡 Convert a BST so that every node holds the **sum of all values greater than or equal to it**.
5. 🟡 Find the **in-order successor** of a given node.
6. 🟡 Check whether two BSTs contain the **same set of values** (they may have different shapes).
7. 🔴 Recover a BST in which **two nodes were swapped** by mistake.
8. 🔴 Implement the rotations for the **left-right** and **right-left** cases separately and trace one by hand.

<details>
<summary>Hints</summary>

1. Walk down: when you go right, the current node is a floor candidate; when you go left, it is a ceiling candidate.
2. If a node is below `low`, ignore its left subtree; if it is above `high`, ignore its right subtree.
4. A reverse inorder walk (right, me, left) while keeping a running total.
6. Compare the two inorder lists.
7. In an inorder list the two swapped values show up as the places where the order goes wrong.
</details>

---

[← 19. Trees and Binary Trees](19-trees.md) · [Handbook contents](README.md) · [21. Heaps and Priority Queues →](21-heaps.md)
