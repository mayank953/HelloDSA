"""12. The Choices Tree: Permutations, Codes, Keypads and Hanoi

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 12-the-choices-tree.py
"""

def print_permutations(remaining, plate=""):
    if remaining == "":                       # base case: every dish has been placed
        print(plate)
        return
    for i in range(len(remaining)):
        chosen = remaining[i]                                   # choice: this dish goes next
        left_over = remaining[:i] + remaining[i + 1:]           # the dishes that are still available
        print_permutations(left_over, plate + chosen)           # assume: arrange all the rest

print_permutations("abc")

def show_choices(remaining, plate="", depth=0):
    pad = "    " * depth
    if remaining == "":
        print(f"{pad}done: {plate!r}")
        return
    print(f"{pad}plate={plate!r}, still available={remaining!r}")
    for i, chosen in enumerate(remaining):
        show_choices(remaining[:i] + remaining[i + 1:], plate + chosen, depth + 1)

show_choices("abc")

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

def hanoi(n, source="A", target="C", spare="B"):
    if n == 0:                                                # no disks: nothing to do
        return []
    first_half = hanoi(n - 1, source, spare, target)          # assume: n-1 disks go source -> spare
    big_move = [(source, target)]                             # my part: move the biggest disk
    second_half = hanoi(n - 1, spare, target, source)         # assume: n-1 disks go spare -> target
    return first_half + big_move + second_half

for step, (src, dst) in enumerate(hanoi(3), start=1):
    print(f"step {step}: move the top disk from {src} to {dst}")

print(f"{'disks':>5} | {'moves':>6} | {'2^n - 1':>7}")
for n in range(1, 11):
    print(f"{n:>5} | {len(hanoi(n)):>6} | {2 ** n - 1:>7}")

moves = 2 ** 64 - 1
years = moves / (60 * 60 * 24 * 365)
print(f"{moves:,} moves at one per second is about {years / 1e9:,.0f} billion years")

def is_valid_solution(n, moves):
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    for source, target in moves:
        disk = pegs[source].pop()                               # take the top disk
        if pegs[target] and pegs[target][-1] < disk:            # illegal: bigger onto smaller
            return False
        pegs[target].append(disk)
    return pegs["C"] == list(range(n, 0, -1))                   # everything arrived, in order

print(all(is_valid_solution(n, hanoi(n)) for n in range(0, 11)))

print('\n[all code in this chapter ran successfully]')
