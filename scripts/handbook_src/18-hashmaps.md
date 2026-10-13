## The cloakroom idea

At a big event you hand in your coat and receive a **numbered token**. Later you show token **47** and the attendant walks **straight to hook 47**. They do not look through every coat. The token *is* the address.

Now imagine that the token was not an arbitrary number but **computed from your name**, so you never even need to remember it. Say "Asha Verma", the attendant runs a quick calculation in their head, gets "hook 12", and walks there.

That is a **hash map** (also called a hash table, or in Python a `dict`):

- You store a **value** under a **key** (name → phone number).
- A **hash function** turns the key into a number.
- That number, reduced to fit the table, says **which slot** to use.

Lookup, insert and delete become **O(1) on average**, no matter how many entries you have. Of all the data structures in this handbook, this is the one you will use most in real programs and interviews.

> **The core trick:** *instead of searching for the key, compute where it must be.*

---

## Step 1: a hash function

A **hash function** takes a key and returns a whole number. Then `number % capacity` gives a slot index between `0` and `capacity − 1`.

Let us invent the simplest one: add up the character codes of a string.

```python
def weak_hash(text):
    return sum(ord(ch) for ch in text)

for word in ["cat", "dog", "listen", "silent", "enlist"]:
    print(f"{word:>7} -> hash {weak_hash(word):>4} -> slot {weak_hash(word) % 10}")
```

Look at `listen`, `silent`, `enlist`: they are **anagrams**, so they add up to the same number and land in the **same slot**. Different keys with the same slot are called a **collision**, and a hash function that creates many of them is a bad one. Order matters, so let us make it order-sensitive with a **polynomial hash** (the same idea behind many real hash functions): treat the text as digits of a number in some base.

```python
def good_hash(text, base=31):
    value = 0
    for ch in text:
        value = value * base + ord(ch)       # shift previous letters left, then add this one
    return value

for word in ["listen", "silent", "enlist"]:
    print(f"{word:>7} -> hash {good_hash(word):>12} -> slot {good_hash(word) % 10}")
```

Anagrams now get different hashes. Good hash functions follow three rules:

1. **Same key, same hash**, always (or lookups would break).
2. **Spread keys evenly** across the slots.
3. **Fast** to compute.

```python hide
assert weak_hash("listen") == weak_hash("silent") == weak_hash("enlist")
assert len({good_hash(w) for w in ["listen", "silent", "enlist"]}) == 3
assert good_hash("a") == 97 and good_hash("ab") == 97 * 31 + 98
```

---

## Step 2: collisions are inevitable

Say the table has 10 slots and you insert 11 keys. By the **pigeonhole principle** at least two keys share a slot. Even with *fewer* keys than slots, random keys collide surprisingly often (the same maths as the "birthday paradox": in a room of just 23 people, two probably share a birthday).

So any real hash table needs a **collision strategy**. There are two main families.

### Strategy A: chaining

Each slot holds a **small list** (a *bucket*) of all the entries that landed there. To look up a key: hash it, go to its bucket, and scan the (short) bucket.

```text
slot 0:  [ ]
slot 1:  [("cat", 3)] -> [("tac", 9)]       <- a collision: both live in slot 1
slot 2:  [("dog", 5)]
slot 3:  [ ]
```

```python
class HashMap:
    """A hash map using chaining, with automatic resizing."""
    MAX_LOAD = 0.75

    def __init__(self, capacity=4):
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0
        self.resizes = 0

    def _slot(self, key):
        return good_hash(str(key)) % len(self.buckets)

    def put(self, key, value):
        bucket = self.buckets[self._slot(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:                  # the key exists: replace its value
                bucket[i] = (key, value)
                return
        bucket.append((key, value))                  # a new key
        self.size += 1
        if self.size / len(self.buckets) > self.MAX_LOAD:
            self._grow()

    def get(self, key, default=None):
        for existing_key, value in self.buckets[self._slot(key)]:
            if existing_key == key:
                return value
        return default

    def remove(self, key):
        bucket = self.buckets[self._slot(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def _grow(self):
        old_entries = [entry for bucket in self.buckets for entry in bucket]
        self.buckets = [[] for _ in range(len(self.buckets) * 2)]    # double the slots
        self.size = 0
        self.resizes += 1
        for key, value in old_entries:                               # re-insert (re-hash) everything
            self.put(key, value)

phone_book = HashMap()
phone_book.put("Asha", 98100)
phone_book.put("Ravi", 98200)
phone_book.put("Meera", 98300)
phone_book.put("Asha", 98111)                  # update an existing key

print(phone_book.get("Asha"), phone_book.get("Ravi"), phone_book.get("Nobody", "not found"))
print(phone_book.remove("Ravi"), phone_book.get("Ravi"), phone_book.size)
```

