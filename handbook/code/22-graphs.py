"""22. Graphs

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 22-graphs.py
"""

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

def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = []
    visited.append(node)
    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs_recursive(graph, neighbour, visited)     # assume: this explores everything reachable from it
    return visited

print(dfs_recursive(graph, "A"))

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

print('\n[all code in this chapter ran successfully]')
