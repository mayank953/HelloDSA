# 28. DSA Behind AI

**Part 5: DSA in the AI Era** · Intermediate · about 10 minutes to read

> Top-k with a heap, similarity search, LRU caches, tries for tokenizers, graphs for knowledge, queues for batching, and cost thinking for model calls.
**In this repo:** [DSA + AI roadmap](../roadmap/README.md)  
**Run the code from this chapter:** [`code/28-dsa-behind-ai.py`](code/28-dsa-behind-ai.py)  

---

## "But AI will do all this for me"

At the start of this handbook we said that AI can write most of a program, but someone must **read it, debug it, and make it fast and cheap.** Nowhere is that more true than in AI systems themselves.

An AI product is not magic. Around the model there is ordinary software that **stores text, looks things up, remembers answers, queues requests, and plans steps**: all jobs for the data structures you now know. And because every model call costs time and money, the **complexity thinking** from chapters 3 and 4 turns directly into a bill.

In this chapter we build small, working versions of things that really exist inside AI systems. Each one is a toy, but each shows **why** the real thing uses the structure it does.

| Part of an AI system | The DSA idea |
|---|---|
| **Tokenizers** (text to tokens) | Hash maps (counting pairs), tries (longest match) |
| **Search over embeddings** (retrieval, RAG) | Top-k with a heap, clustering into buckets |
| **Caching model answers** | Hash map + doubly linked list (LRU) |
| **Rate limits and request batching** | Queues and sliding windows |
| **Knowledge graphs, tool plans** | Graphs: BFS, topological order |
| **Summarising long documents** | Recursion (a tree of summaries) |
| **Cost and latency** | Time complexity, tokens as a unit of work |

