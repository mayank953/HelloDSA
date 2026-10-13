# 22. Graphs

**Part 3: Data Structures** · Advanced · about 10 minutes to read

> Representations, breadth-first and depth-first search, connected components, cycle detection, topological sort and shortest paths.
**In this repo:** [Graphs: practice checkpoint](../assignments/README.md)  
**Run the code from this chapter:** [`code/22-graphs.py`](code/22-graphs.py)  

---

## When data is a network

A tree is a very tidy kind of relationship: one parent, no loops. But the world is messier.

- **Cities and roads.** Many routes between places, loops everywhere.
- **Friends on a social network.** Anyone can connect to anyone.
- **Web pages and links**, **flights between airports**, **computers in a network**, **courses and their prerequisites**.

The structure for all of these is a **graph**: a set of **nodes** (also called **vertices**) joined by **edges**. A tree is just a graph with no cycles and exactly one path between any two nodes; a graph allows everything.

```text
      A ------ B                 F ------ G
      |        |
      |        |
      C ------ D ------ E
```

This graph has seven nodes and two separate pieces: `{A, B, C, D, E}` and `{F, G}`.

### Vocabulary

| Word | Meaning |
|---|---|
| **Undirected edge** | A two-way road: if A connects to B, B connects to A (friendship) |
| **Directed edge** | A one-way road: A to B does not mean B to A (following someone, a prerequisite) |
| **Weighted edge** | An edge with a cost or distance on it (kilometres, minutes) |
| **Degree** | The number of edges at a node |
| **Path** | A sequence of nodes where each consecutive pair is joined by an edge |
| **Cycle** | A path that returns to its starting node |
| **Connected** | Every node can reach every other node |
| **Connected component** | A maximal connected piece of the graph |
| **DAG** | A **D**irected **A**cyclic **G**raph: one-way edges and no cycles (course prerequisites) |

---

## Storing a graph

There are two standard ways. Let `V` be the number of nodes and `E` the number of edges.

**Adjacency matrix.** A `V × V` table; cell `[a][b]` is 1 if there is an edge from `a` to `b`. Checking an edge is O(1), but it uses **O(V²)** memory even if there are very few edges.

**Adjacency list.** For each node, a **list of its neighbours** (a dictionary from node to list). It uses **O(V + E)** memory, and walking a node's neighbours costs exactly its degree. **This is the one to use almost always**, because most real graphs are *sparse* (far fewer edges than `V²`).

```python
def build_graph(edges, directed=False):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, [])                 # make sure the other end exists as a node too
        if not directed:
            graph[b].append(a)                  # an undirected edge goes both ways
    return graph

edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("F", "G")]
graph = build_graph(edges)
for node, neighbours in graph.items():
    print(node, "->", neighbours)
```

**Output**

```text
A -> ['B', 'C']
B -> ['A', 'D']
C -> ['A', 'D']
D -> ['B', 'C', 'E']
E -> ['D']
F -> ['G']
G -> ['F']
```

| | Adjacency matrix | Adjacency list |
|---|---|---|
| Memory | O(V²) | **O(V + E)** |
| Is there an edge a-b? | **O(1)** | O(degree of a) |
| List the neighbours of a | O(V) | **O(degree of a)** |
| Best for | Dense graphs, quick edge checks | Sparse graphs, traversals |


---

## Breadth-first search (BFS)

You live in a city and want to find the **fewest bus stops** from home to a friend's place. Think of a stone dropped in a pond: the ripples spread outward **one ring at a time**. Ring 1 holds everything one stop away, ring 2 everything two stops away, and so on. The first time a ripple touches your friend's stop, you have found the shortest route.

BFS does exactly that, using a **queue** (chapter 17) so that nodes discovered first are explored first:

1. Put the start node in the queue and mark it **visited**.
2. Take a node from the **front**. Look at each neighbour; if it is not visited yet, **mark it visited** and put it at the **back**.
3. Repeat until the queue is empty.

```python
from collections import deque

def bfs_order(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)          # mark when we QUEUE it, so it is never queued twice
                queue.append(neighbour)
    return order

print(bfs_order(graph, "A"))
```

**Output**

```text
['A', 'B', 'C', 'D', 'E']
```

Visit order: `A`, then its neighbours `B` and `C` (ring 1), then `D` (ring 2), then `E` (ring 3).

### Shortest path in an unweighted graph

To get the actual route (not just the count), remember **who discovered each node** (its *parent*). Then follow parents back from the destination.