### The load factor and why we resize

If we keep adding to a fixed number of slots, buckets get longer and longer, and lookups degrade towards scanning a list. The key number is the **load factor**:

> **load factor = entries ÷ slots**

When it passes a limit (here 0.75) we **double the slots and re-insert every entry** (every hash must be recomputed because `% capacity` changed). Like the growing array in chapter 14, that rehashing is expensive but rare, so inserts stay **amortised O(1)**.

Watch the table grow, and see how *evenly* the entries spread:

```python
table = HashMap()
for n in range(1000):
    table.put(f"user{n}", n)

lengths = [len(b) for b in table.buckets]
print(f"entries: {table.size}, slots: {len(table.buckets)}, resizes: {table.resizes}")
print(f"load factor: {table.size / len(table.buckets):.2f}")
print(f"longest bucket: {max(lengths)}, empty slots: {lengths.count(0)}")
```

Even with a thousand entries the longest bucket is tiny, so a lookup touches only a handful of entries. That is how "O(1) on average" comes true.

```python hide
assert table.size == 1000 and all(table.get(f"user{n}") == n for n in range(1000))
assert table.size / len(table.buckets) <= HashMap.MAX_LOAD and max(lengths) < 15
assert phone_book.get("Asha") == 98111 and phone_book.get("Ravi") is None and phone_book.size == 2
```

### Strategy B: open addressing (linear probing)

Instead of buckets, keep **one entry per slot**. If the slot is taken, **try the next one**, then the next, wrapping around, until you find an empty slot. To look up, follow the same trail.

```text
insert "cat" -> slot 3 (free)               [ . . . cat . . . . ]
insert "tac" -> slot 3 taken, try 4 (free)  [ . . . cat tac . . . ]
find   "tac" -> start at slot 3, not it, try slot 4: found it
```

**Deleting is tricky.** If you simply empty slot 3, the trail to `tac` is broken: a lookup for `tac` would start at 3, see "empty" and wrongly give up. So we leave a **tombstone** marker meaning "something was here; keep walking".

```python
EMPTY, TOMBSTONE = object(), object()

class LinearProbingMap:
    def __init__(self, capacity=8):
        self.keys = [EMPTY] * capacity
        self.values = [None] * capacity
        self.size = 0

    def _find(self, key):
        """Return (slot of key or None, first reusable slot)."""
        capacity = len(self.keys)
        start = good_hash(str(key)) % capacity
        reusable = None
        for step in range(capacity):
            i = (start + step) % capacity                 # try the next slot, wrapping around
            if self.keys[i] is EMPTY:
                return None, (reusable if reusable is not None else i)
            if self.keys[i] is TOMBSTONE:
                if reusable is None:
                    reusable = i
            elif self.keys[i] == key:
                return i, reusable
        return None, reusable

    def put(self, key, value):
        found, reusable = self._find(key)
        if found is not None:
            self.values[found] = value
            return
        if reusable is None:
            raise OverflowError("table is full")
        self.keys[reusable], self.values[reusable] = key, value
        self.size += 1

    def get(self, key, default=None):
        found, _ = self._find(key)
        return self.values[found] if found is not None else default

    def remove(self, key):
        found, _ = self._find(key)
        if found is None:
            return False
        self.keys[found], self.values[found] = TOMBSTONE, None
        self.size -= 1
        return True

pm = LinearProbingMap()
for word in ["cat", "tac", "act"]:
    pm.put(word, len(word))
print(pm.get("tac"), pm.remove("cat"), pm.get("tac"), pm.get("act"))
```

