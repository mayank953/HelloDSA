## Data that branches

Arrays, linked lists, stacks and queues are all **linear**: items lined up one after another. But a lot of real data is **hierarchical**:

- A **family tree**: grandparents, parents, children.
- A company's **org chart**: CEO, managers, employees.
- The **folders** on your laptop: a folder contains files and more folders.
- A web page's **HTML**: elements inside elements.
- Every `if/else` decision flow, every chess game's possible moves.

The structure that captures this is the **tree**.

```text
                 Company
               /    |    \
           Sales   Tech   HR
           /  \      |
       North  South  Backend
```

In this chapter we will see that trees and recursion are made for each other: **a tree is a recursive structure** (each child is itself a smaller tree), so the recursion recipe from chapter 6 gives us almost every algorithm for free.

---

## Tree vocabulary (learn it once, use it forever)

```text
            A                 <- root (the top node; it has no parent)
          /   \
         B     C              <- B and C are children of A; they are siblings
        / \     \
       D   E     F            <- D, E, F are leaves (nodes with no children)
```

| Word | Meaning | In the picture |
|---|---|---|
| **Node** | One item in the tree | A, B, C, D, E, F |
| **Edge** | A link from parent to child | A-B, A-C, B-D, ... |
| **Root** | The top node (exactly one) | A |
| **Parent / child** | A node and the nodes directly below it | A is the parent of B and C |
| **Siblings** | Children of the same parent | B and C |
| **Leaf** | A node with no children | D, E, F |
| **Subtree** | A node together with everything below it | B with D and E |
| **Depth (level)** of a node | Edges from the root down to it | depth of D is 2 |
| **Height** of the tree | The longest path from the root down to a leaf | 3 nodes tall (2 edges) |
| **Binary tree** | Every node has **at most two** children: *left* and *right* | the tree above |

Two facts that never change:

- A tree with `n` nodes has exactly **`n − 1` edges**.
- A tree has **no cycles**: there is exactly one path between any two nodes.

---

## Building a binary tree

A node holds a value and two pointers: **left** and **right**. (Compare with the linked-list node, which had one `next`.)

```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

#            1
#          /   \
#         2     3
#        / \     \
#       4   5     6
root = TreeNode(1,
                TreeNode(2, TreeNode(4), TreeNode(5)),
                TreeNode(3, None, TreeNode(6)))

print(root.value, root.left.value, root.right.value, root.left.right.value)
```

Typing nested constructors gets tedious. A helper that builds a tree from a **level-by-level list** (with `None` for a missing child) lets us write trees compactly:

```python
from collections import deque

def build(values):
    """build([1, 2, 3, 4, 5, None, 6]) makes the tree above."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root

def draw(node, indent=0):
    """Print the tree sideways: the root is on the left, the right subtree on top."""
    if node is None:
        return
    draw(node.right, indent + 4)
    print(" " * indent + str(node.value))
    draw(node.left, indent + 4)

tree = build([1, 2, 3, 4, 5, None, 6])
draw(tree)
```

Tilt your head left: `1` is the root, `3` and `2` are its children, `6` sits above `3`... The `draw` function is itself a nice little recursion: draw the right subtree, print me, draw the left subtree.

---

## Thinking recursively about trees

Here is the sentence to memorise:

> **A tree is either empty, or it is a root with a left tree and a right tree.**

That *is* the recursion recipe:

1. **Base case.** The empty tree (`None`).
2. **Assume.** The recursive calls work correctly on the left subtree and on the right subtree. (Trust them, as always.)
3. **My part.** Combine the two answers with this node.

Let us apply it to four tiny questions. Notice that every function has **the same skeleton**, and only "my part" changes.

```python
def count_nodes(node):
    if node is None:                                       # base case
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)   # me + left + right

def sum_values(node):
    if node is None:
        return 0
    return node.value + sum_values(node.left) + sum_values(node.right)

def count_leaves(node):
    if node is None:
        return 0
    if node.left is None and node.right is None:          # I am a leaf
        return 1
    return count_leaves(node.left) + count_leaves(node.right)

def height(node):                                          # number of nodes on the longest root-to-leaf path
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))

print(count_nodes(tree), sum_values(tree), count_leaves(tree), height(tree))
```

```python hide
assert (count_nodes(tree), sum_values(tree), count_leaves(tree), height(tree)) == (6, 21, 3, 3)
assert count_nodes(None) == 0 and height(None) == 0 and height(TreeNode(1)) == 1
```

