# 11. Recursion on Strings

**Part 2: Recursion** · Intermediate · about 7 minutes to read

> Remove a character, palindromes, and the take-or-skip idea behind subsequences, with the wedding-plate story.
**In the video:** [`7:46:50`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=28010s) Recursion with strings · [`8:03:10`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=28990s) Palindrome · [`8:30:09`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=30609s) Substring vs subsequence · [`8:36:04`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=30964s) Print all subsequences · [`8:55:10`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=32110s) Return all subsequences  
**In this repo:** [Recursion and strings: code, notes, notebooks](../recursion/04-recursion-and-strings/)  
**Run the code from this chapter:** [`code/11-recursion-on-strings.py`](code/11-recursion-on-strings.py)  

---

## A string is a list of characters (with one catch)

Everything you learned about recursion on lists applies to strings, because a string is a sequence of characters:

- the **first character** `s[0]` is "my job",
- the **rest** `s[1:]` is the smaller problem,
- the **base case** is the empty string `""` (or sometimes a one-character string).

The one catch: Python strings are **immutable**. You cannot change a character in place. Every "change" builds a **new** string. That is fine for recursion (we like returning new values), but keep it in mind for cost.

```python
text = "recursion"
print(text[0], "|", text[1:], "|", text[-1], "|", text[:-1])
print(text[1:3], text[::-1], len(text))
```

**Output**

```text
r | ecursion | n | recursio
ec noisrucer 9
```

We use slicing in this chapter because it keeps the ideas short. If cost matters, pass an index (chapter 9).

---

## Problem 1: remove every occurrence of a character

**Question.** `remove("abczz", "z") → "abc"`. (A classic warm-up.)

**Smaller problem.** Everything after the first character.

**Assume.** `remove(rest, ch)` returns the rest with every `ch` already removed.

**My part.** Look at my own character. If it equals `ch`, drop it (return just the cleaned rest). Otherwise keep it in front.

**Base case.** The empty string stays empty.

```python
def remove(text, ch):
    if text == "":                       # base case
        return ""
    cleaned_rest = remove(text[1:], ch)  # assume: the rest without any ch
    if text[0] == ch:
        return cleaned_rest              # my character is unwanted: drop it
    return text[0] + cleaned_rest        # keep my character in front

print(remove("abczz", "z"), remove("good morning", "o"), remove("zzz", "z") == "", remove("abc", "x"))
```

**Output**

```text
abc gd mrning True abc
```


**Cost.** One call per character; each call builds a new string, so it is **O(n²)** in the worst case with slicing (every slice and concatenation copies). With an index and a list of kept characters it would be O(n).

> **Habit from the video:** for *every* string problem, test the empty string, a one-character string, a string where *everything* matches, and a string where *nothing* matches.

---

## Problem 2: replace and clean (two classics)

### Replace every `"pi"` with `"3.14"`

This is a famous interview question with a small twist: **look at two characters at a time**.

**Smaller problem.** If the string *starts with* `"pi"`, the smaller problem is the string after those two characters. Otherwise it is the string after one character.

```python
def replace_pi(text):
    if len(text) <= 1:                         # base case: too short to contain "pi"
        return text
    if text[0:2] == "pi":
        return "3.14" + replace_pi(text[2:])   # consume two characters, write the replacement
    return text[0] + replace_pi(text[1:])      # consume one

print(replace_pi("pippppiiiipi"))
```

**Output**

```text
3.14ppp3.14iii3.14
```

### Collapse adjacent duplicates: `"aabbbccd" → "abcd"`

**My part.** Compare my character with the next one. If they are equal, skip mine (the next one will stand in for both).

```python
def collapse(text):
    if len(text) <= 1:
        return text
    if text[0] == text[1]:
        return collapse(text[1:])              # drop me; the next identical letter carries on
    return text[0] + collapse(text[1:])

print(collapse("aabbbccd"), collapse("abc"), collapse("aaaa"))
```

**Output**

```text
abcd abc a
```


Both problems have the same shape: *decide what to do with my first character(s), then hand the rest to recursion.*

---

## Problem 3: is it a palindrome?

A **palindrome** reads the same forwards and backwards: `"nitin"`, `"madam"`, `"racecar"`.

