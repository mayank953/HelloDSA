## Walking through a maze

You enter a maze. At every junction you pick a corridor and walk. Sometimes it leads to the exit. Often it leads to a **dead end**. What do you do at a dead end? You do not give up. You **walk back to the last junction and try a different corridor.**

That is **backtracking**: *try a choice, explore everything that follows from it, and if it does not work out (or even if it does), undo the choice and try the next one.*

Chapters 11 and 12 already did this, quietly. When we wrote `explore(rest, plate + chosen)`, the *old* `plate` was untouched after the call returned, because we built a **new** string for each branch. The "undo" happened for free.

Backtracking is what you do when you want **one shared piece of state** (a single list, a single board) instead of copying at every step. It is faster and uses less memory, but now **you** must undo each choice. That discipline is the whole technique.

> **The three beats of backtracking:** **choose**, **explore**, **un-choose**.

---

## The template

```text
def explore(state):
    if state is a complete answer:
        record it
        return
    for each choice available right now:
        if the choice is allowed:            <- pruning: skip hopeless choices early
            make the choice                  (CHOOSE)
            explore(the new state)           (EXPLORE)
            undo the choice                  (UN-CHOOSE)
```

It is the same recursion recipe: base case (complete answer), assume (the call explores everything that follows), my part (make *one* choice, then undo it).

---

## Warm-up: subsets with one shared list

We already generated subsets by take-or-leave. Here is the backtracking version with a **single** list called `path` that every call shares:

```python
def subsets(items):
    answers, path = [], []

    def explore(i):
        if i == len(items):
            answers.append(path[:])      # record a COPY of the current path
            return
        path.append(items[i])            # CHOOSE: take items[i]
        explore(i + 1)                   # EXPLORE everything that follows
        path.pop()                       # UN-CHOOSE: put it back
        explore(i + 1)                   # the other branch: leave items[i] out

    explore(0)
    return answers

print(subsets([1, 2, 3]))
```

Two details deserve your full attention.

**1. The copy.** `answers.append(path[:])` stores a *copy*. If you write `answers.append(path)`, you store the **same list** again and again. Because `path` keeps changing (and ends up empty at the end), every stored answer ends up looking identical:

```python
def subsets_bug(items):
    answers, path = [], []

    def explore(i):
        if i == len(items):
            answers.append(path)         # BUG: not a copy. All answers are the same list object.
            return
        path.append(items[i]); explore(i + 1); path.pop()
        explore(i + 1)

    explore(0)
    return answers

print(subsets_bug([1, 2, 3]))
```

The famous "why is my answer full of empty lists?" bug. Remember chapter 2: *a list is a label on one object.*

**2. The undo.** `path.pop()` is the un-choose. If you forget it, `path` keeps growing and every later branch starts from a dirty state.

```python hide
assert len(subsets([1, 2, 3])) == 8 and [] in subsets([1, 2, 3]) and [1, 2, 3] in subsets([1, 2, 3])
assert subsets_bug([1, 2, 3]) == [[]] * 8
```

---

## Problem 1: combinations that add up to a target

**Question.** Given distinct positive numbers `candidates`, find **every combination** that sums to `target`. Each number may be used **any number of times**. Example: `candidates = [2, 3, 6, 7]`, `target = 7` gives `[2, 2, 3]` and `[7]`.

**Choice.** At each step, which candidate do I add next?

**Avoiding duplicates.** If we allowed any candidate at any step we would get `[2, 2, 3]`, `[2, 3, 2]` and `[3, 2, 2]`, which are the same combination in different orders. To avoid that, **only look at candidates from the current position onward** (never go back to a smaller index).

**Pruning.** If a candidate is already **larger than what is left**, adding it overshoots the target. If we sort the candidates, every candidate *after* it is even bigger, so we can **stop the loop**.

```python
def combination_sum(candidates, target):
    candidates = sorted(candidates)
    answers, path = [], []

    def explore(start, remaining):
        if remaining == 0:                          # complete answer: the path sums to target
            answers.append(path[:])
            return
        for i in range(start, len(candidates)):
            number = candidates[i]
            if number > remaining:                  # PRUNE: this and every later number overshoot
                break
            path.append(number)                     # CHOOSE
            explore(i, remaining - number)          # EXPLORE (i, not i+1: a number may be reused)
            path.pop()                              # UN-CHOOSE

    explore(0, target)
    return answers

print(combination_sum([2, 3, 6, 7], 7))
print(combination_sum([2, 3, 5], 8))
```

