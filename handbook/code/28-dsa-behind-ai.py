"""28. DSA Behind AI

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 28-dsa-behind-ai.py
"""

from collections import Counter

def pair_counts(words):
    """words maps a tuple of symbols to how often that word occurs."""
    counts = Counter()
    for symbols, frequency in words.items():
        for left, right in zip(symbols, symbols[1:]):
            counts[(left, right)] += frequency
    return counts

def merge_pair(words, pair):
    merged = {}
    for symbols, frequency in words.items():
        out, i = [], 0
        while i < len(symbols):
            if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
                out.append(symbols[i] + symbols[i + 1])      # glue the pair into one symbol
                i += 2
            else:
                out.append(symbols[i])
                i += 1
        merged[tuple(out)] = merged.get(tuple(out), 0) + frequency
    return merged

def train_bpe(text, merges):
    words = {tuple(word) + ("_",): count for word, count in Counter(text.split()).items()}   # "_" marks a word end
    learned = []
    for _ in range(merges):
        counts = pair_counts(words)
        if not counts:
            break
        best = max(counts, key=lambda pair: (counts[pair], pair))      # most frequent pair (ties: alphabetical)
        words = merge_pair(words, best)
        learned.append(best)
    return learned, words

corpus = "low low low low low lower lower newest newest newest newest newest newest widest widest widest"
merges, final_words = train_bpe(corpus, 8)
for step, pair in enumerate(merges, start=1):
    print(f"merge {step}: {pair[0]!r} + {pair[1]!r} -> {pair[0] + pair[1]!r}")
print(final_words)

def encode(word, merges):
    symbols = list(word) + ["_"]
    for left, right in merges:
        out, i = [], 0
        while i < len(symbols):
            if i < len(symbols) - 1 and symbols[i] == left and symbols[i + 1] == right:
                out.append(left + right)
                i += 2
            else:
                out.append(symbols[i])
                i += 1
        symbols = out
    return symbols

print(encode("lowest", merges))
print(encode("newer", merges))

class Trie:
    def __init__(self):
        self.children = {}                    # letter -> Trie
        self.is_word = False

    def insert(self, word):
        node = self
        for letter in word:
            node = node.children.setdefault(letter, Trie())
        node.is_word = True

    def longest_match(self, text, start):
        """The longest vocabulary word that begins at text[start]."""
        node, best = self, None
        for i in range(start, len(text)):
            node = node.children.get(text[i])
            if node is None:
                break
            if node.is_word:
                best = text[start:i + 1]
        return best

    def autocomplete(self, prefix):
        node = self
        for letter in prefix:
            node = node.children.get(letter)
            if node is None:
                return []
        found = []
        def collect(current, spelled):
            if current.is_word:
                found.append(spelled)
            for letter in sorted(current.children):
                collect(current.children[letter], spelled + letter)
        collect(node, prefix)
        return found

vocabulary = Trie()
for piece in ["un", "happi", "happy", "ness", "u", "h", "a", "p", "i", "n", "e", "s"]:
    vocabulary.insert(piece)

def tokenize(text):
    tokens, position = [], 0
    while position < len(text):
        piece = vocabulary.longest_match(text, position) or text[position]    # unknown letters become single tokens
        tokens.append(piece)
        position += len(piece)
    return tokens

print(tokenize("unhappiness"))
print(vocabulary.autocomplete("ha"))

import math, heapq

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def cosine(a, b):
    return dot(a, b) / (math.sqrt(dot(a, a)) * math.sqrt(dot(b, b)))

print(cosine([1, 0], [2, 0]), cosine([1, 0], [0, 1]), round(cosine([1, 1], [1, 0]), 3))

def pseudo_vectors(count, dimension, seed):
    state, vectors = seed, []
    for _ in range(count):
        vector = []
        for _ in range(dimension):
            state = (state * 1103515245 + 12345) % (2 ** 31)      # a classic simple generator
            vector.append(state / 2 ** 31 * 2 - 1)                 # a number between -1 and 1
        vectors.append(vector)
    return vectors

stored = pseudo_vectors(3000, 8, seed=7)
queries = pseudo_vectors(200, 8, seed=99)

def top_k(query, vectors, k=3):
    best = heapq.nlargest(k, range(len(vectors)), key=lambda i: cosine(query, vectors[i]))
    return best                                                    # the indexes of the k most similar vectors

print(top_k(queries[0], stored))

landmarks = stored[:32]
buckets = {i: [] for i in range(32)}
for index, vector in enumerate(stored):
    nearest = max(range(32), key=lambda j: cosine(vector, landmarks[j]))
    buckets[nearest].append(index)

def approximate_best(query, landmarks_to_check):
    ranked = sorted(range(32), key=lambda j: -cosine(query, landmarks[j]))[:landmarks_to_check]
    candidates = [i for j in ranked for i in buckets[j]]
    return max(candidates, key=lambda i: cosine(query, stored[i])), len(candidates)

for check in [1, 4, 8, 16]:
    hits, scanned = 0, 0
    for query in queries:
        guess, looked_at = approximate_best(query, check)
        hits += guess == top_k(query, stored, 1)[0]
        scanned += looked_at
    print(f"check {check:>2} of 32 buckets: looked at {scanned / len(queries) / len(stored):>5.1%} of the data, found the true best {hits / len(queries):>5.1%} of the time")