```python
def shortest_path(graph, start, goal):
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:                          # walk back through the parents
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]
        for neighbour in graph[node]:
            if neighbour not in parent:            # `parent` doubles as the visited set
                parent[neighbour] = node
                queue.append(neighbour)
    return None                                    # unreachable

print(shortest_path(graph, "A", "E"), shortest_path(graph, "A", "G"))
```

**Output**

```text
['A', 'B', 'D', 'E'] None
```

**Why is BFS's path the shortest?** Nodes are processed in order of their distance from the start, so the first time we reach the goal is along a shortest route. (This only holds when every edge counts the same. With weights, see Dijkstra below.)

**Cost.** Each node is queued once and each edge examined once (twice if undirected): **O(V + E)** time, **O(V)** space.


---

## Depth-first search (DFS)

BFS spreads out like a ripple. **DFS** behaves like someone exploring a maze: go **as deep as possible** down one corridor, and only when you hit a dead end, **back up** and try the next corridor. It is natural recursion, the same shape as backtracking (chapter 13): *choose a neighbour, explore from there, come back.*

```python
def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = []
    visited.append(node)
    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs_recursive(graph, neighbour, visited)     # assume: this explores everything reachable from it
    return visited

print(dfs_recursive(graph, "A"))
```

**Output**

```text
['A', 'B', 'D', 'C', 'E']
```

The order `A, B, D, C, E` goes deep first: `A → B → D`, then backs up to `D`'s other neighbour `C`, and so on. Now the **iterative** version. A **stack** replaces the call stack (chapter 16). It is the BFS code with one change: `pop()` instead of `popleft()`.

```python
def dfs_iterative(graph, start):
    visited, stack, order = set(), [start], []
    while stack:
        node = stack.pop()                      # the most recently added: that is the "deep" part
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbour in reversed(graph[node]): # reversed, so the first neighbour is explored first
            if neighbour not in visited:
                stack.append(neighbour)
    return order

print(dfs_iterative(graph, "A"))
```

**Output**

```text
['A', 'B', 'D', 'C', 'E']
```

> **BFS versus DFS in one line.** Same algorithm; BFS uses a **queue** (first in, first out), DFS uses a **stack** (last in, first out). That tiny difference changes everything about the order.


**When to use which**

| Need | Choose |
|---|---|
| **Shortest path** in an unweighted graph, "fewest steps" | **BFS** |
| Explore everything, detect cycles, find components, topological sort, backtracking | **DFS** |
| Very deep graphs (a recursion would overflow) | Iterative DFS, or BFS |
| Very wide graphs (a queue would use too much memory) | DFS |

---

## Connected components

How many separate pieces does the graph have? Start a search at any unvisited node and mark everything it reaches: that is **one component**. Repeat for the next unvisited node.

```python
def count_components(graph):
    visited, components = set(), 0
    for start in graph:
        if start in visited:
            continue
        components += 1                         # a new, unexplored piece
        stack = [start]
        while stack:                            # flood the whole piece
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            stack.extend(n for n in graph[node] if n not in visited)
    return components

print(count_components(graph))
```

**Output**

```text
2
```

The outer loop over *all* nodes is what makes it work on **disconnected** graphs. Forgetting it is a classic bug: a single search from one node never sees the other pieces.

### A grid is a graph: counting islands

A map of `1` (land) and `0` (water): every cell is a node, and neighbouring land cells are connected. How many islands are there? It is "count components" in disguise.

```python
def count_islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen = set()

    def sink(r, c):                              # flood this whole island with DFS
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1" or (r, c) in seen:
            return
        seen.add((r, c))
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            sink(r + dr, c + dc)

    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                islands += 1
                sink(r, c)
    return islands

print(count_islands(["11000", "11000", "00100", "00011"]))
```

**Output**

```text
3
```


---

## Detecting a cycle

**Undirected graph.** During DFS, if we meet a node we have **already visited** that is **not the node we just came from**, we have found a cycle. (The "parent" check matters: in an undirected graph every edge can be walked back, which is not a cycle.)

```python
def has_cycle_undirected(graph):
    visited = set()

    def explore(node, parent):
        visited.add(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                if explore(neighbour, node):
                    return True
            elif neighbour != parent:             # visited, and not just where we came from
                return True
        return False

    return any(explore(node, None) for node in graph if node not in visited)

print(has_cycle_undirected(graph), has_cycle_undirected(build_graph([("A", "B"), ("B", "C"), ("C", "D")])))
```

