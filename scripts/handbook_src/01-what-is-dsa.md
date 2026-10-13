## Before we start: why are you even learning this?

You will hear this question a hundred times: *"AI writes code now. Why should I study DSA?"*

Here is the honest answer. AI can write ninety percent of a program and get it right. The remaining ten percent is the part that decides whether you are useful: somebody has to **read that code, understand it, find why it is slow or wrong, and fix it**. That "somebody" needs to think in terms of *how data is stored* and *how many steps a solution takes*. That is exactly what DSA trains.

DSA is also the one topic that every big product company still tests in its first two interview rounds. Not because they love puzzles, but because DSA is the cleanest way to see **how you think when the problem is new**.

So the goal of this handbook is not to make you memorise a hundred solutions. It is to make you **understand things so well that new problems stop being scary**.

> **Promise for the whole handbook.** We never run after the answer. We build the *intuition* first (a story, a picture), then the idea, then the code. If the code is the only thing you remember, you will forget it in two months. If the story is what you remember, you can rebuild the code in two minutes.

---

## Data, structure, and the two words together

Break the term in two:

- **Data** is anything that is information. The video you are watching is data. The code you write is data. Your marks, your contacts, your photos: all data.
- **Structure** is *how you arrange it* so that you can use it well.

Put them together and you get a **data structure**: a way of **storing and arranging data so that the operations you care about are easy and fast**.

### A story: three ways to keep your friends' phone numbers

Imagine you want to store the phone numbers of 1,000 friends.

1. **A loose pile of sticky notes.** Adding a new friend is instant (drop one more note). Finding "Rahul" means going through the pile, one note at a time.
2. **A diary sorted alphabetically.** Finding "Rahul" is fast (jump to the R pages). But adding a new friend means making space in the middle of the diary.
3. **A diary with an index at the back** ("Rahul → page 41"). Finding is almost instant. Adding means updating the index too.

Same data. Three structures. Three different trade-offs. **There is no "best" data structure; there is only the best one for the operations you do most.** That one sentence is the heart of DSA.

Python gives you these structures ready-made. Look at how they behave on the same job: *"is this name in my collection?"*

```python
names_list = ["Asha", "Ravi", "Meera", "Karan", "Zoya"]      # a list: sticky notes in a pile
names_set = {"Asha", "Ravi", "Meera", "Karan", "Zoya"}        # a set: the indexed diary

print("Karan" in names_list)   # Python checks the notes one by one until it finds Karan
print("Karan" in names_set)    # Python jumps straight to the right place
print("Nobody" in names_list)  # to say 'no', the list has to read every single note
```

On five names you cannot feel any difference. Let us **count the work** instead of timing it (counting is exact; timing changes with your laptop):

```python
def steps_to_find_in_list(items, target):
    """How many items do we look at before we can answer?"""
    steps = 0
    for item in items:
        steps += 1
        if item == target:
            break
    return steps

friends = [f"friend{i}" for i in range(1_000_000)]

print("first friend:", steps_to_find_in_list(friends, "friend0"))
print("last friend :", steps_to_find_in_list(friends, "friend999999"))
print("not a friend:", steps_to_find_in_list(friends, "stranger"))
```

A set (or a dictionary) needs a handful of steps for *every* one of those questions, no matter how many friends you have. That is the difference between an app that feels instant and one that freezes.

```python hide
assert steps_to_find_in_list(friends, "friend0") == 1
assert steps_to_find_in_list(friends, "friend999999") == 1_000_000
assert steps_to_find_in_list(friends, "stranger") == 1_000_000
```

---

## What is an algorithm?

An **algorithm** is a *step-by-step set of instructions* that solves a problem. A recipe is an algorithm. Directions to a friend's house are an algorithm. Nothing scary.

Two things make an algorithm good:

1. It is **correct** for every valid input (including the strange ones: empty, one item, duplicates).
2. It is **efficient**: it does not waste time or memory.

Same problem, two algorithms. *"Find 7,654,321 in a sorted list of ten million numbers."*

- **Algorithm A (linear scan):** start at the first number and check each one. Worst case, ten million checks.
- **Algorithm B (binary search):** open the list in the middle. If the middle number is too big, throw away the right half. Repeat. Each step halves what is left.

```python
def linear_checks(sorted_numbers, target):
    checks = 0
    for value in sorted_numbers:
        checks += 1
        if value == target:
            return checks
    return checks

def binary_checks(sorted_numbers, target):
    low, high, checks = 0, len(sorted_numbers) - 1, 0
    while low <= high:
        mid = (low + high) // 2
        checks += 1
        if sorted_numbers[mid] == target:
            return checks
        if sorted_numbers[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return checks

numbers = list(range(10_000_000))
print("linear scan :", linear_checks(numbers, 7_654_321), "checks")
print("binary search:", binary_checks(numbers, 7_654_321), "checks")
```

Millions of checks against roughly twenty. Same answer, completely different cost. That is why we **study algorithms**: not to show off, but because the difference between a good and a bad one is the difference between a second and a month.

```python hide
assert linear_checks(numbers, 7_654_321) == 7_654_322
assert 15 <= binary_checks(numbers, 7_654_321) <= 24
```