class LRUCache:
    class Node:
        def __init__(self, key=None, value=None):
            self.key, self.value = key, value
            self.prev = self.next = None

    def __init__(self, capacity):
        self.capacity = capacity
        self.lookup = {}                                       # key -> node: O(1) finding
        self.head, self.tail = self.Node(), self.Node()        # sentinels: head side = most recent
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.lookup.get(key)
        if node is None:
            return None
        self._unlink(node)                                     # touched: move to the front
        self._push_front(node)
        return node.value

    def put(self, key, value):
        node = self.lookup.get(key)
        if node:
            node.value = value
            self._unlink(node)
        else:
            if len(self.lookup) == self.capacity:              # full: evict the least recently used
                oldest = self.tail.prev
                self._unlink(oldest)
                del self.lookup[oldest.key]
            node = self.Node(key, value)
            self.lookup[key] = node
        self._push_front(node)

cache = LRUCache(2)
cache.put("a", 1); cache.put("b", 2)
cache.get("a")                      # "a" is now the most recently used
cache.put("c", 3)                   # the cache is full: "b" (least recently used) is evicted
print(cache.get("a"), cache.get("b"), cache.get("c"))

def request_stream(count, distinct, seed=5):
    state, stream = seed, []
    for _ in range(count):
        state = (state * 1103515245 + 12345) % (2 ** 31)
        fraction = state / 2 ** 31
        stream.append(f"question {int(fraction ** 3 * distinct)}")     # cubing skews us towards small numbers
    return stream

stream = request_stream(2000, 50)
cache, model_calls = LRUCache(10), 0
for prompt in stream:
    if cache.get(prompt) is None:
        model_calls += 1                          # a cache miss: pay for a model call
        cache.put(prompt, "an answer")
print(f"{len(stream)} requests, {model_calls} model calls: {1 - model_calls / len(stream):.0%} served from the cache")

from collections import deque

class RateLimiter:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.recent = deque()

    def allow(self, now):
        while self.recent and self.recent[0] <= now - self.window:    # forget requests older than the window
            self.recent.popleft()
        if len(self.recent) < self.limit:
            self.recent.append(now)
            return True
        return False

limiter = RateLimiter(limit=3, window=10)
for t in [0, 1, 2, 3, 9, 10, 11, 12, 13]:
    print(f"t={t:>2}: {'allowed' if limiter.allow(t) else 'blocked'}")

def batch(prompts, size):
    return [prompts[i:i + size] for i in range(0, len(prompts), size)]

waiting = [f"prompt {i}" for i in range(10)]
print([len(b) for b in batch(waiting, 4)], "prompts per call")

facts = [
    ("Marie Curie", "Physics"), ("Marie Curie", "Chemistry"), ("Marie Curie", "Paris"),
    ("Paris", "France"), ("France", "Europe"), ("Physics", "Science"), ("Chemistry", "Science"),
    ("Einstein", "Physics"), ("Einstein", "Germany"), ("Germany", "Europe"),
]
graph = {}
for a, b in facts:
    graph.setdefault(a, []).append(b)
    graph.setdefault(b, []).append(a)

def relation_path(start, goal):
    parent, queue = {start: None}, deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]
        for neighbour in graph[node]:
            if neighbour not in parent:
                parent[neighbour] = node
                queue.append(neighbour)
    return None

print(" -> ".join(relation_path("Marie Curie", "Einstein")))
print(" -> ".join(relation_path("Paris", "Germany")))

steps = {
    "search the web": ["read the pages"],
    "read the pages": ["extract the numbers", "summarise"],
    "extract the numbers": ["draw the chart"],
    "summarise": ["write the report"],
    "draw the chart": ["write the report"],
    "write the report": [],
}
in_degree = {step: 0 for step in steps}
for step in steps:
    for later in steps[step]:
        in_degree[later] += 1
ready = deque(step for step, count in in_degree.items() if count == 0)
plan = []
while ready:
    step = ready.popleft()
    plan.append(step)
    for later in steps[step]:
        in_degree[later] -= 1
        if in_degree[later] == 0:
            ready.append(later)
print(plan)

def summarise_tree(chunks, group_size, calls):
    if len(chunks) == 1:                               # base case: one summary left
        return chunks[0]
    summaries = []
    for i in range(0, len(chunks), group_size):
        group = chunks[i:i + group_size]
        calls.append(len(group))                       # one model call per group
        summaries.append(f"summary of {len(group)}")
    return summarise_tree(summaries, group_size, calls)   # assume: the recursion finishes the job

calls = []
result = summarise_tree([f"chunk {i}" for i in range(100)], 4, calls)

levels, remaining = 0, 100
while remaining > 1:                                   # how many rounds of summarising?
    remaining = -(-remaining // 4)                     # ceiling division: groups of 4
    levels += 1
print(f"100 chunks needed {len(calls)} model calls over {levels} levels, final answer: {result!r}")

price_per_million_tokens = 3.00          # an invented price in dollars, for illustration only

def monthly_cost(requests_per_day, tokens_per_request, price=price_per_million_tokens):
    tokens = requests_per_day * 30 * tokens_per_request
    return tokens / 1_000_000 * price

print(f"short prompts : ${monthly_cost(5_000, 500):,.2f} per month")
print(f"stuffing the whole document into every prompt: ${monthly_cost(5_000, 20_000):,.2f} per month")

print(f"{'tokens':>9} | {'token pairs (n^2)':>20} | {'relative cost':>13}")
base = 1000 ** 2
for n in [1_000, 2_000, 4_000, 8_000, 16_000, 128_000]:
    print(f"{n:>9,} | {n * n:>20,} | {n * n / base:>12,.0f}x")

print('\n[all code in this chapter ran successfully]')
