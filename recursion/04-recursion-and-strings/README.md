# 4. Recursion and Strings

Strings and recursion: removing characters, palindromes, subsequences (take or skip), permutations (the plate analogy), decoding digit strings, phone keypad words, and the Tower of Hanoi. Each problem appears as a print version and a return version where it matters.

## Chapters

| Time | Chapter | Code and notes |
|------|---------|----------------|
| `7:46:50` | Recursion with strings: remove a character | [💻 `01-remove-a-character.py`](code/01-remove-a-character.py) · [📄 `recursion-strings-and-questions.pdf`](notes/recursion-strings-and-questions.pdf) |
| `8:03:10` | Palindrome check | [💻 `02-palindrome.py`](code/02-palindrome.py) |
| `8:30:09` | Substring vs subsequence | [🧩 `03-strings-substring-subsequence-starter.py`](code/03-strings-substring-subsequence-starter.py) |
| `8:36:04` | Print all subsequences | [💻 `04-print-all-subsequences.py`](code/04-print-all-subsequences.py) |
| `8:55:10` | Return all subsequences | [💻 `05-return-all-subsequences.py`](code/05-return-all-subsequences.py) |
| `9:11:19` | Permutations: print them | [💻 `06-print-permutations.py`](code/06-print-permutations.py) |
| `9:34:25` | Permutations: return them | [💻 `07-return-permutations.py`](code/07-return-permutations.py) |
| `9:50:00` | Return all codes | [💻 `08-return-all-codes.py`](code/08-return-all-codes.py) |
| `10:28:10` | Words from a phone number | [💻 `09-words-from-a-phone-number.py`](code/09-words-from-a-phone-number.py) |
| `10:49:58` | Tower of Hanoi | [💻 `10-tower-of-hanoi.py`](code/10-tower-of-hanoi.py) |
| `11:08:12` | Wrap-up | — |

## Files

### Code

| File | What it shows |
|---|---|
| [💻 `01-remove-a-character.py`](code/01-remove-a-character.py) | Remove every occurrence of a character, for example `z` from `abczz`. |
| [💻 `02-palindrome.py`](code/02-palindrome.py) | Palindrome check with a start and end helper. |
| [🧩 `03-strings-substring-subsequence-starter.py`](code/03-strings-substring-subsequence-starter.py) | Starter: notes on string, substring and subsequence, with an empty `return_subsequences`. |
| [💻 `04-print-all-subsequences.py`](code/04-print-all-subsequences.py) | Print every subsequence using a "taken so far" parameter. |
| [💻 `05-return-all-subsequences.py`](code/05-return-all-subsequences.py) | Return all subsequences as a list. |
| [💻 `06-print-permutations.py`](code/06-print-permutations.py) | Print every permutation of a string. |
| [💻 `07-return-permutations.py`](code/07-return-permutations.py) | Return all permutations as a list. |
| [💻 `08-return-all-codes.py`](code/08-return-all-codes.py) | Decode a digit string into letters (1 is a, 26 is z) and return every possible word. |
| [💻 `09-words-from-a-phone-number.py`](code/09-words-from-a-phone-number.py) | Every word that a phone-keypad number could spell. |
| [💻 `10-tower-of-hanoi.py`](code/10-tower-of-hanoi.py) | Tower of Hanoi with a step counter. |

### Notes (PDF)

| File | Pages | Size | What it is |
|---|---|---|---|
| [📄 `recursion-strings-and-questions.pdf`](notes/recursion-strings-and-questions.pdf) | 16 | 8.0 MB | Whiteboard notes and questions for strings (16 pages). |

### Notebooks

| File | What it is |
|---|---|
| [📓 `recursion-with-strings-class-notebook.ipynb`](notebooks/recursion-with-strings-class-notebook.ipynb) | Class notebook: recursion with strings. |
| [📓 `subsequences-class-notebook.ipynb`](notebooks/subsequences-class-notebook.ipynb) | Class notebook: subsequences. |
| [📓 `permutations-class-notebook.ipynb`](notebooks/permutations-class-notebook.ipynb) | Class notebook: permutations. |
| [📓 `letter-combinations-class-notebook.ipynb`](notebooks/letter-combinations-class-notebook.ipynb) | Class notebook: letter combinations from a keypad. |
| [📓 `print-and-return-codes-class-notebook.ipynb`](notebooks/print-and-return-codes-class-notebook.ipynb) | Class notebook: decoding digits, printing and returning. |
| [📓 `tower-of-hanoi-class-notebook.ipynb`](notebooks/tower-of-hanoi-class-notebook.ipynb) | Class notebook: Tower of Hanoi. |
| [📓 `questions.ipynb`](notebooks/questions.ipynb) | A longer practice notebook of recursion questions with code (63 cells). |

## Try it yourself

1. List all subsequences of `"abcd"` by hand using take or skip, then check the count (16).
2. Write `reverse_string(s)` recursively.
3. Count the permutations of a 4-letter word, then predict the count for 5 letters.
4. Run `10-tower-of-hanoi.py` for 3, 4 and 5 disks and find the pattern in the number of moves.
5. Take the checkpoint: `assignments/A4-recursion-and-strings.ipynb`.

🎯 **Checkpoint:** [Checkpoint 4: Recursion and Strings](../../assignments/A4-recursion-and-strings.ipynb) (solutions: [here](../../assignments/solutions/A4-recursion-and-strings.ipynb)).

---
[← Searching and Sorting with Recursion](../03-searching-and-sorting/) · [Recursion home](../README.md)