> If you have not met the AI vocabulary yet (tokens, embeddings, RAG, agents, context window), the [AI concepts guide](https://github.com/mayank953/python-ai-crash-course/tree/main/ai-concepts) in the Hello Python repository explains each term. You do not need it to follow the code below.

---

## 1. Tokens: how a tokenizer learns, with a hash map

A language model does not read letters or words; it reads **tokens**, chunks of text from a fixed **vocabulary**. Common words are one token; rare words are split into pieces. How is that vocabulary built?

One popular family of methods is **byte-pair encoding (BPE)**. The idea is wonderfully simple: *start with single characters, then repeatedly merge the **most frequent adjacent pair** into a new symbol.*

The core job is **counting pairs**, which is exactly what a hash map is for. Here is a tiny version (real tokenizers work on bytes and huge corpora, but the loop is the same):

```python
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
```

**Output**

```text
merge 1: 't' + '_' -> 't_'
merge 2: 's' + 't_' -> 'st_'
merge 3: 'e' + 'st_' -> 'est_'
merge 4: 'o' + 'w' -> 'ow'
merge 5: 'l' + 'ow' -> 'low'
merge 6: 'w' + 'est_' -> 'west_'
merge 7: 'n' + 'e' -> 'ne'
merge 8: 'ne' + 'west_' -> 'newest_'
{('low', '_'): 5, ('low', 'e', 'r', '_'): 2, ('newest_',): 6, ('w', 'i', 'd', 'est_'): 3}
```

Watch what happens: pieces that appear together often (`es`, `est`, `lo`, `low`) become single tokens. Frequent words end up as **one** token; rare words stay split into pieces. That is why common words are cheap in tokens and unusual ones cost more.

To **encode** a new word, replay the learned merges in order:

```python
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
```

**Output**

```text
['low', 'est_']
['ne', 'w', 'e', 'r', '_']
```


> **Why this matters to you.** Providers bill by tokens, and the context window is measured in tokens. Longer, rarer words and unusual scripts cost more tokens. Understanding that tokens are *learned chunks* helps you estimate and reduce cost.

---

## 2. A trie: matching the longest known piece

Once you have a vocabulary, how do you split text into tokens quickly? Many tokenizers use a **longest-match** idea: at each position, take the **longest vocabulary entry** that matches. Doing that by comparing against every entry would be slow. A **trie** (pronounced "try", from *retrieval*) makes it fast.

A trie is a tree where **each edge is a letter**. A word is a path from the root. Words that share a beginning share a path, so the structure stores prefixes **once**:

```text
          (root)
         /  |   \
        u   h    n
        |   |    |
        n   a    e
        |   |    |
        *   p    s
            |    ...
            p
            ...
```

```python
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
```

**Output**

```text
['un', 'happi', 'ness']
['happi', 'happy']
```

Matching one piece costs at most the *length of that piece*, regardless of how big the vocabulary is. The very same trie powers **autocomplete** and spell-checkers.


---

## 3. Searching by meaning: vectors and top-k

Here is the central trick of modern retrieval (RAG): represent every text as a **vector** (a list of numbers, an *embedding*) so that **texts with similar meaning get vectors that point in similar directions**. To answer a question, embed it, then find the **stored vectors most similar to the question's vector**.

The similarity measure is **cosine similarity**: 1 means the same direction, 0 unrelated, −1 opposite.

```python
import math, heapq

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def cosine(a, b):
    return dot(a, b) / (math.sqrt(dot(a, a)) * math.sqrt(dot(b, b)))

print(cosine([1, 0], [2, 0]), cosine([1, 0], [0, 1]), round(cosine([1, 1], [1, 0]), 3))
```

**Output**

```text
1.0 0.0 0.707
```

### Brute force: a heap for the top-k (chapter 21)

To find the best `k` of `n` stored vectors, score each one and keep the `k` best, using a **heap of size `k`**: **O(n · d)** work for `n` vectors of `d` numbers, plus O(n log k) for the heap.

Let us create 3,000 reproducible vectors (a tiny deterministic random-number generator keeps the output identical on every machine):

```python
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
```

**Output**

```text
[1030, 2034, 1316]
```

This is *exact*, and perfectly fine for thousands of vectors. For **millions or billions**, scoring every vector for every question is too slow. Real systems use **approximate nearest-neighbour (ANN)** indexes: structures (graph-based, tree-based, hash-based, cluster-based) that **check only a small, promising part of the data** and accept that they might occasionally miss the very best answer. It is a deliberate **speed versus accuracy trade-off**.

### A toy ANN: a clustered index

Here is the idea in a few lines. Pick 32 "landmark" vectors. Put every stored vector into the **bucket of its nearest landmark**. To answer a query, find the nearest landmarks and **search only those buckets**. Let us *measure* what we gain and what we lose:

```python
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
```

**Output**

```text
check  1 of 32 buckets: looked at  3.4% of the data, found the true best 66.0% of the time
check  4 of 32 buckets: looked at 12.6% of the data, found the true best 94.0% of the time
check  8 of 32 buckets: looked at 25.0% of the data, found the true best 100.0% of the time
check 16 of 32 buckets: looked at 49.8% of the data, found the true best 100.0% of the time
```

This is the shape of every ANN trade-off: look at **more** of the data and you find the true best **more often**, but you pay more time. Real indexes are far smarter than our toy, but the **knob between speed and recall** is the same.


---

## 4. Caching model answers: the LRU cache

Calling a large model is slow and costs money. If many users ask the **same question**, why pay again? Keep a **cache** of recent answers. But memory is limited, so when the cache is full we must **evict** something. A sensible rule: evict the **Least Recently Used (LRU)** entry (the one nobody has touched for the longest time).

An LRU cache needs two things at once, both in **O(1)**:

- **Find** an entry by key, which is a **hash map**.
- **Know the order of use**, moving an entry to "most recent" when it is touched and removing the "least recent" one when full, which is a **doubly linked list** (chapter 15: delete a node in O(1) *if you already hold it*).

The hash map hands us the node; the linked list rearranges it in O(1). Neither structure alone can do it.

```python
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
```

**Output**

```text
1 None 3
```


(In everyday Python you can use `functools.lru_cache` for function results, or `collections.OrderedDict`; building it by hand shows *why* it works.)

### What does caching save? Simulate it

Suppose 2,000 requests arrive, but people ask some questions much more often than others (a typical skew). How many calls to the "model" do we avoid with a cache of just 10 entries?

```python
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
```

**Output**

```text
2000 requests, 1085 model calls: 46% served from the cache
```


---

## 5. Queues: batching and rate limits

APIs limit how fast you may call them. A **sliding-window rate limiter** allows at most `limit` requests in any window of `window` seconds. A **deque** (chapter 17) of recent request times does it: drop timestamps that have left the window, then check the length.

```python
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
```

**Output**

```text
t= 0: allowed
t= 1: allowed
t= 2: allowed
t= 3: blocked
t= 9: blocked
t=10: allowed
t=11: allowed
t=12: allowed
t=13: blocked
```

**Batching** is the same queue idea from the other side: instead of sending one prompt at a time, collect waiting prompts and send them together to save per-call overhead.

```python
def batch(prompts, size):
    return [prompts[i:i + size] for i in range(0, len(prompts), size)]

waiting = [f"prompt {i}" for i in range(10)]
print([len(b) for b in batch(waiting, 4)], "prompts per call")
```

**Output**

```text
[4, 4, 2] prompts per call
```


---

## 6. Graphs: knowledge and plans

### A knowledge graph

Facts like "Marie Curie *worked in* Paris" are naturally **edges**. A graph lets you ask *"how are these two things related?"* by finding the **shortest path** (BFS, chapters 17 and 22). The data below is a tiny invented example:

```python
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
```

**Output**

```text
Marie Curie -> Physics -> Einstein
Paris -> France -> Europe -> Germany
```

### A plan with dependencies

An AI **agent** often breaks a goal into steps, where some steps need others to finish first. That is a **DAG**, and **topological order** (chapter 22) tells the agent a valid order to run them.

```python
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
```

**Output**

```text
['search the web', 'read the pages', 'extract the numbers', 'summarise', 'draw the chart', 'write the report']
```

If `plan` came out shorter than the number of steps, there would be a **cycle** (two steps waiting on each other), and the agent could never finish.


---

## 7. Recursion: summarising a very long document

A document may be too long for a model's **context window**. A standard remedy: **split it into chunks, summarise each chunk, then summarise the summaries**, and repeat until one summary is left. It is a **tree of summaries**, and the recursion should look very familiar.

```python
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
```

**Output**

```text
100 chunks needed 35 model calls over 4 levels, final answer: 'summary of 2'
```

Each level shrinks the number of pieces by a factor of `group_size`, so there are about `log(n) / log(group_size)` levels, and the **total number of calls is about `n / (group_size − 1)`**. That is **O(n) calls and O(log n) depth**: exactly the tree-recursion analysis from chapters 7 and 19.


---

## 8. Complexity is your bill

### Tokens are the unit of work

Providers charge per **token** (usually separately for input and output). So an O(n) or O(n²) pipeline is not only about seconds: it is about **money**. Work out the cost of a design *before* building it:

```python
price_per_million_tokens = 3.00          # an invented price in dollars, for illustration only

def monthly_cost(requests_per_day, tokens_per_request, price=price_per_million_tokens):
    tokens = requests_per_day * 30 * tokens_per_request
    return tokens / 1_000_000 * price

print(f"short prompts : ${monthly_cost(5_000, 500):,.2f} per month")
print(f"stuffing the whole document into every prompt: ${monthly_cost(5_000, 20_000):,.2f} per month")
```

**Output**

```text
short prompts : $225.00 per month
stuffing the whole document into every prompt: $9,000.00 per month
```

The second design uses **40 times** the tokens, so it costs 40 times more. *Retrieving only the relevant passage* (sections 3 and 4) is the difference. That is DSA saving money.


### Why long context is expensive

In the standard attention mechanism of a Transformer, every token is compared with every other token, so the number of comparisons grows with the **square** of the sequence length: an O(n²) shape. (Many engineering tricks reduce the cost in practice, but the shape explains why long contexts are expensive.)

```python
print(f"{'tokens':>9} | {'token pairs (n^2)':>20} | {'relative cost':>13}")
base = 1000 ** 2
for n in [1_000, 2_000, 4_000, 8_000, 16_000, 128_000]:
    print(f"{n:>9,} | {n * n:>20,} | {n * n / base:>12,.0f}x")
```

**Output**

```text
   tokens |    token pairs (n^2) | relative cost
    1,000 |            1,000,000 |            1x
    2,000 |            4,000,000 |            4x
    4,000 |           16,000,000 |           16x
    8,000 |           64,000,000 |           64x
   16,000 |          256,000,000 |          256x
  128,000 |       16,384,000,000 |       16,384x
```

Double the context, **four times** the pair-comparisons. You already know this shape from chapter 3, and now you know why teams work hard to keep prompts short and relevant.


---

## More places DSA appears

- **Edit distance** (chapter 25) powers spell-correction and the **word error rate** used to evaluate speech recognition.
- **Longest common subsequence** is behind `diff` tools and sequence comparison.
- **Dynamic programming** also underlies classic decoding algorithms (such as Viterbi) in speech and sequence models.
- **Hash maps** deduplicate training data and store feature counts.
- **Heaps and priority queues** order tasks for agents and beam search over candidate outputs.
- **Union-Find** clusters near-duplicate documents.
- **Sorting and binary search** power indexes and range queries over logs and metrics.

The pattern is always the same: **the model is one component; everything around it is data structures and algorithms**, and the people who understand them build the faster, cheaper, more reliable systems.

---

## Practice

1. 🟢 Extend the BPE trainer to print how the **number of tokens needed to encode the corpus** shrinks after each merge.
2. 🟢 Add a `delete(word)` method to the trie.
3. 🟡 Make `top_k` return `(index, score)` pairs and handle ties deterministically.
4. 🟡 Change the clustered index to probe buckets by **decreasing similarity** until a given number of candidates has been collected.
5. 🟡 Give the LRU cache a **time-to-live**: entries expire after `ttl` seconds.
6. 🟡 Implement a **token bucket** rate limiter (a different rule: tokens refill at a steady rate; each request spends one).
7. 🔴 Build a tiny **retrieval pipeline**: chunk a text file, embed each chunk with a simple bag-of-words vector, and answer a question by returning the top 3 chunks.
8. 🔴 Detect near-duplicate documents with **shingles** (sets of short word sequences) and Union-Find.
9. 🔴 Estimate the **cost** of a design that summarises 10,000 documents with the tree of summaries, and compare group sizes 2, 4 and 10.

<details>
<summary>Hints</summary>

1. After each merge, sum `len(symbols) * frequency` over the words.
5. Store `(value, expiry_time)` and treat an expired entry as a miss.
7. A bag-of-words vector counts each word; cosine similarity then works on dictionaries of counts.
9. Total calls is about `n / (group_size - 1)`; larger groups mean fewer calls but longer prompts.
</details>

---

## Where this leaves you

You now have the foundations behind both halves of modern software: the **classical** structures and algorithms, and the **AI systems** that are built on top of them. Follow the **[DSA + AI roadmap](../roadmap/README.md)** for what to build next, keep solving problems, and share your progress with **#HelloDSA**.

---

[← 27. Patterns and the Interview Playbook](27-patterns-and-interview-playbook.md) · [Handbook contents](README.md)
