"""13. Backtracking: Choose, Explore, Undo

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 13-backtracking.py
"""

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

def draw(placement):
    n = len(placement)
    return "\n".join("".join("Q " if placement[r] == c else ". " for c in range(n)) for r in range(n))

print(draw(solve_n_queens(6)[0]))

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

print('\n[all code in this chapter ran successfully]')
