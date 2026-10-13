"""19. Trees and Binary Trees

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 19-trees.py
"""

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

def is_mirror(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.value == b.value and is_mirror(a.left, b.right) and is_mirror(a.right, b.left)

def is_symmetric(root):
    return root is None or is_mirror(root.left, root.right)

print(is_symmetric(build([1, 2, 2, 3, 4, 4, 3])), is_symmetric(build([1, 2, 2, None, 3, None, 3])))

def invert(node):
    if node is None:
        return None
    node.left, node.right = invert(node.right), invert(node.left)
    return node

flipped = invert(build([1, 2, 3, 4, 5, None, 6]))
backwards = []
inorder(flipped, backwards.append)
print(backwards)                        # an inverted tree reads backwards in order

def has_path_sum(node, target):
    if node is None:
        return False
    remaining = target - node.value
    if node.left is None and node.right is None:     # a leaf: the path ends here
        return remaining == 0
    return has_path_sum(node.left, remaining) or has_path_sum(node.right, remaining)

fresh = build([1, 2, 3, 4, 5, None, 6])
print(has_path_sum(fresh, 7), has_path_sum(fresh, 10), has_path_sum(fresh, 5))

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

def lowest_common_ancestor(node, p, q):
    if node is None or node.value in (p, q):
        return node
    left = lowest_common_ancestor(node.left, p, q)
    right = lowest_common_ancestor(node.right, p, q)
    if left and right:                               # one on each side: this is the split
        return node
    return left or right

print(lowest_common_ancestor(fresh, 4, 5).value, lowest_common_ancestor(fresh, 4, 6).value, lowest_common_ancestor(fresh, 2, 4).value)

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

from functools import lru_cache

@lru_cache(maxsize=None)
def count_shapes(n):
    if n == 0:
        return 1                                   # exactly one empty tree
    return sum(count_shapes(k) * count_shapes(n - 1 - k) for k in range(n))

print([count_shapes(n) for n in range(1, 9)])

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

print('\n[all code in this chapter ran successfully]')
