"""11. Recursion on Strings

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 11-recursion-on-strings.py
"""

text = "recursion"
print(text[0], "|", text[1:], "|", text[-1], "|", text[:-1])
print(text[1:3], text[::-1], len(text))

def remove(text, ch):
    if text == "":                       # base case
        return ""
    cleaned_rest = remove(text[1:], ch)  # assume: the rest without any ch
    if text[0] == ch:
        return cleaned_rest              # my character is unwanted: drop it
    return text[0] + cleaned_rest        # keep my character in front

print(remove("abczz", "z"), remove("good morning", "o"), remove("zzz", "z") == "", remove("abc", "x"))

def replace_pi(text):
    if len(text) <= 1:                         # base case: too short to contain "pi"
        return text
    if text[0:2] == "pi":
        return "3.14" + replace_pi(text[2:])   # consume two characters, write the replacement
    return text[0] + replace_pi(text[1:])      # consume one

print(replace_pi("pippppiiiipi"))

def collapse(text):
    if len(text) <= 1:
        return text
    if text[0] == text[1]:
        return collapse(text[1:])              # drop me; the next identical letter carries on
    return text[0] + collapse(text[1:])

print(collapse("aabbbccd"), collapse("abc"), collapse("aaaa"))

def is_palindrome(text):
    if len(text) <= 1:                    # base case
        return True
    if text[0] != text[-1]:               # my part, checked FIRST: a mismatch decides the answer
        return False
    return is_palindrome(text[1:-1])      # assume: the middle part

print(is_palindrome("nitin"), is_palindrome("abca"), is_palindrome(""), is_palindrome("ab"))

def palindrome_helper(text, start, end):
    if start >= end:                       # the pointers met or crossed: all pairs matched
        return True
    if text[start] != text[end]:
        return False
    return palindrome_helper(text, start + 1, end - 1)

def is_palindrome_fast(text):
    return palindrome_helper(text, 0, len(text) - 1)

print(is_palindrome_fast("nitin"), is_palindrome_fast("nitinr"))

def is_clean_palindrome(sentence):
    letters = "".join(ch.lower() for ch in sentence if ch.isalnum())
    return is_palindrome_fast(letters)

print(is_clean_palindrome("A man, a plan, a canal: Panama"))

text = "abc"

substrings = {text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1)}
print("substrings   :", sorted(substrings))

from itertools import combinations
subsequences = {"".join(c) for size in range(len(text) + 1) for c in combinations(text, size)}
print("subsequences :", sorted(subsequences))
print(len(substrings), "substrings (n(n+1)/2 =", len(text) * (len(text) + 1) // 2, ") and", len(subsequences), "subsequences (2^n =", 2 ** len(text), ")")

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

def print_subsequences(remaining, taken_so_far=""):
    if remaining == "":
        print(repr(taken_so_far))
        return
    first, rest = remaining[0], remaining[1:]
    print_subsequences(rest, taken_so_far + first)    # choice 1: take the first dish
    print_subsequences(rest, taken_so_far)            # choice 2: leave the first dish

print_subsequences("abc")

def subsequences(text):
    if text == "":
        return [""]                                  # exactly one plate: the empty one
    first, rest = text[0], text[1:]
    small_answer = subsequences(rest)                # assume: every plate from the rest
    with_first = [first + plate for plate in small_answer]   # plates where I TAKE my dish
    return small_answer + with_first                 # plates where I LEAVE it, then those with it

print(subsequences("abc"))
print(len(subsequences("abcd")), "subsequences of abcd")

def fill_subsequences(remaining, taken_so_far, answers):
    if remaining == "":
        answers.append(taken_so_far)
        return
    fill_subsequences(remaining[1:], taken_so_far + remaining[0], answers)
    fill_subsequences(remaining[1:], taken_so_far, answers)

answers = []
fill_subsequences("abc", "", answers)
print(answers)

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

def distinct_subsequences(text):
    """Duplicates in the input would repeat subsequences; a set removes them."""
    return sorted(set(subsequences(text)))

print(distinct_subsequences("aab"))

def subsequences_with_sum(numbers, target, i=0, running=0):
    """Count the subsets of numbers[i:] that, added to `running`, reach target."""
    if i == len(numbers):
        return 1 if running == target else 0
    taking = subsequences_with_sum(numbers, target, i + 1, running + numbers[i])
    leaving = subsequences_with_sum(numbers, target, i + 1, running)
    return taking + leaving

print(subsequences_with_sum([2, 3, 5, 7], 10))      # 3+7 and 2+3+5

print('\n[all code in this chapter ran successfully]')
