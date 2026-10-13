"""20. Binary Search Trees

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 20-binary-search-trees.py
"""

class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def search(node, target):
    if node is None:                     # fell off the tree: not present
        return False
    if target == node.value:
        return True
    if target < node.value:
        return search(node.left, target)        # smaller: only the left can hold it
    return search(node.right, target)           # bigger: only the right can hold it

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

def inorder(node, out):
    if node:
        inorder(node.left, out)
        out.append(node.value)
        inorder(node.right, out)
    return out

print(inorder(root, []))

def minimum(node):
    while node.left is not None:
        node = node.left
    return node

def maximum(node):
    while node.right is not None:
        node = node.right
    return node

print(minimum(root).value, maximum(root).value)

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

sample = None
for number in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    sample = insert(sample, number)

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

print('\n[all code in this chapter ran successfully]')