**The idea.** Compare the **first** and **last** characters. If they differ, it is not a palindrome. If they match, the question becomes the same question for the **inside** (everything between them).

**Assume.** `is_palindrome(inside)` is correct.

**My part.** First equals last, *and* the inside is a palindrome.

**Base case.** A string of length 0 or 1 is a palindrome.

```python
def is_palindrome(text):
    if len(text) <= 1:                    # base case
        return True
    if text[0] != text[-1]:               # my part, checked FIRST: a mismatch decides the answer
        return False
    return is_palindrome(text[1:-1])      # assume: the middle part

print(is_palindrome("nitin"), is_palindrome("abca"), is_palindrome(""), is_palindrome("ab"))
```

**Output**

```text
True False True False
```

Notice, as in "is it sorted?", that we check **before** recursing so we can stop at the first mismatch.

The version that avoids copying uses two indexes, `start` and `end`, closing in from both ends (this is the helper function from the video):

```python
def palindrome_helper(text, start, end):
    if start >= end:                       # the pointers met or crossed: all pairs matched
        return True
    if text[start] != text[end]:
        return False
    return palindrome_helper(text, start + 1, end - 1)

def is_palindrome_fast(text):
    return palindrome_helper(text, 0, len(text) - 1)

print(is_palindrome_fast("nitin"), is_palindrome_fast("nitinr"))
```

**Output**

```text
True False
```

A real-world variation ignores case and punctuation (`"A man, a plan, a canal: Panama"`). Clean the string once, outside the recursion:

```python
def is_clean_palindrome(sentence):
    letters = "".join(ch.lower() for ch in sentence if ch.isalnum())
    return is_palindrome_fast(letters)

print(is_clean_palindrome("A man, a plan, a canal: Panama"))
```

**Output**

```text
True
```


---

## Substring versus subsequence

Two words that confuse everybody. Take the string `"abc"`.

- A **substring** is a **continuous** piece: `a`, `b`, `c`, `ab`, `bc`, `abc`. (You cannot skip letters.)
- A **subsequence** keeps the **order**, but you may **skip** letters: all the substrings, plus `ac`, plus the empty string. (You may skip, but you may not reorder: `ca` is *not* a subsequence.)

```python
text = "abc"

substrings = {text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1)}
print("substrings   :", sorted(substrings))

from itertools import combinations
subsequences = {"".join(c) for size in range(len(text) + 1) for c in combinations(text, size)}
print("subsequences :", sorted(subsequences))
print(len(substrings), "substrings (n(n+1)/2 =", len(text) * (len(text) + 1) // 2, ") and", len(subsequences), "subsequences (2^n =", 2 ** len(text), ")")
```

**Output**

```text
substrings   : ['a', 'ab', 'abc', 'b', 'bc', 'c']
subsequences : ['', 'a', 'ab', 'abc', 'ac', 'b', 'bc', 'c']
6 substrings (n(n+1)/2 = 6 ) and 8 subsequences (2^n = 8 )
```

A string of length `n` has `n(n+1)/2` substrings but **2ⁿ subsequences**. That exponential count is the clue: *subsequences are about choices, and the recursion tree doubles at every letter.*

---

## The wedding buffet: take it or leave it

You are at a wedding with a buffet of three dishes: **A, B, C**. For **each** dish you decide: put it on your plate, or **leave it**.

- Dish A: take or leave (2 choices).
- Dish B: take or leave (2 choices).
- Dish C: take or leave (2 choices).

Total plates you can make: `2 × 2 × 2 = 8`. They are:

```text
leave A, leave B, leave C   ->  (empty plate)
leave A, leave B, take  C   ->  C
leave A, take  B, leave C   ->  B
leave A, take  B, take  C   ->  BC
take  A, leave B, leave C   ->  A
take  A, leave B, take  C   ->  AC
take  A, take  B, leave C   ->  AB
take  A, take  B, take  C   ->  ABC
```

Those eight plates **are** the eight subsequences of `"abc"`. The whole problem is: *"for each character, take it or leave it; keep the order."*

That is a recursion, because **after deciding about the first dish, the situation is the same question for the remaining dishes.** Let us *watch* the decisions as a tree:

