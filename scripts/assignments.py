"""Checkpoint assignments, one per recursion topic.

Each problem has:
  prompt   markdown shown to the learner
  starter  code the learner edits (valid Python; `...` is the blank)
  solution reference answer
  check    asserts that pass for the solution and fail for the starter
`build.py` turns these into assignments/<id>.ipynb and assignments/solutions/<id>.ipynb and
verifies every solution passes and every blank starter fails its check.
Solutions rely on optional parameters with defaults (for example `i=0`), so the tests can call
each function with just the documented arguments.
"""

SETUP = '''import inspect
import re


def check_recursive(fn, allow_loops=False):
    """Passes when `fn` calls itself and, unless allow_loops=True, uses no for/while statements."""
    lines = inspect.getsource(fn).split("\\n")[1:]
    body = "\\n".join(lines)
    assert re.search(rf"\\b{fn.__name__}\\s*\\(", body), f"{fn.__name__} should call itself (recursion)"
    if not allow_loops:
        assert not re.search(r"^\\s*(for|while)\\b", body, re.M), "No loops here: use recursion instead"
'''

ASSIGNMENTS = [
    # ------------------------------------------------------------------ 1
    dict(
        id="A1-introduction-to-recursion", title="Checkpoint 1: Introduction to Recursion",
        after="intro", topic="Introduction to Recursion",
        intro="Base case, recursive case, and the order of work. Every function must be recursive and use no loops.",
        problems=[
            dict(title="Count a digit",
                 prompt="Write `count_digit(n, d)`: how many times does the digit `d` appear in the positive integer `n`?",
                 starter="def count_digit(n, d):\n    ...",
                 solution="def count_digit(n, d):\n    if n == 0:\n        return 0\n    return (1 if n % 10 == d else 0) + count_digit(n // 10, d)",
                 check="assert count_digit(1022, 2) == 2\nassert count_digit(5, 5) == 1\nassert count_digit(123, 9) == 0\nassert count_digit(777, 7) == 3\nassert count_digit(100, 0) == 2\ncheck_recursive(count_digit)"),
            dict(title="Sum of squares",
                 prompt="Write `sum_of_squares(n)` returning 1\u00b2 + 2\u00b2 + ... + n\u00b2 (and 0 for `n = 0`).",
                 starter="def sum_of_squares(n):\n    ...",
                 solution="def sum_of_squares(n):\n    if n == 0:\n        return 0\n    return n * n + sum_of_squares(n - 1)",
                 check="assert sum_of_squares(0) == 0\nassert sum_of_squares(1) == 1\nassert sum_of_squares(3) == 14\nassert sum_of_squares(10) == 385\ncheck_recursive(sum_of_squares)"),
            dict(title="Greatest common divisor",
                 prompt="Write `gcd(a, b)` with Euclid's idea: `gcd(a, 0) = a`, otherwise `gcd(a, b) = gcd(b, a % b)`.",
                 starter="def gcd(a, b):\n    ...",
                 solution="def gcd(a, b):\n    if b == 0:\n        return a\n    return gcd(b, a % b)",
                 check="assert gcd(48, 18) == 6\nassert gcd(17, 5) == 1\nassert gcd(0, 9) == 9\nassert gcd(100, 75) == 25\ncheck_recursive(gcd)"),
            dict(title="Head and tail order",
                 prompt="Write `count_up(n)` returning `[1, 2, ..., n]` and `count_down(n)` returning `[n, ..., 1]` (both `[]` for 0). "
                        "Notice how the position of the recursive call changes the order.",
                 starter="def count_up(n):\n    ...\n\n\ndef count_down(n):\n    ...",
                 solution="def count_up(n):\n    if n == 0:\n        return []\n    return count_up(n - 1) + [n]\n\n\ndef count_down(n):\n    if n == 0:\n        return []\n    return [n] + count_down(n - 1)",
                 check="assert count_up(5) == [1, 2, 3, 4, 5]\nassert count_down(5) == [5, 4, 3, 2, 1]\nassert count_up(0) == [] and count_down(0) == []\ncheck_recursive(count_up)\ncheck_recursive(count_down)"),
            dict(title="Binary representation",
                 prompt="Write `to_binary(n)` returning the binary digits of `n` as a string (`'0'` for 0). Hint: `to_binary(n // 2)` followed by the last bit.",
                 starter="def to_binary(n):\n    ...",
                 solution="def to_binary(n):\n    if n < 2:\n        return str(n)\n    return to_binary(n // 2) + str(n % 2)",
                 check="assert to_binary(0) == '0'\nassert to_binary(1) == '1'\nassert to_binary(10) == '1010'\nassert to_binary(255) == '11111111'\ncheck_recursive(to_binary)"),
        ]),
    # ------------------------------------------------------------------ 2
    dict(
        id="A2-recursion-and-arrays", title="Checkpoint 2: Recursion and Arrays",
        after="arrays", topic="Recursion and Arrays",
        intro="Shrink the list, trust the recursive call, combine. You may add optional parameters with defaults (such as `i=0`) to avoid slicing.",
        problems=[
            dict(title="Maximum of a list",
                 prompt="Write `max_of_list(nums)` for a non-empty list, without using `max()`.",
                 starter="def max_of_list(nums):\n    ...",
                 solution="def max_of_list(nums):\n    if len(nums) == 1:\n        return nums[0]\n    rest = max_of_list(nums[1:])\n    return nums[0] if nums[0] > rest else rest",
                 check="assert max_of_list([3, 9, 2]) == 9\nassert max_of_list([5]) == 5\nassert max_of_list([-4, -2, -9]) == -2\nassert max_of_list([1, 2, 3, 4, 5]) == 5\ncheck_recursive(max_of_list)"),
            dict(title="Count occurrences",
                 prompt="Write `count_occurrences(nums, x)`: how many times does `x` appear in `nums`? An empty list gives 0.",
                 starter="def count_occurrences(nums, x):\n    ...",
                 solution="def count_occurrences(nums, x):\n    if not nums:\n        return 0\n    return (1 if nums[0] == x else 0) + count_occurrences(nums[1:], x)",
                 check="assert count_occurrences([], 3) == 0\nassert count_occurrences([2, 2, 5, 2], 2) == 3\nassert count_occurrences([1, 2, 3], 9) == 0\ncheck_recursive(count_occurrences)"),
            dict(title="Last index",
                 prompt="Write `last_index(nums, x, i=None)` returning the last index of `x`, or -1 if it is absent. Start from the end.",
                 starter="def last_index(nums, x, i=None):\n    ...",
                 solution="def last_index(nums, x, i=None):\n    if i is None:\n        i = len(nums) - 1\n    if i < 0:\n        return -1\n    if nums[i] == x:\n        return i\n    return last_index(nums, x, i - 1)",
                 check="assert last_index([3, 2, 5, 2, 8, 2, 1], 2) == 5\nassert last_index([3, 2, 5], 9) == -1\nassert last_index([], 1) == -1\nassert last_index([7], 7) == 0\ncheck_recursive(last_index)"),
            dict(title="Return a new list of indices",
                 prompt="Write `indices_greater_than(nums, k, i=0)` returning a **new list** of the indices whose value is greater than `k` (in increasing order).",
                 starter="def indices_greater_than(nums, k, i=0):\n    ...",
                 solution="def indices_greater_than(nums, k, i=0):\n    if i == len(nums):\n        return []\n    rest = indices_greater_than(nums, k, i + 1)\n    return ([i] if nums[i] > k else []) + rest",
                 check="assert indices_greater_than([3, 8, 1, 9, 5], 4) == [1, 3, 4]\nassert indices_greater_than([], 0) == []\nassert indices_greater_than([1, 1], 5) == []\ncheck_recursive(indices_greater_than)"),
            dict(title="Reverse a list",
                 prompt="Write `reverse_list(nums)` returning a new reversed list. The original list must not change.",
                 starter="def reverse_list(nums):\n    ...",
                 solution="def reverse_list(nums):\n    if not nums:\n        return []\n    return reverse_list(nums[1:]) + [nums[0]]",
                 check="data = [1, 2, 3]\nassert reverse_list(data) == [3, 2, 1]\nassert data == [1, 2, 3]\nassert reverse_list([]) == []\nassert reverse_list([7]) == [7]\ncheck_recursive(reverse_list)"),
        ]),
    # ------------------------------------------------------------------ 3
    dict(
        id="A3-searching-and-sorting", title="Checkpoint 3: Searching and Sorting",
        after="search-sort", topic="Searching and Sorting with Recursion",
        intro="Linear and binary search, then merge sort and quick sort. Sorting functions must return a new list and leave the input unchanged.",
        problems=[
            dict(title="Find the first occurrence",
                 prompt="Write `find_first(nums, x, i=0)` returning the index of the first `x`, or -1.",
                 starter="def find_first(nums, x, i=0):\n    ...",
                 solution="def find_first(nums, x, i=0):\n    if i == len(nums):\n        return -1\n    if nums[i] == x:\n        return i\n    return find_first(nums, x, i + 1)",
                 check="assert find_first([4, 7, 7, 1], 7) == 1\nassert find_first([4, 7], 9) == -1\nassert find_first([], 1) == -1\ncheck_recursive(find_first)"),
            dict(title="Binary search",
                 prompt="Write `binary_search(nums, target, low=0, high=None)` for a sorted list. Return the index or -1.",
                 starter="def binary_search(nums, target, low=0, high=None):\n    ...",
                 solution="def binary_search(nums, target, low=0, high=None):\n    if high is None:\n        high = len(nums) - 1\n    if low > high:\n        return -1\n    mid = (low + high) // 2\n    if nums[mid] == target:\n        return mid\n    if nums[mid] < target:\n        return binary_search(nums, target, mid + 1, high)\n    return binary_search(nums, target, low, mid - 1)",
                 check="data = [1, 3, 5, 7, 9, 11]\nassert [binary_search(data, v) for v in data] == [0, 1, 2, 3, 4, 5]\nassert binary_search(data, 4) == -1\nassert binary_search(data, 100) == -1\nassert binary_search([], 1) == -1\ncheck_recursive(binary_search)"),
            dict(title="Merge two sorted lists",
                 prompt="Write `merge(a, b)` that merges two sorted lists into one new sorted list. You can use a loop or recursion.",
                 starter="def merge(a, b):\n    ...",
                 solution="def merge(a, b):\n    out = []\n    i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            out.append(a[i])\n            i += 1\n        else:\n            out.append(b[j])\n            j += 1\n    return out + a[i:] + b[j:]",
                 check="assert merge([1, 4, 9], [2, 3, 10]) == [1, 2, 3, 4, 9, 10]\nassert merge([], [1]) == [1]\nassert merge([1, 1], [1]) == [1, 1, 1]\nassert merge([], []) == []"),
            dict(title="Merge sort",
                 prompt="Write `merge_sort(nums)` returning a new sorted list. Use your `merge` from the previous problem.",
                 starter="def merge_sort(nums):\n    ...",
                 solution="def merge_sort(nums):\n    if len(nums) <= 1:\n        return nums[:]\n    mid = len(nums) // 2\n    return merge(merge_sort(nums[:mid]), merge_sort(nums[mid:]))",
                 check="import random\nrandom.seed(1)\nfor _ in range(30):\n    data = [random.randint(-20, 20) for _ in range(random.randint(0, 12))]\n    copy = data[:]\n    assert merge_sort(data) == sorted(data)\n    assert data == copy\ncheck_recursive(merge_sort)"),
            dict(title="Quick sort",
                 prompt="Write `quick_sort(nums)` returning a new sorted list. Use the last element as the pivot. It must work with duplicates.",
                 starter="def quick_sort(nums):\n    ...",
                 solution="def quick_sort(nums):\n    if len(nums) <= 1:\n        return nums[:]\n    pivot = nums[-1]\n    smaller = [x for x in nums[:-1] if x <= pivot]\n    larger = [x for x in nums[:-1] if x > pivot]\n    return quick_sort(smaller) + [pivot] + quick_sort(larger)",
                 check="import random\nrandom.seed(2)\nfor _ in range(30):\n    data = [random.randint(-5, 5) for _ in range(random.randint(0, 15))]\n    copy = data[:]\n    assert quick_sort(data) == sorted(data)\n    assert data == copy\ncheck_recursive(quick_sort)"),
        ]),
    # ------------------------------------------------------------------ 4
    dict(
        id="A4-recursion-and-strings", title="Checkpoint 4: Recursion and Strings",
        after="strings", topic="Recursion and Strings",
        intro="Strings, subsequences, permutations, keypad words and the Tower of Hanoi. Loops are allowed for the problems that need to try several choices.",
        problems=[
            dict(title="Remove a character",
                 prompt="Write `remove_char(s, ch)` returning `s` without any `ch`.",
                 starter="def remove_char(s, ch):\n    ...",
                 solution="def remove_char(s, ch):\n    if s == '':\n        return ''\n    rest = remove_char(s[1:], ch)\n    return rest if s[0] == ch else s[0] + rest",
                 check="assert remove_char('good morning', 'o') == 'gd mrning'\nassert remove_char('zzz', 'z') == ''\nassert remove_char('', 'a') == ''\nassert remove_char('abc', 'x') == 'abc'\ncheck_recursive(remove_char)"),
            dict(title="Reverse a string",
                 prompt="Write `reverse_string(s)` recursively.",
                 starter="def reverse_string(s):\n    ...",
                 solution="def reverse_string(s):\n    if len(s) <= 1:\n        return s\n    return reverse_string(s[1:]) + s[0]",
                 check="assert reverse_string('abc') == 'cba'\nassert reverse_string('') == ''\nassert reverse_string('a') == 'a'\nassert reverse_string('racecar') == 'racecar'\ncheck_recursive(reverse_string)"),
            dict(title="All subsequences",
                 prompt="Write `subsequences(s)` returning a list of all subsequences of `s`, including the empty string, in any order.",
                 starter="def subsequences(s):\n    ...",
                 solution="def subsequences(s):\n    if s == '':\n        return ['']\n    rest = subsequences(s[1:])\n    return rest + [s[0] + x for x in rest]",
                 check="assert sorted(subsequences('abc')) == sorted(['', 'a', 'b', 'c', 'ab', 'ac', 'bc', 'abc'])\nassert subsequences('') == ['']\nassert len(subsequences('abcd')) == 16\ncheck_recursive(subsequences)"),
            dict(title="All permutations",
                 prompt="Write `permutations(s)` returning a list of every permutation of a string with distinct letters, in any order.",
                 starter="def permutations(s):\n    ...",
                 solution="def permutations(s):\n    if len(s) <= 1:\n        return [s]\n    out = []\n    for i, ch in enumerate(s):\n        for p in permutations(s[:i] + s[i + 1:]):\n            out.append(ch + p)\n    return out",
                 check="from itertools import permutations as _perms\nassert sorted(permutations('abc')) == sorted(''.join(p) for p in _perms('abc'))\nassert len(permutations('abcd')) == 24\nassert permutations('a') == ['a']\ncheck_recursive(permutations, allow_loops=True)"),
            dict(title="Phone keypad words",
                 prompt="The keypad mapping is given. Write `letter_combinations(digits)` returning every word the digit string could spell (`['']` for an empty string).",
                 starter="KEYS = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}\n\n\ndef letter_combinations(digits):\n    ...",
                 solution="KEYS = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}\n\n\ndef letter_combinations(digits):\n    if digits == '':\n        return ['']\n    rest = letter_combinations(digits[1:])\n    return [c + word for c in KEYS[digits[0]] for word in rest]",
                 check="assert letter_combinations('') == ['']\nassert sorted(letter_combinations('7')) == ['p', 'q', 'r', 's']\nassert sorted(letter_combinations('23')) == sorted(a + b for a in 'abc' for b in 'def')\nassert len(letter_combinations('92')) == 12\ncheck_recursive(letter_combinations, allow_loops=True)"),
            dict(title="Tower of Hanoi moves",
                 prompt="Write `hanoi_moves(n, source='A', target='C', spare='B')` returning the list of moves as `(from_peg, to_peg)` tuples that moves `n` disks from `source` to `target`.",
                 starter="def hanoi_moves(n, source='A', target='C', spare='B'):\n    ...",
                 solution="def hanoi_moves(n, source='A', target='C', spare='B'):\n    if n == 0:\n        return []\n    return (hanoi_moves(n - 1, source, spare, target)\n            + [(source, target)]\n            + hanoi_moves(n - 1, spare, target, source))",
                 check="for n in range(0, 6):\n    moves = hanoi_moves(n)\n    assert len(moves) == 2 ** n - 1\n    pegs = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}\n    for a, b in moves:\n        disk = pegs[a].pop()\n        assert not pegs[b] or pegs[b][-1] > disk, 'a larger disk was placed on a smaller one'\n        pegs[b].append(disk)\n    assert pegs['C'] == list(range(n, 0, -1)), 'all disks must end on the target peg'\ncheck_recursive(hanoi_moves)"),
        ]),
]

# Reference solutions for the two assignment templates in the video (code/10 and code/11).
TEMPLATE_SOLUTIONS = {
    "10-assignment-sum-of-digits.py": (
        "def sum_of_digits(n):\n    # Your code here\n    pass\n",
        "def sum_of_digits(n):\n    n = abs(n)\n    if n < 10:\n        return n\n    return n % 10 + sum_of_digits(n // 10)\n",
    ),
    "11-assignment-power-of-a-number.py": (
        "def power(base: int, exponent: int) -> int:\n    # Your code here\n    pass\n",
        "def power(base: int, exponent: int) -> int:\n    # Halving the exponent keeps the recursion depth small, so even exponent = 1000 is safe.\n"
        "    if exponent == 0:\n        return 1\n    half = power(base, exponent // 2)\n    if exponent % 2 == 0:\n        return half * half\n    return half * half * base\n",
    ),
}