```python hide
p = LinearProbingMap(8)
for i in range(6): p.put(f"k{i}", i)
for i in range(0, 6, 2): assert p.remove(f"k{i}")
assert [p.get(f"k{i}") for i in range(6)] == [None, 1, None, 3, None, 5]
p.put("k0", 99); assert p.get("k0") == 99 and p.size == 4
```

The repo's `dsa-topics/hashmaps/code/linear-probing.py` is a version of this. Open addressing keeps everything in one array (good for caches) but **degrades faster as the table fills**. Let us measure that, counting how many slots a successful lookup visits on average at different load factors:

```python
def average_probes(load_factor, capacity=2003):
    keys = [f"key{i}" for i in range(int(capacity * load_factor))]
    slots = [None] * capacity
    for key in keys:                                    # insert with linear probing
        i = good_hash(key) % capacity
        while slots[i] is not None:
            i = (i + 1) % capacity
        slots[i] = key
    total = 0
    for key in keys:                                    # count the slots visited to find each key
        i = good_hash(key) % capacity
        total += 1
        while slots[i] != key:
            i = (i + 1) % capacity
            total += 1
    return total / len(keys)

for load in [0.25, 0.5, 0.75, 0.9, 0.95]:
    print(f"load factor {load:.2f}: {average_probes(load):.2f} slots visited per lookup")
```