```python
def explore(remaining, plate, depth=0):
    pad = "    " * depth
    if remaining == "":
        print(f"{pad}-> plate is complete: {plate!r}")
        return
    dish = remaining[0]
    print(f"{pad}dish {dish!r}: take it")
    explore(remaining[1:], plate + dish, depth + 1)
    print(f"{pad}dish {dish!r}: leave it")
    explore(remaining[1:], plate, depth + 1)

explore("ab", "")
```

**Output**

```text
dish 'a': take it
    dish 'b': take it
        -> plate is complete: 'ab'
    dish 'b': leave it
        -> plate is complete: 'a'
dish 'a': leave it
    dish 'b': take it
        -> plate is complete: 'b'
    dish 'b': leave it
        -> plate is complete: ''
```

(We used two dishes so the picture fits on a page. Run it with `"abc"` to see all eight leaves.)

Every dish makes two branches: **take** and **leave**. After `n` dishes the tree has `2ⁿ` leaves, and each leaf is one complete plate.

---

## Problem 4a: *print* all subsequences

The plate you are building is passed **down** as an extra argument, `taken_so_far`. When there are no dishes left, the plate is finished: print it.

**Smaller problem.** The dishes after the first one.

**Assume.** The recursion prints every plate that can be made from the remaining dishes, starting from my current plate.

**My part.** Make the two choices, one call each.

**Base case.** No dishes left: print the plate.

```python
def print_subsequences(remaining, taken_so_far=""):
    if remaining == "":
        print(repr(taken_so_far))
        return
    first, rest = remaining[0], remaining[1:]
    print_subsequences(rest, taken_so_far + first)    # choice 1: take the first dish
    print_subsequences(rest, taken_so_far)            # choice 2: leave the first dish

print_subsequences("abc")
```

**Output**

```text
'abc'
'ab'
'ac'
'a'
'bc'
'b'
'c'
''
```

The order printed is the order of the tree's leaves, left to right: everything that **takes** `a` comes before everything that leaves it.

---

## Problem 4b: *return* all subsequences

Often we need the answers **as data**, not just printed. Here the diary lesson (chapter 9) applies: *return a new list.*

**Smaller problem.** The subsequences of the **rest** of the string.

**Assume.** `subsequences(rest)` returns a list of *all* subsequences of `rest`. For `"bc"` that is `["", "b", "c", "bc"]` in some order. (This is the plate-list the "friend" hands back.)

**My part.** Each plate for `"abc"` is either a plate for `"bc"` *without* `a`, or the same plate *with* `a` put in front. So: copy every plate, and also add a version of each with `a` in front.

**Base case.** The empty string has exactly **one** subsequence: the empty plate. So the base case returns **`[""]`**, a list containing one empty string. *Not* an empty list. (Returning `[]` would say "there are no plates at all" and every answer would vanish.)

```python
def subsequences(text):
    if text == "":
        return [""]                                  # exactly one plate: the empty one
    first, rest = text[0], text[1:]
    small_answer = subsequences(rest)                # assume: every plate from the rest
    with_first = [first + plate for plate in small_answer]   # plates where I TAKE my dish
    return small_answer + with_first                 # plates where I LEAVE it, then those with it

print(subsequences("abc"))
print(len(subsequences("abcd")), "subsequences of abcd")
```

**Output**

```text
['', 'c', 'b', 'bc', 'a', 'ac', 'ab', 'abc']
16 subsequences of abcd
```

Trace the build-up for `"abc"` from the bottom of the recursion up:

```text
subsequences("")    = [""]
subsequences("c")   = [""] + ["c"]                     = ["", "c"]
subsequences("bc")  = ["", "c"] + ["b", "bc"]          = ["", "c", "b", "bc"]
subsequences("abc") = ["", "c", "b", "bc"] + ["a", "ac", "ab", "abc"]
```


The pass-the-list-down style also works, for completeness:

```python
def fill_subsequences(remaining, taken_so_far, answers):
    if remaining == "":
        answers.append(taken_so_far)
        return
    fill_subsequences(remaining[1:], taken_so_far + remaining[0], answers)
    fill_subsequences(remaining[1:], taken_so_far, answers)

answers = []
fill_subsequences("abc", "", answers)
print(answers)
```

**Output**

