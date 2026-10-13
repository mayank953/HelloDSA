# 27. Patterns and the Interview Playbook

**Part 4: Algorithms** · Intermediate · about 11 minutes to read

> Eleven patterns that cover most questions, a checklist for the first five minutes of an interview, and a practice plan.
**In this repo:** [DSA + AI roadmap](../roadmap/README.md)  
**Run the code from this chapter:** [`code/27-patterns-and-interview-playbook.py`](code/27-patterns-and-interview-playbook.py)  

---

## You have learned the tools. Now learn to choose.

By now you have a toolbox: recursion, backtracking, arrays, linked lists, stacks, queues, hash maps, trees, heaps, graphs, sorting, binary search, dynamic programming and greedy algorithms.

A new problem rarely announces which tool it needs. The final skill is **recognition**: reading a problem and thinking *"this smells like a sliding window"* or *"this is a graph in disguise."* Experts are not smarter. They have simply seen the **shapes** enough times that they spot them quickly.

This chapter gives you a map of the shapes, a checklist for the first five minutes of any problem, and a plan for practising.

---

## The pattern map

Almost every question you will meet falls into one of these families. Learn the **tell** (what the problem looks like), the **move** (what you do), and the **cost**.

| # | Pattern | The tell | The move | Typical cost | Chapter |
|---|---|---|---|---|---|
| 1 | **Two pointers** | Sorted list; pairs; "from both ends"; in-place compaction | Two indexes closing in or chasing | O(n) | 14 |
| 2 | **Sliding window** | "Longest / shortest / best **contiguous** stretch" with a rule | Grow the right edge, shrink the left | O(n) | 14 |
| 3 | **Fast and slow pointers** | Linked list; "middle"; "cycle" | Two runners at different speeds | O(n) | 15 |
| 4 | **Prefix sums (+ hash map)** | Many range-sum queries; "sub-list with sum k" | Running total; remember earlier totals | O(n) | 14, 18 |
| 5 | **Hash map / set** | "Seen before?", counts, find the partner, group by a signature | Trade O(n) memory for O(1) lookups | O(n) | 18 |
| 6 | **Monotonic stack** | "Next greater / smaller", spans, histogram | Pop items made irrelevant by the newcomer | O(n) | 16 |
| 7 | **BFS** | Fewest steps, level by level, shortest path (unweighted) | Queue + visited set | O(V + E) | 17, 22 |
| 8 | **DFS / backtracking** | "All ways", "does a path exist", constraints, grids | Choose, explore, un-choose | exponential, pruned | 13, 22 |
| 9 | **Binary search (on the answer)** | Sorted data, or a monotone yes/no over a range of answers | Halve the range with a check function | O(log n) × check | 24 |
| 10 | **Heap / top-k** | "k largest / smallest / most frequent", merge sorted streams, running median | Heap of size k | O(n log k) | 21 |
| 11 | **Dynamic programming** | "Number of ways", "min / max cost", overlapping subproblems | State, recurrence, table | states × work | 25 |
| 12 | **Greedy / intervals** | Scheduling, merging intervals, "best local choice is safe" | Sort, then one pass (and test the idea!) | O(n log n) | 26 |
| 13 | **Tree recursion** | Anything on a tree | Base case `None`; combine the left and right answers | O(n) | 19, 20 |
| 14 | **Union-Find / topological order** | Groups that merge; dependencies | Disjoint sets; in-degree queue | ~O(E) | 22 |

> **Tip.** Many problems combine two patterns: a *sliding window with a hash map*, a *BFS with a heap* (that is Dijkstra), *binary search with a greedy check*. Name each ingredient out loud.

---

## The first five minutes: the playbook

Whether you are in an interview or alone with a hard problem, **do not start coding.** Follow these steps. They are the Hello DSA Method from chapter 1, tuned for the clock.

### 1. Understand (1 minute)

- **Restate the problem** in your own words.
- Ask about **inputs**: size? values (negative? duplicates? zero)? sorted? can it be empty?
- Ask about **outputs**: return an index? a count? all the answers? what if there is no answer?

### 2. Examples (1 minute)

Draw **two or three tiny examples**, including an edge case. Solve one by hand and notice what *you* did. That is usually the algorithm.