Lookups stay near 1 or 2 slots for a half-full table, then climb quickly as it fills up. That is why real implementations resize **before** the table gets crowded (Python's `dict` resizes well under 100% full).

---

## Python's `dict` and `set`

Python's `dict` *is* a hash map (and `set` is a hash map with keys only). A few facts worth knowing:

- Keys must be **hashable**, which in practice means **immutable**: strings, numbers, tuples of those. A list cannot be a key.

```python expect-error
bad = {}
bad[[1, 2]] = "a list"
```

  Why? If a key could change after it was stored, its hash would change, and the entry would be lost in the wrong slot. A tuple works:

```python
good = {(1, 2): "a tuple", "name": "string", 42: "int"}
print(good[(1, 2)])
```

- Since Python 3.7 a `dict` **remembers insertion order**.
- Looking something up (`key in my_dict`, `my_dict[key]`) is **O(1) on average**; the **worst case is O(n)** if everything collides (which a good hash function makes extremely unlikely).
- Never change a dict's size **while looping over it**.

| Operation | Average | Worst case |
|---|---|---|
| `d[key]`, `key in d` | **O(1)** | O(n) |
| `d[key] = value` | **O(1)** (amortised) | O(n) |
| `del d[key]` | **O(1)** | O(n) |
| Iterating all entries | O(n) | O(n) |

---

## Patterns that use hash maps

You already used one: **Two Sum** in chapter 14. Here are more, because this is where hash maps earn their reputation.

### Pattern 1: counting

```python
from collections import Counter

votes = ["red", "blue", "red", "green", "blue", "red"]
print(Counter(votes))
print(Counter(votes).most_common(1))
```

**First non-repeating character:** count everything in one pass, then find the first character with count 1 in a second pass. **O(n)**.

```python
def first_unique(text):
    counts = Counter(text)
    for i, ch in enumerate(text):
        if counts[ch] == 1:
            return i
    return -1

print(first_unique("leetcode"), first_unique("aabb"))
```

### Pattern 2: group by a *signature*

**Group the anagrams** in `["eat", "tea", "tan", "ate", "nat", "bat"]`. Anagrams are words with the same letters, so **sorting a word's letters gives a signature** that all its anagrams share. Use the signature as the dictionary key.

```python
def group_anagrams(words):
    groups = {}
    for word in words:
        signature = "".join(sorted(word))             # "eat", "tea", "ate" all become "aet"
        groups.setdefault(signature, []).append(word)
    return list(groups.values())

print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
```

This idea (choose a **canonical form** as the key) is behind many "group the equivalent things" problems.

### Pattern 3: prefix sums and a hash map

**Question.** Count the sub-lists of `numbers` that add up to `k`. For `[1, 2, 3]` and `k = 3`: `[1, 2]` and `[3]` give 2.

**Idea.** A sub-list from `i` to `j` sums to `k` exactly when `prefix[j + 1] − prefix[i] = k` (chapter 14). While scanning, keep a hash map of **how many times each prefix sum has appeared**. At each step, the number of earlier prefix sums equal to `running − k` is the number of sub-lists *ending here* with sum `k`.

```python
def count_subarrays_with_sum(numbers, k):
    count, running = 0, 0
    seen = {0: 1}                                  # the empty prefix has sum 0
    for value in numbers:
        running += value
        count += seen.get(running - k, 0)          # how many earlier prefixes make a sub-list of sum k?
        seen[running] = seen.get(running, 0) + 1
    return count

print(count_subarrays_with_sum([1, 2, 3], 3), count_subarrays_with_sum([1, 1, 1], 2))
```

A nested-loop solution is O(n²). This is **O(n)**.

### Pattern 4: sets for "have I seen it?" and for ranges

**Longest run of consecutive numbers** in an unsorted list in O(n): put everything in a set; only start counting from numbers that have **no predecessor** (`x − 1` not in the set), then walk upward.

```python
def longest_consecutive(numbers):
    present = set(numbers)
    best = 0
    for x in present:
        if x - 1 not in present:                   # x begins a run
            length = 1
            while x + length in present:
                length += 1
            best = max(best, length)
    return best

print(longest_consecutive([100, 4, 200, 1, 3, 2]))
```

### Pattern 5: memoization is a hash map

The notebook of answers in chapter 7 was a dictionary all along: **key = the arguments, value = the answer**. That is the bridge to dynamic programming.

```python hide
assert Counter(votes).most_common(1) == [("red", 3)]
assert first_unique("leetcode") == 0 and first_unique("loveleetcode") == 2 and first_unique("aabb") == -1
assert sorted(map(sorted, group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))) == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
assert count_subarrays_with_sum([1, 2, 3], 3) == 2 and count_subarrays_with_sum([1, 1, 1], 2) == 2
import random
rng = random.Random(4)
for _ in range(100):
    data = [rng.randint(-3, 3) for _ in range(rng.randint(0, 14))]
    k = rng.randint(-4, 4)
    brute = sum(1 for i in range(len(data)) for j in range(i, len(data)) if sum(data[i:j + 1]) == k)
    assert count_subarrays_with_sum(data, k) == brute
assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4 and longest_consecutive([]) == 0
```

---

## Hash map or something else?

| You need... | Use |
|---|---|
| Fast lookup, insert, delete by key | **Hash map / set** |
| Keys in **sorted order**, range queries ("all keys between a and b") | A balanced tree (chapter 20) or sort the keys |
| The smallest or largest quickly | A **heap** (chapter 21) |
| Order of insertion with fast ends | `deque`, or `dict` (which remembers insertion order) |

---

## Common mistakes

- **Mutable keys.** Lists and dicts cannot be keys; use tuples.
- **Assuming a hash map keeps keys sorted.** It does not (it keeps *insertion* order, which is different).
- **Changing a dict while iterating over it.** Iterate over `list(d)` instead.
- **`defaultdict` side effect:** *reading* a missing key creates it.
- **Forgetting a collision strategy** when building your own table, or forgetting to **rehash** when growing.
- **Trusting `hash()` values to be stable between runs** (Python randomises string hashes for security). Never store them.
- **Treating O(1) as "free".** A hash computation on a very long key takes time proportional to the key's length.

---

## Practice

1. 🟢 Check whether a list contains a duplicate, in O(n).
2. 🟢 Check whether two strings are anagrams using a Counter.
3. 🟡 Find the intersection of two lists (each common value once).
4. 🟡 *Isomorphic strings:* can the letters of `s` be replaced to get `t` with a consistent one-to-one mapping?
5. 🟡 Given a list and a target, find all **unique pairs** that sum to the target.
6. 🟡 Return the **top k most frequent** words (bucket by count, or use a heap from chapter 21).
7. 🔴 *Longest substring with at most k distinct characters* (a sliding window plus a count dictionary).
8. 🔴 Implement `HashMap` **with open addressing and automatic resizing**, then compare its probe counts with the chaining version.

<details>
<summary>Hints</summary>

1. Put items in a set; if an item is already there, return `True`.
4. Keep two dictionaries (s→t and t→s) and check both directions stay consistent.
7. Expand the right edge adding to a count dict; while the dict has more than k keys, shrink from the left, removing keys whose count hits 0.
</details>