For **height**: my height is one more than the *taller* of my two subtrees' heights. Do not trace the whole tree in your head; trust the recipe, and check with a small example.

---

## The traversals: visiting every node

A **traversal** visits each node exactly once. There is more than one sensible order, and chapter 8 already told you where the difference comes from. For a node, we make three moves in some order: **visit the node itself**, **go into the left subtree**, **go into the right subtree**. The only question is **when** we do the visiting, relative to the two recursive calls:

| Name | Order | Where "visit me" sits |
|---|---|---|
| **Preorder** | **me**, left, right | *before* both calls |
| **Inorder** | left, **me**, right | *between* the calls |
| **Postorder** | left, right, **me** | *after* both calls |

```python
def preorder(node, visit):
    if node is None:
        return
    visit(node.value)                 # me first
    preorder(node.left, visit)
    preorder(node.right, visit)

def inorder(node, visit):
    if node is None:
        return
    inorder(node.left, visit)
    visit(node.value)                 # me in the middle
    inorder(node.right, visit)

def postorder(node, visit):
    if node is None:
        return
    postorder(node.left, visit)
    postorder(node.right, visit)
    visit(node.value)                 # me last

for name, walk in [("preorder ", preorder), ("inorder  ", inorder), ("postorder", postorder)]:
    seen = []
    walk(tree, seen.append)
    print(name, seen)
```

Same tree, three different orders, produced by **moving one line**. These three are called **depth-first** traversals, because they go deep before going wide.

```python hide
def collect(walk, t):
    seen = []; walk(t, seen.append); return seen
assert collect(preorder, tree) == [1, 2, 4, 5, 3, 6]
assert collect(inorder, tree) == [4, 2, 5, 1, 3, 6]
assert collect(postorder, tree) == [4, 5, 2, 6, 3, 1]
```

**When is each useful?**