**Output**

```text
True False
```

**Directed graph.** "Already visited" is not enough: two different paths can both lead to a node without forming a cycle. We need to know whether the node is **still on the current path**. Use three states: **white** (not seen), **grey** (on the current DFS path), **black** (completely finished). Meeting a **grey** node means we looped back onto our own path.

```python
def has_cycle_directed(graph):
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {node: WHITE for node in graph}

    def explore(node):
        colour[node] = GREY                        # we are inside this node's exploration
        for neighbour in graph[node]:
            if colour[neighbour] == GREY:          # an edge back onto the current path: a cycle
                return True
            if colour[neighbour] == WHITE and explore(neighbour):
                return True
        colour[node] = BLACK                       # finished: safe
        return False

    return any(colour[node] == WHITE and explore(node) for node in graph)

loop = build_graph([("A", "B"), ("B", "C"), ("C", "A")], directed=True)
diamond = build_graph([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")], directed=True)   # two paths to D, no cycle
print(has_cycle_directed(loop), has_cycle_directed(diamond))
```

**Output**

```text
True False
```


---

## Topological sort: ordering tasks with dependencies

You must take courses with prerequisites: *Python before DSA, DSA before ML, Maths before ML, Python before Web.* In what order can you take them? A valid order puts every course **after** all its prerequisites. This is a **topological sort**, and it exists **only if the graph is a DAG** (a cycle would mean "A needs B needs A").

**Kahn's algorithm.** Count each node's **in-degree** (how many prerequisites it still waits for). Nodes with in-degree 0 are ready now. Take one, "complete" it, and reduce the in-degree of everything that depended on it, adding newly-ready nodes. If we finish with every node processed, we have an order; if some are left, there is a **cycle**.

```python
def topological_order(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbour in graph[node]:
            in_degree[neighbour] += 1
    ready = deque(node for node, degree in in_degree.items() if degree == 0)
    order = []
    while ready:
        node = ready.popleft()
        order.append(node)                           # take this course
        for neighbour in graph[node]:
            in_degree[neighbour] -= 1                # one prerequisite of `neighbour` is now done
            if in_degree[neighbour] == 0:
                ready.append(neighbour)
    return order if len(order) == len(graph) else None      # None means there was a cycle

courses = build_graph([("Python", "DSA"), ("DSA", "ML"), ("Maths", "ML"), ("Python", "Web")], directed=True)
print(topological_order(courses))
print(topological_order(loop))
```

**Output**

```text
['Python', 'Maths', 'DSA', 'Web', 'ML']
None
```


(Your order may differ from ours: usually several valid orders exist. The only rule is that every arrow points forward.)

This is how build systems order compilation, how spreadsheets decide which cell to compute first, and how package managers install dependencies.

---

## Shortest paths with weights: Dijkstra

If roads have **different lengths**, BFS's "fewest edges" is no longer "shortest distance". The fix is **Dijkstra's algorithm**.

**The idea (a GPS story).** Keep the best distance found so far to every node. Repeatedly take the **closest unfinalised node** (a *min-heap* from chapter 21 hands it to you in O(log n)), declare its distance final, and see whether going **through it** gives a better route to its neighbours (*relaxing* the edges). Because all weights are non-negative, once a node is the closest one remaining, no later route can beat it.

```python
import heapq

def dijkstra(roads, start):
    distance = {node: float("inf") for node in roads}
    distance[start] = 0
    previous = {}
    heap = [(0, start)]                              # (distance so far, node)
    while heap:
        dist, node = heapq.heappop(heap)
        if dist > distance[node]:                    # a stale entry: we found a better way already
            continue
        for neighbour, weight in roads[node]:
            candidate = dist + weight                # go to `node`, then along this road
            if candidate < distance[neighbour]:
                distance[neighbour] = candidate      # a better route: relax the edge
                previous[neighbour] = node
                heapq.heappush(heap, (candidate, neighbour))
    return distance, previous

def route(previous, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(previous[path[-1]])
    return path[::-1]

roads = {"A": [("B", 4), ("C", 2)],
         "B": [("D", 5)],
         "C": [("B", 1), ("D", 8)],
         "D": []}
distance, previous = dijkstra(roads, "A")
print(distance)
print(route(previous, "A", "D"))
```

**Output**

```text
{'A': 0, 'B': 3, 'C': 2, 'D': 8}
['A', 'C', 'B', 'D']
```