### 3. Brute force (1 minute)

State the simplest correct solution **and its cost**, even if it is slow. This shows you can solve the problem, and gives you a baseline and a test oracle.

### 4. Look at the constraints

The size of the input tells you how much work is allowed. This is the fastest way to pick a pattern:

| If `n` is about | The solution can cost about |
|---|---|
| up to 10 | `n!`: backtracking over permutations |
| up to 20 to 25 | `2ⁿ`: subsets, bitmasks |
| up to 500 | `n³` |
| up to 5,000 to 10,000 | `n²`: nested loops, 2D DP |
| up to 1,000,000 | `n log n`: sort, heap, binary search, divide and conquer |
| 10,000,000 or more | `n` or `log n`: one pass, hash map, math |

```python
def target_complexity(n):
    """A rule of thumb: the slowest running time that is still comfortable for input size n."""
    if n <= 10:
        return "O(n!)"
    if n <= 25:
        return "O(2^n)"
    if n <= 500:
        return "O(n^3)"
    if n <= 10_000:
        return "O(n^2)"
    if n <= 1_000_000:
        return "O(n log n)"
    return "O(n) or O(log n)"

for n in [8, 20, 300, 5_000, 200_000, 10_000_000]:
    print(f"n up to {n:>10,}: aim for {target_complexity(n)}")
```

**Output**

```text
n up to          8: aim for O(n!)
n up to         20: aim for O(2^n)
n up to        300: aim for O(n^3)
n up to      5,000: aim for O(n^2)
n up to    200,000: aim for O(n log n)
n up to 10,000,000: aim for O(n) or O(log n)
```


### 5. Optimise: find the pattern (3 minutes)

Ask the pattern questions *in order*:

1. **Is it sorted** (or can I sort it)? Two pointers, binary search, greedy.
2. Does it ask about a **contiguous stretch**? Sliding window, prefix sums, Kadane.
3. Does it need **fast lookup or counting**? Hash map or set.
4. Is it about **"next greater" or nesting**? Stack.
5. Is it a **tree or a graph**? Recursion, BFS or DFS.
6. Does it say **"all ways" or "generate"**? Backtracking.
7. Does it say **"number of ways", "minimum / maximum cost"** with overlapping subproblems? DP.
8. Is there a **monotone yes/no over a range** ("smallest X such that...")? Binary search on the answer.
9. Is it **top-k or merging streams**? Heap.

### 6. Code (carefully)

- Write clear names: `left`, `right`, `window_sum`, `small_answer`.
- Do the **base case first**, as in every recursion.
- Narrate: *"This handles the empty case; here I move the left pointer because the window is invalid..."*

### 7. Verify

- **Trace your example** by hand, line by line.
- Test the **edge cases**: empty, one item, all equal, already sorted, reversed, duplicates, negatives, the largest input.
- Fix bugs by *reading*, not by random edits.

### 8. Analyse

State **time and space** (chapters 3 and 4), then say what could be improved. Interviewers listen for *"the recursion depth adds O(h) space"*.

---

## From brute force to optimal: a worked example

Let us practise "start slow, then improve" on the maximum-subarray problem from chapter 14 (the largest sum of a contiguous stretch). We will write three solutions and **count the steps** of each:

```python
def max_subarray_cubic(items):
    steps, best = 0, items[0]
    for start in range(len(items)):
        for end in range(start, len(items)):
            total = 0
            for k in range(start, end + 1):          # re-add the whole stretch each time
                total += items[k]
                steps += 1
            best = max(best, total)
    return best, steps

def max_subarray_quadratic(items):
    steps, best = 0, items[0]
    for start in range(len(items)):
        total = 0
        for end in range(start, len(items)):         # extend the previous total by one item
            total += items[end]
            steps += 1
            best = max(best, total)
    return best, steps

def max_subarray_linear(items):
    steps, best, current = 0, items[0], items[0]
    for value in items[1:]:
        current = max(value, current + value)        # Kadane: drop a stretch that hurts
        best = max(best, current)
        steps += 1
    return best, steps

data = [(i * 37) % 19 - 9 for i in range(120)]       # a reproducible mix of negatives and positives
for solve in (max_subarray_cubic, max_subarray_quadratic, max_subarray_linear):
    answer, steps = solve(data)
    print(f"{solve.__name__:<24} answer {answer:>3}   steps {steps:>9,}")
```