```text
['abc', 'ab', 'ac', 'a', 'bc', 'b', 'c', '']
```


**Cost.** There are `2ⁿ` plates, and building each takes up to `n` characters: **O(n · 2ⁿ)** time, and the answer itself is **O(2ⁿ)** items of space. Nothing can beat that, because the output alone has that many items. The recursion depth is only `n`.

---

## Variations worth knowing

The same take-or-leave skeleton solves a whole family of problems. Change "my part", keep the shape:

```python
def subsequences_of_length(text, k):
    """All subsequences with exactly k characters (these are the combinations)."""
    if k == 0:
        return [""]
    if len(text) < k:
        return []                                   # not enough letters left to fill k places
    first, rest = text[0], text[1:]
    taking = [first + s for s in subsequences_of_length(rest, k - 1)]
    leaving = subsequences_of_length(rest, k)
    return taking + leaving

print(subsequences_of_length("abcd", 2))
```

**Output**

```text
['ab', 'ac', 'ad', 'bc', 'bd', 'cd']
```

```python
def distinct_subsequences(text):
    """Duplicates in the input would repeat subsequences; a set removes them."""
    return sorted(set(subsequences(text)))

print(distinct_subsequences("aab"))
```

**Output**

```text
['', 'a', 'aa', 'aab', 'ab', 'b']
```

```python
def subsequences_with_sum(numbers, target, i=0, running=0):
    """Count the subsets of numbers[i:] that, added to `running`, reach target."""
    if i == len(numbers):
        return 1 if running == target else 0
    taking = subsequences_with_sum(numbers, target, i + 1, running + numbers[i])
    leaving = subsequences_with_sum(numbers, target, i + 1, running)
    return taking + leaving

print(subsequences_with_sum([2, 3, 5, 7], 10))      # 3+7 and 2+3+5
```

**Output**

```text
2
```


That last one is the seed of **backtracking** (chapter 13): take-or-leave while keeping track of a running total.

---

## Common mistakes

- **Base case `[]` instead of `[""]`** for the subsequences problem. One missing bracket, and every answer disappears.
- **Forgetting the empty subsequence** (a valid plate: take nothing).
- **Mixing up substring and subsequence** in the question. Read it twice.
- **`text[1:-1]` on very short strings.** Check `len(text) <= 1` first.
- **Putting the print in the wrong place** (before vs after, chapter 8), which changes the order of the output.
- **Building strings with `+=` in a loop** when a list of characters and `"".join` would do (performance).

---

## Practice

1. 🟢 `reverse(text)` recursively. Then check your answer against `text[::-1]`.
2. 🟢 `count_char(text, ch)`: how many times does `ch` appear?
3. 🟢 `move_x_to_end("axbxc")` returns `"abcxx"`.
4. 🟡 Print every subsequence of `"abc"` in **lexicographic** (dictionary) order. *(Hint: decide "leave it" before "take it".)*
5. 🟡 Generate all **substrings** recursively.
6. 🟡 `count_subsequences(text)` without building them: how many are there? Then make it handle duplicates.
7. 🟡 Print all subsequences with their **ASCII code** sum.
8. 🔴 Return all subsequences whose characters are in **increasing** order (for `"abdc"`, drop `"dc"`).
9. 🔴 Longest common subsequence of two strings with plain recursion. How slow is it? What would you add to fix it? *(You will meet it again in chapter 25.)*

<details>
<summary>Hints</summary>

3. Recurse on the rest, then put an `x` at the end of the answer if you were an `x`, otherwise put your character in front.
6. The answer is `2 ** len(text)`; with duplicates, count distinct ones with a set (or reason combinatorially).
8. Carry the last chosen character as an extra argument; only take the next one if it is larger.
9. If the first characters match, `1 + lcs(rest_a, rest_b)`; otherwise the larger of dropping one from either. Exponential, and the same pairs repeat: memoize.
</details>

Test yourself on these ideas with [Checkpoint 4](../assignments/A4-recursion-and-strings.ipynb).

---

[← 10. Searching and Sorting with Recursion](10-searching-and-sorting-with-recursion.md) · [Handbook contents](README.md) · [12. The Choices Tree: Permutations, Codes, Keypads and Hanoi →](12-the-choices-tree.md)