- **Preorder:** copy a tree; print a folder structure (parent before contents).
- **Inorder:** for a *binary search tree* it visits values **in sorted order** (next chapter).
- **Postorder:** delete a tree or compute folder sizes (you need the children's answers *before* your own).

### Level order: visiting row by row

The fourth traversal goes **wide** instead of deep: all nodes at depth 0, then depth 1, then depth 2. As in chapter 17, a **queue** does this naturally.

```python
def level_order(root):
    levels = []
    queue = deque([root] if root else [])
    while queue:
        level = []
        for _ in range(len(queue)):               # exactly the nodes that are on the current level
            node = queue.popleft()
            level.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels

print(level_order(tree))
```

```python hide
assert level_order(tree) == [[1], [2, 3], [4, 5, 6]] and level_order(None) == []
```

Taking a snapshot of `len(queue)` at the start of each round is the standard trick to separate levels.

### Inorder without recursion

The call stack is a stack (chapter 16), so we can do the same traversal with our own:

```python
def inorder_iterative(root):
    result, stack, current = [], [], root
    while current or stack:
        while current:                    # go as far left as possible, remembering the way back
            stack.append(current)
            current = current.left
        current = stack.pop()             # nothing more on the left: visit this node
        result.append(current.value)
        current = current.right           # then do the right subtree
    return result

print(inorder_iterative(tree))
```

```python hide
assert inorder_iterative(tree) == collect(inorder, tree) and inorder_iterative(None) == []
```

---

## Problems on binary trees

Every one of these is the recipe with a different "my part".

### Is the tree symmetric? (mirror image)

Two trees are mirrors if their roots match, the left of one mirrors the right of the other, *and* the right of one mirrors the left of the other.

```python
def is_mirror(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.value == b.value and is_mirror(a.left, b.right) and is_mirror(a.right, b.left)

def is_symmetric(root):
    return root is None or is_mirror(root.left, root.right)

print(is_symmetric(build([1, 2, 2, 3, 4, 4, 3])), is_symmetric(build([1, 2, 2, None, 3, None, 3])))
```

### Invert (flip) the tree

My part: swap my two children, after inverting each of them.

```python
def invert(node):
    if node is None:
        return None
    node.left, node.right = invert(node.right), invert(node.left)
    return node

flipped = invert(build([1, 2, 3, 4, 5, None, 6]))
backwards = []
inorder(flipped, backwards.append)
print(backwards)                        # an inverted tree reads backwards in order
```

```python hide
assert is_symmetric(build([1, 2, 2, 3, 4, 4, 3])) and not is_symmetric(build([1, 2, 2, None, 3, None, 3]))
assert collect(inorder, flipped) == [6, 3, 1, 5, 2, 4]
```

### Does a root-to-leaf path add up to a target?

My part: subtract my value from the target and ask whether *either* child can finish the job.

```python
def has_path_sum(node, target):
    if node is None:
        return False
    remaining = target - node.value
    if node.left is None and node.right is None:     # a leaf: the path ends here
        return remaining == 0
    return has_path_sum(node.left, remaining) or has_path_sum(node.right, remaining)

fresh = build([1, 2, 3, 4, 5, None, 6])
print(has_path_sum(fresh, 7), has_path_sum(fresh, 10), has_path_sum(fresh, 5))
```

### All root-to-leaf paths (backtracking meets trees)

```python
def all_paths(root):
    paths, path = [], []

    def explore(node):
        if node is None:
            return
        path.append(str(node.value))                 # CHOOSE
        if node.left is None and node.right is None:
            paths.append("->".join(path))            # a complete path
        else:
            explore(node.left)                       # EXPLORE
            explore(node.right)
        path.pop()                                   # UN-CHOOSE

    explore(root)
    return paths

print(all_paths(fresh))
```

```python hide
assert has_path_sum(fresh, 7) and has_path_sum(fresh, 10) and not has_path_sum(fresh, 5)
assert all_paths(fresh) == ["1->2->4", "1->2->5", "1->3->6"]
```

### Is it balanced? (and the "return two things" trick)

A tree is **height-balanced** if at *every* node the heights of the left and right subtrees differ by at most 1. Checking `height` at every node would cost O(n²). The elegant fix: let the recursion return the **height**, and use `-1` to signal "unbalanced somewhere below".

```python
def check_balanced(node):
    """Return the height, or -1 if the tree below is unbalanced."""
    if node is None:
        return 0
    left = check_balanced(node.left)
    if left == -1:
        return -1                                    # pass the bad news up
    right = check_balanced(node.right)
    if right == -1 or abs(left - right) > 1:
        return -1
    return 1 + max(left, right)

def is_balanced(root):
    return check_balanced(root) != -1

chain = build([1, 2, None, 3])                        # a lopsided "stick" going down the left
print(is_balanced(fresh), is_balanced(chain))
```

### The diameter

The **diameter** is the longest path (counted in edges) between *any* two nodes. The best path through a node goes down the left side and down the right side, so at each node the candidate is `left height + right height`. We update a running best while computing heights, **one pass, O(n)**.

```python
def diameter(root):
    best = 0

    def depth(node):
        nonlocal best
        if node is None:
            return 0
        left, right = depth(node.left), depth(node.right)
        best = max(best, left + right)               # the longest path that bends at this node
        return 1 + max(left, right)

    depth(root)
    return best

print(diameter(fresh))
```

```python hide
assert is_balanced(fresh) and not is_balanced(chain) and is_balanced(None)
assert diameter(fresh) == 4 and diameter(None) == 0 and diameter(TreeNode(1)) == 0
```

### The lowest common ancestor

The **lowest common ancestor (LCA)** of two nodes is the deepest node that has both as descendants.

**Recipe.** If I am one of the two, I am the answer (ancestors are allowed to be the node itself). Otherwise ask both subtrees. If **both** report finding something, then the two nodes are on different sides, so **I** am the split point. If only one side finds something, pass that answer up.

```python
def lowest_common_ancestor(node, p, q):
    if node is None or node.value in (p, q):
        return node
    left = lowest_common_ancestor(node.left, p, q)
    right = lowest_common_ancestor(node.right, p, q)
    if left and right:                               # one on each side: this is the split
        return node
    return left or right

print(lowest_common_ancestor(fresh, 4, 5).value, lowest_common_ancestor(fresh, 4, 6).value, lowest_common_ancestor(fresh, 2, 4).value)
```

```python hide
assert lowest_common_ancestor(fresh, 4, 5).value == 2 and lowest_common_ancestor(fresh, 4, 6).value == 1
assert lowest_common_ancestor(fresh, 2, 4).value == 2
```

---

## How big can a tree get?

A binary tree of height `h` (counted in levels) holds at most `1 + 2 + 4 + ... + 2^(h−1) = 2^h − 1` nodes. Turn that around: with `n` nodes the **shortest possible** tree has height about `log₂ n`. A tree with a million nodes can be only about 20 levels tall, which is exactly why searching a *balanced* tree is so fast.

The other extreme is a **skewed tree**: every node has only one child, so it is just a linked list of height `n`. That is the worst case, and the reason balance matters.

```python
def skewed(n):
    root = TreeNode(0)
    node = root
    for i in range(1, n):
        node.right = TreeNode(i)
        node = node.right
    return root

def perfect(levels):
    def make(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return TreeNode(mid, make(lo, mid - 1), make(mid + 1, hi))
    return make(1, 2 ** levels - 1)

n = 15
print(f"{n} nodes in a skewed tree: height {height(skewed(n))}; arranged perfectly: height {height(perfect(4))}")
```

### How many different binary trees have `n` nodes?

Pick which node is the root; then the others split into a left part of size `k` and a right part of size `n − 1 − k`. Counting both sides' shapes independently gives a recursion:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def count_shapes(n):
    if n == 0:
        return 1                                   # exactly one empty tree
    return sum(count_shapes(k) * count_shapes(n - 1 - k) for k in range(n))

print([count_shapes(n) for n in range(1, 9)])
```

Those are the **Catalan numbers** again (1, 2, 5, 14, 42, ...). They counted balanced brackets in chapter 13: the same recursion hiding in two disguises.

```python hide
assert height(skewed(15)) == 15 and height(perfect(4)) == 4 and count_nodes(perfect(4)) == 15
assert [count_shapes(n) for n in range(1, 9)] == [1, 2, 5, 14, 42, 132, 429, 1430]
```

---

## Complexity of tree algorithms

| Algorithm | Time | Extra space |
|---|---|---|
| Any traversal (pre/in/post/level), count, height, sum | **O(n)**: every node once | O(h): the recursion stack (level order: O(width)) |
| Balanced tree | O(n) | **O(log n)** |
| Skewed tree | O(n) | **O(n)** |

The height `h` is the key variable. For a balanced tree `h ≈ log n`; for a skewed tree `h = n`. Recursive tree code on a skewed tree of a hundred thousand nodes will overflow Python's stack, so for such cases use the iterative version.

---

## Beyond binary: general trees

A node can have **any number of children**: a list of children instead of `left` and `right`. Folders, HTML and organisation charts are general trees. The recursion has the same recipe, with a loop over the children:

```python
class GeneralNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

def count_all(node):
    return 1 + sum(count_all(child) for child in node.children)    # me, plus every child's tree

def print_tree(node, depth=0):
    print("    " * depth + node.name)
    for child in node.children:
        print_tree(child, depth + 1)

company = GeneralNode("Company", [
    GeneralNode("Sales", [GeneralNode("North"), GeneralNode("South")]),
    GeneralNode("Tech", [GeneralNode("Backend")]),
    GeneralNode("HR"),
])
print_tree(company)
print(count_all(company), "nodes")
```

```python hide
assert count_all(company) == 7
```

The repo's [`dsa-topics/trees`](../dsa-topics/trees/) notebooks cover generic trees (level-wise input, nodes at a depth, preorder and postorder) alongside the binary tree code.

---

## Common mistakes

- **Forgetting the empty-tree base case**: every function must handle `None` first.
- **Confusing height (nodes) with height (edges).** State which one you mean; the answers differ by one.
- **Mixing up preorder, inorder and postorder.** Remember the position of "me" relative to the calls.
- **Computing `height` at every node** inside another recursion (O(n²)). Return it along with the answer instead (the diameter and balance tricks).
- **Using `if node.left or node.right`** when you mean "is a leaf": a leaf has *neither* child.
- **Modifying the tree while walking it** without care.
- **Not handling skewed trees:** the recursion depth equals the height.

---

## Practice

1. 🟢 Find the maximum value in a binary tree.
2. 🟢 Count the nodes **at a given depth** `k`.
3. 🟢 Check whether two trees are **identical**.
4. 🟡 Print the **left view** (the first node of each level, as seen from the left).
5. 🟡 Compute the sum of all **left leaves**.
6. 🟡 Return the **zigzag level order** (left to right, then right to left, alternating).
7. 🟡 Build a tree from its **preorder and inorder** lists.
8. 🔴 Find the **maximum path sum** between any two nodes (values can be negative).
9. 🔴 Serialise a tree to a string and rebuild it from that string.

<details>
<summary>Hints</summary>

2. Pass the remaining depth down: at depth 0 return 1 if the node exists.
4. Use level order and keep the first node of each level.
7. The first preorder value is the root. Find it in the inorder list: everything on its left is the left subtree.
8. Like the diameter: return the best *downward* path from each node, and update a global best with `left + right + me`.
</details>