**Output**

```text
max_subarray_cubic       answer  45   steps   295,240
max_subarray_quadratic   answer  45   steps     7,260
max_subarray_linear      answer  45   steps       119
```

Same answer, three orders of magnitude apart. And notice how each improvement came from *one question*:

1. **Cubic → quadratic:** *"Am I recomputing a sum I already know?"* (Reuse the running total, as in prefix sums.)
2. **Quadratic → linear:** *"Do I need every start, or can I decide locally whether to keep the current stretch?"* (A DP/greedy insight: drop a negative running total.)


**Always keep the brute force.** It is a **test oracle**: run your clever solution and the slow one on thousands of random small inputs, and compare. That is how we checked every algorithm in this handbook:

```python
import random
rng = random.Random(27)
for _ in range(500):
    small = [rng.randint(-9, 9) for _ in range(rng.randint(1, 12))]
    assert max_subarray_linear(small)[0] == max_subarray_cubic(small)[0]
print("the fast solution agrees with the brute force on 500 random inputs")
```

**Output**

```text
the fast solution agrees with the brute force on 500 random inputs
```

---

## Pattern drills: name the pattern

Cover the answers and decide. For each, name the pattern and give one sentence of approach.

1. *Given a sorted list and a target, return the pair that adds up to it.*
2. *Longest substring with at most two distinct characters.*
3. *Does this linked list contain a loop?*
4. *Count the sub-lists whose elements add up to `k`.*
5. *For each day, how many days until a warmer temperature?*
6. *Fewest moves for a knight to reach a square on a chessboard.*
7. *List every valid arrangement of `n` pairs of brackets.*
8. *Smallest capacity that lets a ship deliver all packages in `d` days.*
9. *The 10 most common words in a huge file.*
10. *The number of ways to make a total with given coins.*
11. *Schedule the most non-overlapping meetings.*
12. *Are two people in the same friend group?* (friendships arrive over time)

<details>
<summary>Answers</summary>

1. **Two pointers** from both ends.
2. **Sliding window** with a count dictionary.
3. **Fast and slow pointers** (Floyd).
4. **Prefix sums + hash map**.
5. **Monotonic stack** (next greater element).
6. **BFS** on the board (unweighted shortest path).
7. **Backtracking** with pruning (`opened < n`, `closed < opened`).
8. **Binary search on the answer** with a greedy feasibility check.
9. **Hash map (Counter) + heap** of size 10.
10. **Dynamic programming** (unbounded knapsack / coin change, count version).
11. **Greedy**: sort by end time.
12. **Union-Find**.
</details>

---

## Everything on one page: costs of the structures

| Structure | Access by index | Search | Insert | Delete | Notes |
|---|---|---|---|---|---|
| **Array / list** | **O(1)** | O(n) | O(1) end, O(n) elsewhere | O(1) end, O(n) elsewhere | Compact, cache-friendly |
| **Linked list** | O(n) | O(n) | O(1) at head (or at a known node) | O(1) at a known node | No shifting |
| **Stack** | n/a | n/a | O(1) push | O(1) pop | LIFO |
| **Queue / deque** | n/a | n/a | O(1) | O(1) | FIFO |
| **Hash map / set** | n/a | **O(1)** avg | O(1) avg | O(1) avg | Unordered (insertion-ordered in Python) |
| **BST (unbalanced)** | n/a | O(h) | O(h) | O(h) | h from log n to n |
| **Balanced BST (AVL)** | n/a | **O(log n)** | O(log n) | O(log n) | Keeps order |
| **Heap** | n/a | O(n) | O(log n) | O(log n) (min) | O(1) peek at the min |
| **Graph (adjacency list)** | n/a | O(V + E) traversal | O(1) add edge | O(degree) | Space O(V + E) |

And the algorithms:

| Algorithm | Time | Space |
|---|---|---|
| Linear search | O(n) | O(1) |
| Binary search | O(log n) | O(1) iterative |
| Merge sort | O(n log n) | O(n) |
| Quick sort | O(n log n) avg, O(n²) worst | O(log n) |
| Heap sort | O(n log n) | O(1) |
| BFS / DFS | O(V + E) | O(V) |
| Dijkstra (heap) | O((V + E) log V) | O(V) |
| Naive Fibonacci / subsets | O(2ⁿ) | O(n) stack |
| Permutations | O(n · n!) | O(n) stack |
| DP (typical) | states × work per state | states (often reducible) |

---

## Practising well: the plan

### The shape of a good week

| Day | What to do |
|---|---|
| 1 to 3 | **Learn** one topic from this handbook; run and change the code |
| 4 to 5 | **Solve 4 to 6 problems** on that topic, time-boxed to **25 minutes each** |
| 6 | **Review** every problem you could not finish: read a solution, then close it and **re-code from memory** |
| 7 | **Revise** an older topic with 2 or 3 problems, without notes |

### A suggested order (twelve weeks)

| Weeks | Topic | Problems to aim for |
|---|---|---|
| 1 | Arrays, strings, hash maps | 12 |
| 2 | Two pointers, sliding window, prefix sums | 12 |
| 3 | Stacks, queues, monotonic stack | 10 |
| 4 | Linked lists | 10 |
| 5 to 6 | **Recursion and backtracking** | 15 |
| 7 | Binary search (including on the answer) | 10 |
| 8 | Trees and BSTs | 12 |
| 9 | Heaps and sorting | 8 |
| 10 | Graphs: BFS, DFS, topological sort, Union-Find | 12 |
| 11 to 12 | **Dynamic programming**, then greedy | 15 + 6 |

Do not rush: *a problem you understand deeply is worth five you copied.*

### How to review a problem (use this table)

Keep an **error log**. After every problem you struggle with, write one line:

| Problem | Pattern | Where I got stuck | The insight | Redo on |
|---|---|---|---|---|
| Next greater element | Monotonic stack | Did not see why `while` is still O(n) | Each item is pushed and popped once | next Sunday |

Review the log once a week. After a month it shows exactly which pattern you keep missing.

### Habits of people who improve fast

- **Time-box**, then read a hint, not the whole solution. Struggle with a purpose for 25 to 30 minutes first.
- **Explain aloud** (to a friend, a rubber duck, or a recording). If you cannot explain it simply, you have not understood it.
- **Re-derive, do not memorise.** If you can rebuild merge sort from the police story, you do not need to cram its code.
- **Vary the problems.** Doing 30 sliding-window questions in a row teaches you less than 10 mixed ones, where you must *identify* the pattern.
- **Draw.** Trees, stacks, pointers and DP tables. Always.

---

## In the interview room

- **Think aloud.** The interviewer is assessing how you reason; silence hides it.
- **Clarify before coding.** Two good questions beat ten minutes of wrong code.
- **Start with the brute force**, state its cost, *then* improve it. It is fine to say, *"I will begin simple and optimise."*
- **Test with your own example** before saying "done". Interviewers love candidates who find their own bug.
- **When stuck:** go back to a tiny example, try a different pattern, or ask for a hint. Asking is not failing.
- **Be honest** about what you do not know. "I would look up the exact syntax, but the idea is..." is a fine answer.

---

## Common mistakes

- **Jumping straight into code** without examples or a plan.
- **Optimising too early**, before you have any correct solution.
- **Forgetting edge cases:** empty, single, duplicates, negatives, huge input.
- **Memorising solutions** instead of patterns.
- **Never revisiting** problems you got wrong.
- **Ignoring complexity analysis** at the end.

---

## Where to go next

- Work through the four auto-checked **[checkpoint assignments](../assignments/README.md)** and the extra **handbook practice sets** there.
- Re-watch the **video** and compare its explanations with these chapters; each chapter lists the matching timestamps.
- Follow the **[DSA + AI roadmap](../roadmap/README.md)** for the order of what to learn after this.
- Share what you build with **#HelloDSA**.

---

[← 26. Greedy Algorithms](26-greedy.md) · [Handbook contents](README.md) · [28. DSA Behind AI →](28-dsa-behind-ai.md)