The direct road `A → B` costs 4, but `A → C → B` costs only `2 + 1 = 3`, which is why the cheapest route to `D` is `A, C, B, D` with total 8.

**Cost.** **O((V + E) log V)** with a heap. **Limitation:** it needs **non-negative** weights; a negative edge breaks the "closest is final" argument (use Bellman-Ford then).


---

## Union-Find: tracking components as edges arrive

What if edges are **added over time** and we keep asking *"are these two connected yet?"* Running a search each time is slow. **Union-Find** (disjoint-set union) answers in nearly constant time.

Each node points to a **parent**; the chain ends at a **representative** (the root). Two nodes are in the same group exactly when they have the same representative.

- **find(x):** follow parents to the root. (**Path compression:** while walking, point everyone straight at the root, flattening the structure.)
- **union(a, b):** join the two roots. (**Union by size:** attach the smaller group under the larger.)

```python
class UnionFind:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}
        self.groups = len(self.parent)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]     # path compression (halving)
            x = self.parent[x]
        return x

    def union(self, a, b):
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False                                      # already together
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a                          # the smaller group joins the larger
        self.size[root_a] += self.size[root_b]
        self.groups -= 1
        return True

uf = UnionFind("ABCDEFG")
for a, b in [("A", "B"), ("C", "D"), ("B", "D"), ("F", "G")]:
    uf.union(a, b)
print("groups:", uf.groups, " A~C?", uf.find("A") == uf.find("C"), " A~F?", uf.find("A") == uf.find("F"))
```

**Output**

```text
groups: 3  A~C? True  A~F? False
```

With both tricks, each operation takes **almost O(1)** (technically O(α(n)), the inverse Ackermann function, which is below 5 for any input you will ever meet). Union-Find is the engine of **Kruskal's minimum spanning tree** algorithm and also a quick way to detect a cycle while adding edges: if `union` returns `False`, that edge closes a cycle.


---

## Complexity summary

| Task | Algorithm | Time |
|---|---|---|
| Traverse everything | BFS or DFS | **O(V + E)** |
| Shortest path, unweighted | BFS | O(V + E) |
| Shortest path, non-negative weights | Dijkstra with a heap | O((V + E) log V) |
| Connected components | BFS / DFS / Union-Find | O(V + E) |
| Cycle detection | DFS | O(V + E) |
| Topological order | Kahn's algorithm / DFS | O(V + E) |
| Connectivity as edges arrive | Union-Find | ~O(1) per edge |

---

## Common mistakes

- **Forgetting the visited set**, so the search loops forever on a cycle.
- **Marking visited when dequeuing** instead of when enqueuing (BFS): the same node gets queued many times.
- **Running only one search** on a disconnected graph.
- **Mixing up directed and undirected** edges when building the list.
- **Using BFS for weighted shortest paths**, or Dijkstra with negative weights.
- **Recursive DFS on a huge graph**: the call stack overflows. Use an explicit stack.
- **Cycle detection in a directed graph with only a visited set**: it falsely flags diamonds. Use the three colours.

---

## Practice

1. 🟢 Does a path exist between two nodes?
2. 🟢 Find the node with the **highest degree**.
3. 🟡 *Flood fill:* change the colour of a connected region in a picture grid.
4. 🟡 *Number of provinces:* given an adjacency matrix of friendships, count the groups.
5. 🟡 *Course schedule:* can all the courses be finished (is there a cycle)? Return one valid order.
6. 🟡 *Is the graph bipartite* (can the nodes be coloured with two colours so no edge joins the same colour)? Use BFS colouring.
7. 🔴 *Word ladder:* the fewest one-letter changes from `"hit"` to `"cog"` through a word list (BFS on words).
8. 🔴 *Cheapest flights within k stops:* a variation of Dijkstra or Bellman-Ford.
9. 🔴 Use Union-Find to compute a **minimum spanning tree** (Kruskal): sort edges by weight, add an edge if it joins two different groups.

<details>
<summary>Hints</summary>

3. DFS or BFS from the starting cell, repainting cells of the old colour.
6. Colour the start 0, its neighbours 1, their neighbours 0; if a neighbour already has the same colour as you, it is not bipartite.
7. Each word is a node; two words are neighbours if they differ by one letter. BFS from `"hit"` gives the fewest changes.
</details>

---

[← 21. Heaps and Priority Queues](21-heaps.md) · [Handbook contents](README.md) · [23. Sorting Algorithms Compared →](23-sorting-compared.md)