### Structures and algorithms are a pair

Algorithms work *on* data structures, and each structure has its own rules. A tuple can never "append". A list can. So an algorithm written for a tuple will never say "append"; it will say "make a new one". A set has no order, so no algorithm on a set will say "give me the third item".

> When you learn a new data structure, ask three questions: **What can I do with it? How fast is each thing? What can I *not* do?**

---

## The Hello DSA Method

Most people get stuck on a new question because they stare at it and wait for the answer to appear. Do this instead. Use the same steps, every time, on every problem in this handbook:

| Step | What you do | The question to ask yourself |
|---|---|---|
| **1. Understand** | Read the question twice. Say it in your own words. | *What goes in? What must come out?* |
| **2. Play with examples** | Solve 2 or 3 tiny inputs by hand, including an empty or one-item input. | *What did I actually do on paper?* |
| **3. Find the smaller problem** | Look for the **same problem on a smaller input**. | *If somebody handed me the answer for a smaller input, could I finish the job?* |
| **4. Assume it works** | Trust that the smaller problem is already solved. Do **not** dive inside it. | *What is the one thing I still have to do myself?* |
| **5. Do your part** | Combine the smaller answer with your own small step. | *How do I glue the two together?* |
| **6. Base case and edge cases** | Decide where it stops. Test empty, one item, duplicates, negatives. | *When does the problem become too small to shrink?* |
| **7. Trace and draw** | Draw the tree or the memory by hand for a tiny input. | *Does the picture match the code?* |
| **8. Measure** | Work out the time and the memory. | *What happens if the input is a million times larger?* |

Steps 3 to 5 are the *thinking* part. Steps 6 and 7 are how you *check yourself*. Step 8 is what separates a working solution from a good one.

You will see this method used on every worked problem from chapter 5 onwards.

```python
# Tiny practice: the method on a very small problem.
# Problem: "sum all numbers in a list".
#
# Step 2 (examples):   [] -> 0     [4] -> 4     [4, 1, 7] -> 12
# Step 3 (smaller):    the sum of [4, 1, 7] = 4 + (the sum of [1, 7])
# Step 4 (assume):     somebody hands me the sum of [1, 7] = 8
# Step 5 (my part):    add my own 4 to it -> 12
# Step 6 (base case):  the sum of an empty list is 0
def total(numbers):
    if len(numbers) == 0:
        return 0
    return numbers[0] + total(numbers[1:])

print(total([4, 1, 7]))
```

Do not worry if you do not yet see *why* that works. We spend chapters 5 to 13 on exactly that idea. Notice only how each comment lines up with a step in the table.

```python hide
assert total([]) == 0 and total([4]) == 4 and total([4, 1, 7]) == 12
```

---

## How to study with this handbook

1. **Read the story first.** Picture it.
2. **Run every code block yourself.** Change a number. Break it. Fix it.
3. **Draw the trees and the memory on paper.** Every time. For the first fifteen or twenty questions, do not skip this. Drawing is not a beginner's crutch; it is the skill.
4. **Close the page and redo the problem from a blank file.** If you cannot, you understood the answer but not the idea. Read the story again.
5. **Do the practice problems** at the end of each chapter, then the auto-checked [checkpoint assignments](../assignments/README.md).
6. **Come back a week later** and redo one problem without help. That is when it sticks.

> If a chapter feels hard, that is normal. Recursion, trees and dynamic programming are *the* topics where most people give up. That is why they get the most pages here.

---

## What this handbook covers

| Part | Chapters | You will be able to |
|---|---|---|
| **1. Foundations** | 1 to 4 | Think in terms of structures, count time and memory |
| **2. Recursion** | 5 to 13 | Solve problems by trusting smaller versions of themselves, up to backtracking |
| **3. Data structures** | 14 to 22 | Use arrays, linked lists, stacks, queues, hashmaps, trees, heaps and graphs |
| **4. Algorithms** | 23 to 27 | Sort, search, use dynamic programming and greedy ideas, and recognise patterns |
| **5. DSA in the AI era** | 28 | See where these ideas show up inside AI systems |

---

## Practice

1. 🟢 In your own words, why is "the best data structure" the wrong question? What should you ask instead?
2. 🟢 You have 50 million product names and users search by exact name all day. Would you store them in a list or a set? Why?
3. 🟢 Write down, as plain steps, the algorithm you use to find a word in a dictionary. Is it closer to linear scan or to binary search?
4. 🟡 Modify `binary_checks` so that it returns the number of checks for a target that is **not** in the list. What is the largest number of checks you ever see for ten million numbers?
5. 🟡 Apply the Hello DSA Method (steps 1 to 6) to "find the largest number in a list". Which smaller problem did you find?

<details>
<summary>Hints</summary>

1. There is no universal winner. Ask: which operations will I do most (search, insert, delete, order)?
2. A set or dictionary. Lookup by exact value does not slow down as the collection grows.
3. Binary search: you open the middle and discard half. A person flipping page by page would be a linear scan.
4. Around 24 for ten million, because 2 to the power 24 is about sixteen million. Halving can only happen about log base 2 of n times.
5. The largest of `[a, b, c, d]` is the larger of `a` and the largest of `[b, c, d]`.
</details>