```python hide
assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
assert combination_sum([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
assert combination_sum([2], 1) == []
```

### How much does pruning save?

Pruning is not a small optimisation. Let us count the number of recursive calls with and without the cut-off:

```python
def count_calls(candidates, target, prune):
    candidates = sorted(candidates)
    calls = 0

    def explore(start, remaining):
        nonlocal calls
        calls += 1
        if remaining <= 0:
            return
        for i in range(start, len(candidates)):
            if prune and candidates[i] > remaining:
                break
            explore(i, remaining - candidates[i])

    explore(0, target)
    return calls

for target in [10, 20, 30]:
    print(f"target {target:>2}: without pruning {count_calls([2, 3, 6, 7, 8, 9], target, False):>7,} calls, with pruning {count_calls([2, 3, 6, 7, 8, 9], target, True):>6,}")
```

The gap grows with the target. Good pruning is the difference between a backtracking solution that finishes and one that does not.

---

## Problem 2: balanced brackets (generate parentheses)

**Question.** List every valid string made of `n` pairs of `()`. For `n = 3`: `((()))`, `(()())`, `(())()`, `()(())`, `()()()`.

**Choices.** At each position put `(` or `)`. Not every choice is allowed:

- You may add `(` only while you have **used fewer than `n`** open brackets.
- You may add `)` only if there is an **open bracket still waiting** to be closed (`closed < opened`).

Those two rules are **the pruning**: they stop the recursion from ever building an invalid prefix, so we never waste time on it.

```python
def generate_parentheses(n):
    answers = []

    def explore(current, opened, closed):
        if len(current) == 2 * n:
            answers.append(current)
            return
        if opened < n:
            explore(current + "(", opened + 1, closed)      # choose "("
        if closed < opened:
            explore(current + ")", opened, closed + 1)      # choose ")"

    explore("", 0, 0)
    return answers

print(generate_parentheses(3))
print([len(generate_parentheses(n)) for n in range(1, 9)])
```

(Here we built a fresh string each time, so no explicit undo was needed. It is still the same idea: *choice, explore.*)

The counts `1, 2, 5, 14, 42, 132, ...` are the famous **Catalan numbers**. They count balanced brackets, binary trees with `n` nodes, and many other things. You will meet them again in chapter 19.

```python hide
assert generate_parentheses(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
assert [len(generate_parentheses(n)) for n in range(1, 9)] == [1, 2, 5, 14, 42, 132, 429, 1430]
```

---

## Problem 3: N-Queens

**Question.** Place `n` queens on an `n × n` chessboard so that **no two attack each other**. A queen attacks along her row, her column and both diagonals.

**Choices.** Put exactly one queen in each **row**, top to bottom. For the current row, *which column?* That alone removes the row conflict: we only need to check **columns and diagonals**.

**Tracking attacks in O(1).** Two cells share a *↘ diagonal* when `row − col` is equal, and a *↙ diagonal* when `row + col` is equal. So we keep three sets: used columns, used `row − col` values, used `row + col` values.

**Prune.** If a column or diagonal is taken, do not even try that cell.

```python
def solve_n_queens(n):
    solutions, placement = [], []              # placement[row] = column of the queen in that row
    used_cols, diag_down, diag_up = set(), set(), set()

    def place(row):
        if row == n:                           # every row has a queen: a complete answer
            solutions.append(placement[:])
            return
        for col in range(n):
            if col in used_cols or (row - col) in diag_down or (row + col) in diag_up:
                continue                       # PRUNE: this cell is attacked
            used_cols.add(col); diag_down.add(row - col); diag_up.add(row + col)   # CHOOSE
            placement.append(col)
            place(row + 1)                                                          # EXPLORE
            placement.pop()                                                         # UN-CHOOSE
            used_cols.remove(col); diag_down.remove(row - col); diag_up.remove(row + col)

    place(0)
    return solutions

print([len(solve_n_queens(n)) for n in range(1, 9)])
```

Eight queens has 92 solutions. Let us see one for six queens (`Q` is a queen):

```python
def draw(placement):
    n = len(placement)
    return "\n".join("".join("Q " if placement[r] == c else ". " for c in range(n)) for r in range(n))

print(draw(solve_n_queens(6)[0]))
```

