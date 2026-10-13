"""18. Hashmaps

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 18-hashmaps.py
"""

def weak_hash(text):
    return sum(ord(ch) for ch in text)

for word in ["cat", "dog", "listen", "silent", "enlist"]:
    print(f"{word:>7} -> hash {weak_hash(word):>4} -> slot {weak_hash(word) % 10}")

def good_hash(text, base=31):
    value = 0
    for ch in text:
        value = value * base + ord(ch)       # shift previous letters left, then add this one
    return value

for word in ["listen", "silent", "enlist"]:
    print(f"{word:>7} -> hash {good_hash(word):>12} -> slot {good_hash(word) % 10}")

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

table = HashMap()
for n in range(1000):
    table.put(f"user{n}", n)

lengths = [len(b) for b in table.buckets]
print(f"entries: {table.size}, slots: {len(table.buckets)}, resizes: {table.resizes}")
print(f"load factor: {table.size / len(table.buckets):.2f}")
print(f"longest bucket: {max(lengths)}, empty slots: {lengths.count(0)}")

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

good = {(1, 2): "a tuple", "name": "string", 42: "int"}
print(good[(1, 2)])

from collections import Counter

votes = ["red", "blue", "red", "green", "blue", "red"]
print(Counter(votes))
print(Counter(votes).most_common(1))

def first_unique(text):
    counts = Counter(text)
    for i, ch in enumerate(text):
        if counts[ch] == 1:
            return i
    return -1

print(first_unique("leetcode"), first_unique("aabb"))

def group_anagrams(words):
    groups = {}
    for word in words:
        signature = "".join(sorted(word))             # "eat", "tea", "ate" all become "aet"
        groups.setdefault(signature, []).append(word)
    return list(groups.values())

print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))

def count_subarrays_with_sum(numbers, k):
    count, running = 0, 0
    seen = {0: 1}                                  # the empty prefix has sum 0
    for value in numbers:
        running += value
        count += seen.get(running - k, 0)          # how many earlier prefixes make a sub-list of sum k?
        seen[running] = seen.get(running, 0) + 1
    return count

print(count_subarrays_with_sum([1, 2, 3], 3), count_subarrays_with_sum([1, 1, 1], 2))

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

print('\n[all code in this chapter ran successfully]')
