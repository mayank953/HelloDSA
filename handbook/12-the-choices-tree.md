# 12. The Choices Tree: Permutations, Codes, Keypads and Hanoi

**Part 2: Recursion** · Advanced · about 11 minutes to read

> Problems where every step offers several choices. Permutations, decoding digit strings, phone keypad words, and the Tower of Hanoi.
**In the video:** [`9:11:19`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=33079s) Permutations · [`9:34:25`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=34465s) Return permutations · [`9:50:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=35400s) Return all codes · [`10:28:10`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=37690s) Phone keypad · [`10:49:58`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=38998s) Tower of Hanoi  
**In this repo:** [Strings topic: code and notes](../recursion/04-recursion-and-strings/)  
**Run the code from this chapter:** [`code/12-the-choices-tree.py`](code/12-the-choices-tree.py)  

---

## From two choices to many

In chapter 11 every step had **two** choices: take the character or leave it. The recursion tree was a binary tree. Many real problems offer **more than two** choices at each step:

- *Which of the remaining letters goes first?* (permutations)
- *Should I read one digit or two as a letter?* (decoding)
- *Which of the 3 or 4 letters on this phone key do I press?* (keypad)

The shape of the solution stays the same. The only new tool is a **loop inside the recursion**: *for every choice available right now, make that choice and recurse on what is left.* We keep using the recipe:

1. **Base case.** No decisions left: a complete answer is ready.
2. **Assume.** The recursive call handles every way of finishing from the situation I leave behind.
3. **My part.** For each choice I can make *now*, make it, and hand the rest to recursion.

We finish with the **Tower of Hanoi**, a problem that looks impossible until you see the one trick behind it.

---

## 1. Permutations: arranging the plate in order

You are at the wedding buffet again with dishes **A, B, C**. This time the **order** matters: you will eat them one after another, and `ABC` is a different meal from `BAC`.

How many orders are there? You have **3** choices for what to eat first. Whichever you pick, **2** remain for second place. Then **1** for last. So `3 × 2 × 1 = 6 = 3!` orderings. Those are the **permutations** of `"abc"`.

The recursion is just that sentence: *choose the first dish (a loop over the remaining dishes), then arrange the others.*

```python
def print_permutations(remaining, plate=""):
    if remaining == "":                       # base case: every dish has been placed
        print(plate)
        return
    for i in range(len(remaining)):
        chosen = remaining[i]                                   # choice: this dish goes next
        left_over = remaining[:i] + remaining[i + 1:]           # the dishes that are still available
        print_permutations(left_over, plate + chosen)           # assume: arrange all the rest

print_permutations("abc")
```

**Output**

```text
abc
acb
bac
bca
cab
cba
```

Let us draw the choices tree, so you can see where the six leaves come from:

```python
def show_choices(remaining, plate="", depth=0):
    pad = "    " * depth
    if remaining == "":
        print(f"{pad}done: {plate!r}")
        return
    print(f"{pad}plate={plate!r}, still available={remaining!r}")
    for i, chosen in enumerate(remaining):
        show_choices(remaining[:i] + remaining[i + 1:], plate + chosen, depth + 1)

show_choices("abc")
```

**Output**

```text
plate='', still available='abc'
    plate='a', still available='bc'
        plate='ab', still available='c'
            done: 'abc'
        plate='ac', still available='b'
            done: 'acb'
    plate='b', still available='ac'
        plate='ba', still available='c'
            done: 'bac'
        plate='bc', still available='a'
            done: 'bca'
    plate='c', still available='ab'
        plate='ca', still available='b'
            done: 'cab'
        plate='cb', still available='a'
            done: 'cba'
```

At the top there are 3 branches (a, b or c first). Each of those has 2 branches. Each of *those* has 1. The leaves are the 6 permutations. The tree has `n!` leaves, so the work grows **factorially**, which is *very* fast growth. Ten letters already give 3,628,800 permutations.

### Returning the permutations (a list of plates)

As with subsequences, to *use* the permutations we return them. The structure is the same loop, but we collect the plates:

```python
def permutations(text):
    if text == "":
        return [""]                                    # one arrangement of nothing: the empty one
    answers = []
    for i, chosen in enumerate(text):
        left_over = text[:i] + text[i + 1:]
        for smaller in permutations(left_over):        # assume: all arrangements of the left-overs
            answers.append(chosen + smaller)           # my part: put my choice in front
    return answers

print(permutations("abc"))
print(len(permutations("abcd")), "permutations of abcd")
```

**Output**

```text
['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
24 permutations of abcd
```


### A second way: insert one letter everywhere

There is another beautiful way to build permutations, the one many people find more natural. Take the permutations of the **rest**, and for each one, **insert the first character in every possible position**.

For `"abc"`: the rest is `"bc"` with permutations `bc` and `cb`. Insert `a` into `bc` at every position: `abc`, `bac`, `bca`. Insert `a` into `cb`: `acb`, `cab`, `cba`. Six permutations, with no loop over "which goes first".

```python
def permutations_by_insertion(text):
    if text == "":
        return [""]
    first, rest = text[0], text[1:]
    answers = []
    for smaller in permutations_by_insertion(rest):          # assume: all arrangements of the rest
        for position in range(len(smaller) + 1):             # every slot, including both ends
            answers.append(smaller[:position] + first + smaller[position:])
    return answers

print(permutations_by_insertion("abc"))
```

**Output**

```text
['abc', 'bac', 'bca', 'acb', 'cab', 'cba']
```


Both give the same set of answers in a different order. This is the **second approach** the video shows. Having two views of one problem is how you build real understanding.

### Duplicate letters

`permutations("aab")` returns six strings, but only three are different (`aab`, `aba`, `baa`). To avoid repeats, at each level **never choose the same letter twice**:

```python
def unique_permutations(text):
    if text == "":
        return [""]
    answers, tried = [], set()
    for i, chosen in enumerate(text):
        if chosen in tried:                    # we already used this letter as "first" at this level
            continue
        tried.add(chosen)
        for smaller in unique_permutations(text[:i] + text[i + 1:]):
            answers.append(chosen + smaller)
    return answers

print(len(permutations("aab")), "with repeats ->", unique_permutations("aab"))
```

**Output**

```text
6 with repeats -> ['aab', 'aba', 'baa']
```


**Cost.** `n!` answers, each of length `n`: **O(n · n!)**. The recursion depth is `n`.

---

## 2. Return all codes: how many ways can digits be letters?

**Question.** Let `a = 1, b = 2, ..., z = 26`. A digit string like `"123"` can be read in different ways:

- `1, 2, 3` → `abc`
- `1, 23` → `aw`
- `12, 3` → `lc`

Return every word the string can stand for. (This is a classic interview question, and a favourite at big companies.)

**The choice.** At each point you may read **one digit** as a letter, or **two digits** as a letter, *if* the two-digit number is between 10 and 26. Either way, the rest of the string is a smaller problem.

**Assume.** `return_codes(rest)` gives every word the rest can stand for.

**My part.** Put my chosen letter in front of each of those words. Do this once for the one-digit option and once for the two-digit option (when it is valid).

**Base case.** The empty string decodes to exactly one word: the empty word `""`.

**Careful with zeros.** `0` is not a letter, so a string *starting* with `0` cannot be decoded at all. `"10"` can only be read as `10 → j`, never as `1` then `0`.

```python
def to_letter(number):
    return chr(ord("a") + number - 1)           # 1 -> 'a', 2 -> 'b', ..., 26 -> 'z'

def return_codes(digits):
    if digits == "":
        return [""]                                       # one way to decode nothing
    if digits[0] == "0":
        return []                                         # a leading zero has no letter
    words = []
    for word in return_codes(digits[1:]):                 # option 1: read ONE digit
        words.append(to_letter(int(digits[0])) + word)
    if len(digits) >= 2 and 10 <= int(digits[:2]) <= 26:  # option 2: read TWO digits, if allowed
        for word in return_codes(digits[2:]):
            words.append(to_letter(int(digits[:2])) + word)
    return words

print(return_codes("123"))
print(return_codes("10"), return_codes("27"), return_codes("0"), return_codes("226"))
```

**Output**

```text
['abc', 'aw', 'lc']
['j'] ['bg'] [] ['bbf', 'bz', 'vf']
```

Draw the choices for `"123"`:

```text
"123"
 |-- read '1' -> a --  "23"
 |                      |-- read '2' -> b --  "3"  -- read '3' -> c    => "abc"
 |                      |-- read '23' -> w -- ""                       => "aw"
 |-- read '12' -> l -- "3"
                        |-- read '3' -> c -- ""                        => "lc"
```


### Counting without listing

If we only need *how many* words there are, we do not need the words themselves. The same recursion returns a number, and **the number of ways depends only on where we are in the string**, so a notebook (memoization) makes it linear. This is the same Fibonacci-like structure from chapter 7:

```python
from functools import lru_cache

def count_codes(digits):
    @lru_cache(maxsize=None)
    def ways(i):                                    # ways to decode digits[i:]
        if i == len(digits):
            return 1
        if digits[i] == "0":
            return 0
        total = ways(i + 1)
        if i + 1 < len(digits) and 10 <= int(digits[i:i + 2]) <= 26:
            total += ways(i + 2)
        return total
    return ways(0)

print(count_codes("226"), count_codes("1" * 40))
```

**Output**

```text
3 165580141
```


Forty ones can be decoded in more than 165 million ways, and it takes forty steps to *count* them. That is the power of "remember what you have already answered".

---

## 3. Words from a phone number

Old phones put letters on the keys:

```text
 2: abc    3: def
 4: ghi    5: jkl    6: mno
 7: pqrs   8: tuv    9: wxyz
```

**Question.** If someone presses `23`, which words could they mean? Every letter of key `2` can be followed by every letter of key `3`: `ad, ae, af, bd, be, bf, cd, ce, cf` (nine words).

**Smaller problem.** The digits after the first one.

**Assume.** `keypad_words(rest)` returns all words for the rest.

**My part.** For *each letter on my key*, put it in front of *each* of those words. That is two loops, a **combination of choices**.

**Base case.** No digits: one empty word.

```python
KEYS = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}

def keypad_words(digits):
    if digits == "":
        return [""]
    smaller_words = keypad_words(digits[1:])               # assume: all words for the rest
    return [letter + word                                   # my part: every letter of my key...
            for letter in KEYS[digits[0]]
            for word in smaller_words]                      # ...in front of every smaller word

print(keypad_words("23"))
print(len(keypad_words("2345")), "words for 2345")
```

**Output**

```text
['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
81 words for 2345
```


The number of words is the **product** of the letters on the keys: `3 × 3 × 3 × 3 = 81` for `2345`. Pressing `7` or `9` multiplies by 4 instead of 3.

> **A real-world bug lesson.** Look at the `KEYS` table: if you ever type `"6": "ghi"` (copying the row above) instead of `"mno"`, the program still runs and returns plausible-looking wrong words. The repository's own code for this question had exactly that slip, and we fixed it. **When a table drives your answers, test one value from every row.**


---

## 4. Tower of Hanoi

A famous puzzle. Three pegs: a **source**, a **target** (destination) and a **spare** (auxiliary). On the source peg sits a stack of `n` disks, biggest at the bottom, smallest on top. Move the whole stack to the target peg, obeying two rules:

1. Move **one disk at a time**.
2. **Never place a bigger disk on top of a smaller one.**

For one disk the answer is trivial. For three disks you will tie yourself in knots. For ten disks it feels impossible. And yet the recursive solution is **four lines long**.

### The one trick

Forget everything and look *only at the biggest disk*. It is at the bottom of the source. For it to move to the target, **everything above it must be out of the way**, and the target must be **empty**. So all `n − 1` smaller disks must sit on the **spare** peg.

So the plan has three steps:

1. Move the top `n − 1` disks from **source** to **spare** (using the target as the helper).
2. Move the big disk from **source** to **target**. (One move, easy.)
3. Move the `n − 1` disks from **spare** to **target** (using the source as the helper).

Steps 1 and 3 are *the same problem* with one fewer disk and different pegs. That is recursion! **Assume** it can move `n − 1` disks, and use that.

A way to picture it: pretend the biggest disk is glued to the bottom for a moment and invisible to the smaller disks, because it is bigger than every one of them: they can sit on top of it freely. That is why solving "n − 1 disks" works regardless of the big disk underneath.

```python
def hanoi(n, source="A", target="C", spare="B"):
    if n == 0:                                                # no disks: nothing to do
        return []
    first_half = hanoi(n - 1, source, spare, target)          # assume: n-1 disks go source -> spare
    big_move = [(source, target)]                             # my part: move the biggest disk
    second_half = hanoi(n - 1, spare, target, source)         # assume: n-1 disks go spare -> target
    return first_half + big_move + second_half

for step, (src, dst) in enumerate(hanoi(3), start=1):
    print(f"step {step}: move the top disk from {src} to {dst}")
```

**Output**

```text
step 1: move the top disk from A to C
step 2: move the top disk from A to B
step 3: move the top disk from C to B
step 4: move the top disk from A to C
step 5: move the top disk from B to A
step 6: move the top disk from B to C
step 7: move the top disk from A to C
```

Seven steps for three disks. The tiny function above *is* the entire solution. Notice what the roles do in each call: **source, target and spare rotate** as we go deeper. Whatever peg is "the spare" for one call becomes "the target" or "the source" for the next. If you ever get confused, redo the three-step plan on paper with the three names.

### How many moves?

Let `T(n)` be the number of moves for `n` disks. Our plan says `T(n) = T(n − 1) + 1 + T(n − 1) = 2·T(n − 1) + 1`, with `T(0) = 0`. Let the computer tell us the first few:

```python
print(f"{'disks':>5} | {'moves':>6} | {'2^n - 1':>7}")
for n in range(1, 11):
    print(f"{n:>5} | {len(hanoi(n)):>6} | {2 ** n - 1:>7}")
```

**Output**

```text
disks |  moves | 2^n - 1
    1 |      1 |       1
    2 |      3 |       3
    3 |      7 |       7
    4 |     15 |      15
    5 |     31 |      31
    6 |     63 |      63
    7 |    127 |     127
    8 |    255 |     255
    9 |    511 |     511
   10 |   1023 |    1023
```

The moves are exactly **2ⁿ − 1**. Let us *prove* it with PMI, using the skills from chapter 6:

- **Base case:** `T(1) = 1 = 2¹ − 1`. ✔
- **Assume** `T(k) = 2ᵏ − 1`.
- **Prove** for `k + 1`: `T(k + 1) = 2·T(k) + 1 = 2(2ᵏ − 1) + 1 = 2ᵏ⁺¹ − 2 + 1 = 2ᵏ⁺¹ − 1`. ✔

So the time is **O(2ⁿ)**, and no algorithm can do better, because 2ⁿ − 1 is the **minimum** number of moves for `n` disks. The recursion depth is only `n`.

**The legend.** An old story says monks are moving 64 golden disks, one move per second, and that the world ends when they finish. How long?

```python
moves = 2 ** 64 - 1
years = moves / (60 * 60 * 24 * 365)
print(f"{moves:,} moves at one per second is about {years / 1e9:,.0f} billion years")
```

**Output**

```text
18,446,744,073,709,551,615 moves at one per second is about 585 billion years
```

The universe is about 14 billion years old. That is what exponential growth feels like.

### Check the answer with a simulation

Never trust a puzzle solution you have not checked. This tiny simulator plays the moves and enforces the rules:

```python
def is_valid_solution(n, moves):
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    for source, target in moves:
        disk = pegs[source].pop()                               # take the top disk
        if pegs[target] and pegs[target][-1] < disk:            # illegal: bigger onto smaller
            return False
        pegs[target].append(disk)
    return pegs["C"] == list(range(n, 0, -1))                   # everything arrived, in order

print(all(is_valid_solution(n, hanoi(n)) for n in range(0, 11)))
```

**Output**

```text
True
```


If you want to *watch* it, the repo links an [animation](https://yongdanielliang.github.io/animation/web/TowerOfHanoi.html) where you can choose the number of disks.

---

## The choices tree at a glance

| Problem | Choices at each step | Depth | Leaves (answers) | Time |
|---|---|---|---|---|
| Subsequences | take / leave (2) | n | 2ⁿ | O(n · 2ⁿ) |
| Permutations | any remaining item (n, n−1, …, 1) | n | n! | O(n · n!) |
| Decode digits | 1 or 2 digits (≤ 2) | n | up to about 1.6ⁿ | exponential (linear with a memo) |
| Phone keypad | every letter on the key (3 or 4) | number of digits | 3^a · 4^b | proportional to the output |
| Tower of Hanoi | two sub-problems of size n−1 | n | 2ⁿ − 1 moves | O(2ⁿ) |

A common thread: **the output itself is huge**, so these are not "slow because the code is silly"; they are slow because the number of answers is enormous. When the question is only "how many?" or "is there at least one?", ask whether a memo or a smarter idea can skip the listing. That is exactly what dynamic programming does (chapter 25).

---

## Common mistakes

- **Mutating `remaining` in place** while looping over it. Build a **new** string for each branch (`remaining[:i] + remaining[i + 1:]`).
- **Base case `[]` instead of `[""]`** (no answers instead of one empty answer).
- **Ignoring zeros** in the decode problem, or treating `"06"` as the letter `f`.
- **Typos in lookup tables** (the keypad). Test a value from every row.
- **Mixing up the roles of the pegs** in Hanoi. Say the three steps aloud with the names `source`, `target`, `spare` and the recursive calls follow.
- **Forgetting that permutations of duplicates repeat** unless you filter them.

---

## Practice

1. 🟢 Count the permutations of `"abcd"` without generating them.
2. 🟢 Print all permutations of `"abc"` in **lexicographic** order.
3. 🟡 `permutations_of_length(text, k)`: every arrangement of `k` letters chosen from `text`.
4. 🟡 What is the largest keypad input (digits `2` to `9` only) that gives under 10,000 words?
5. 🟡 Modify `return_codes` so it also **prints** the count at the end, and test `"1111"`, `"2626"`, `"1010"`.
6. 🟡 Write `hanoi_count(n)` that returns just the number of moves without building the list. What is the base case?
7. 🔴 Hanoi with **four** pegs (the Frame-Stewart idea): can you use the extra peg to reduce the moves for `n = 4`?
8. 🔴 Generate the **next** permutation of a string in lexicographic order (no recursion). Compare with `itertools`.

<details>
<summary>Hints</summary>

1. `4! = 24`.
3. Stop the recursion when the plate has `k` characters.
4. Each digit multiplies the count by 3 or 4; solve `3^a · 4^b < 10000`.
6. `hanoi_count(0) = 0`, `hanoi_count(n) = 2 * hanoi_count(n - 1) + 1`.
7. Move some disks to one spare peg and some to the other so that fewer big moves are needed.
</details>

---

[← 11. Recursion on Strings](11-recursion-on-strings.md) · [Handbook contents](README.md) · [13. Backtracking: Choose, Explore, Undo →](13-backtracking.md)