```python hide
assert [len(solve_n_queens(n)) for n in range(1, 9)] == [1, 0, 0, 2, 10, 4, 40, 92]
# every solution really is conflict-free
for sol in solve_n_queens(7):
    for r1 in range(7):
        for r2 in range(r1 + 1, 7):
            assert sol[r1] != sol[r2] and abs(sol[r1] - sol[r2]) != r2 - r1
```

### Why backtracking, and how much does it save?

A blind search would try every way of putting one queen in each row: `nⁿ` placements. For `n = 8` that is **16,777,216**. With pruning, how many rows-and-columns do we *actually* visit?

```python
def nodes_visited(n):
    visited = 0
    placement, used_cols, diag_down, diag_up = [], set(), set(), set()

    def place(row):
        nonlocal visited
        visited += 1
        if row == n:
            return
        for col in range(n):
            if col in used_cols or (row - col) in diag_down or (row + col) in diag_up:
                continue
            used_cols.add(col); diag_down.add(row - col); diag_up.add(row + col)
            place(row + 1)
            used_cols.remove(col); diag_down.remove(row - col); diag_up.remove(row + col)

    place(0)
    return visited

for n in [4, 6, 8]:
    print(f"n={n}: blind search ~ {n ** n:>10,} placements, backtracking visited {nodes_visited(n):>6,} partial boards")
```

The vast majority of the search space is **cut off** the moment two queens clash. This is why the technique has a place in your toolbox despite its exponential worst case.

---

## Problem 4: all paths through a maze

A grid of `0` (open) and `1` (wall). Find every route from the top-left to the bottom-right, moving up, down, left or right, **never stepping on the same cell twice in one route**.

**Choices.** The four directions. **Prune.** Walls, cells outside the grid, cells already on the current path.

**The un-choose matters twice here.** When we leave a cell we must **remove it from the current path** *and* mark it **unvisited** again, so other routes may use it. This is the clearest illustration of why undoing is essential.

```python
def all_paths(grid):
    rows, cols = len(grid), len(grid[0])
    paths, path, on_path = [], [], set()

    def explore(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] == 1 or (r, c) in on_path:
            return                                       # PRUNE: off the grid, a wall, or already used
        path.append((r, c)); on_path.add((r, c))         # CHOOSE: step onto this cell
        if (r, c) == (rows - 1, cols - 1):
            paths.append(path[:])                        # reached the exit: record a copy
        else:
            for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                explore(r + dr, c + dc)                  # EXPLORE
        path.pop(); on_path.remove((r, c))               # UN-CHOOSE: step back off this cell

    explore(0, 0)
    return paths

maze = [[0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]]
for route in all_paths(maze):
    print(route)
```

```python hide
assert len(all_paths(maze)) == 2
assert all_paths([[0]]) == [[(0, 0)]] and all_paths([[0, 1], [1, 0]]) == []
open_grid = [[0] * 4 for _ in range(4)]
assert len(all_paths(open_grid)) == 184      # self-avoiding paths corner to corner on a 4x4 grid of cells
```

(Without the `on_path` rule the search would wander in circles forever. In graphs this same idea becomes `visited`, chapter 22.)

---

## Problem 5: finding a word in a letter grid

**Question.** Does `word` appear in a grid of letters, built from adjacent cells (up, down, left, right), using each cell at most once? This is the classic *Word Search* puzzle.

**The neat trick for "visited".** Instead of a separate set, **temporarily overwrite the cell** with `"#"` while we are exploring from it, then **put the letter back**. This is un-choose, written in one line.

```python
def word_exists(board, word):
    rows, cols = len(board), len(board[0])

    def explore(r, c, k):                               # have we matched word[:k] so far?
        if k == len(word):
            return True                                 # every letter matched
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[k]:
            return False                                # PRUNE: wrong letter or off the grid
        saved = board[r][c]
        board[r][c] = "#"                               # CHOOSE: mark this cell as used
        found = any(explore(r + dr, c + dc, k + 1)
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)])
        board[r][c] = saved                             # UN-CHOOSE: restore the letter
        return found

    return any(explore(r, c, 0) for r in range(rows) for c in range(cols))

board = [list("ABCE"),
         list("SFCS"),
         list("ADEE")]
print(word_exists(board, "ABCCED"), word_exists(board, "SEE"), word_exists(board, "ABCB"))
print("board unchanged afterwards:", board == [list("ABCE"), list("SFCS"), list("ADEE")])
```

```python hide
assert word_exists(board, "ABCCED") and word_exists(board, "SEE") and not word_exists(board, "ABCB")
assert board == [list("ABCE"), list("SFCS"), list("ADEE")]
```

The last line proves we undid every mark.

---

## Permutations again: the shared-state version

Chapter 12 built a new string for each branch. With backtracking we keep **one** `path` and a `used` flag per item, which avoids creating strings:

```python
def permutations_backtracking(items):
    answers, path = [], []
    used = [False] * len(items)

    def explore():
        if len(path) == len(items):
            answers.append(path[:])
            return
        for i in range(len(items)):
            if used[i]:
                continue                         # this item is already on the path
            used[i] = True; path.append(items[i])      # CHOOSE
            explore()                                  # EXPLORE
            path.pop(); used[i] = False                # UN-CHOOSE

    explore()
    return answers

print(permutations_backtracking([1, 2, 3]))
```

```python hide
from itertools import permutations as _p
assert sorted(permutations_backtracking([1, 2, 3, 4])) == sorted([list(p) for p in _p([1, 2, 3, 4])])
```

---

## When to use backtracking

Reach for it when the question says:

- *"Find **all** ways to..."* (all subsets, all paths, all arrangements)
- *"Place things so that **no rule is broken**"* (N-Queens, Sudoku)
- *"Is there **at least one** way to...?"* (word search, solving a puzzle)

And remember how it relates to its neighbours:

| Technique | Core idea | Use when |
|---|---|---|
| **Brute force** | Try everything, no cleverness | Tiny inputs |
| **Backtracking** | Try choices, **prune** hopeless branches, undo | Constraints let you cut branches early |
| **Dynamic programming** | Same subproblems repeat: **remember** answers | You only need a count or an optimum, and subproblems overlap |
| **Greedy** | Take the locally best choice, never undo | A local choice is provably safe |

If the same state can be reached by different routes (like decoding digits, chapter 12), memoize it and you are doing DP. If the state is a path you must also output, backtracking is the tool.

---

## Common mistakes

- **Forgetting the undo.** The state silently gets "dirty" and later branches are wrong.
- **Appending the live list** (`answers.append(path)`) instead of a copy (`path[:]`).
- **Not pruning.** The code works on the sample and times out on a real input.
- **Pruning incorrectly**, e.g. `break` when the candidates are not sorted, or `continue` where `break` was meant.
- **Duplicates**: when the input has repeated items, sort first and skip a choice equal to the previous one *at the same level*.
- **Mutating the input** (like the board) and forgetting to restore it.

---

## Practice

1. 🟢 Generate all subsets of a list **with size exactly `k`** (combinations), using a shared `path`.
2. 🟢 Print all binary strings of length `n` with no two adjacent `1`s.
3. 🟡 `subsets_with_duplicates([1, 2, 2])`: no repeated subsets. *(Hint: sort and skip equal neighbours.)*
4. 🟡 Count the ways to place `n` queens on the **first row only** so that none attack. (Then explain why it is a useless question and what it teaches about pruning.)
5. 🟡 Solve the **rat in a maze** variant that only allows moving down and right, and count the paths. Compare with the formula `C(2n−2, n−1)` for an open `n × n` grid.
6. 🔴 Solve a **4 × 4 Sudoku**: fill the blanks so that every row, column and 2 × 2 box holds 1 to 4.
7. 🔴 **Partition a string into palindromes**: return every way to split `"aab"` so every piece is a palindrome.
8. 🔴 **Letter case permutations**: for `"a1b2"` return `["a1b2", "a1B2", "A1b2", "A1B2"]`.

<details>
<summary>Hints</summary>

1. Choose the next item from the current position onward; stop when `len(path) == k`; prune when there are not enough items left.
2. Allow `1` only if the previous character was not `1`.
5. For an open grid moving only down/right, the count is the binomial coefficient `C(2n-2, n-1)`.
6. For each blank, try the digits 1 to 4; skip any digit already in the row, column or box; undo when the rest fails.
7. For each prefix that is a palindrome, recurse on the remaining suffix.
</details>

Backtracking explores the **tree of choices**; next we leave recursion for a while and study the **data structures** that hold our data, beginning with the humble list.
