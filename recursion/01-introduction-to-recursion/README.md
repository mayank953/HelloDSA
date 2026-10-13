# 1. Introduction to Recursion

Starts with what data structures and algorithms are, then builds recursion from the ground up: function calls and the call stack, factorial, the principle of mathematical induction, Fibonacci, head versus tail recursion.

## Chapters

| Time | Chapter | Code and notes |
|------|---------|----------------|
| `0:00` | Welcome: why DSA still matters | — |
| `2:21` | What are data structures? | [📄 `introduction-to-data-structures.pdf`](notes/introduction-to-data-structures.pdf) |
| `15:05` | What is an algorithm? | [📄 `introduction-to-data-structures.pdf`](notes/introduction-to-data-structures.pdf) |
| `22:10` | Why companies and software need DSA | — |
| `24:38` | Why we start with recursion | — |
| `26:19` | Revision: how functions work | — |
| `29:55` | A function calling another function (the call stack) | [💻 `01-intro-to-recursion.py`](code/01-intro-to-recursion.py) · [📄 `01-intro-to-recursion.pdf`](notes/01-intro-to-recursion.pdf) |
| `41:40` | A function calling itself | [💻 `02-function-calling-itself.py`](code/02-function-calling-itself.py) · [📄 `02-function-calling-itself.pdf`](notes/02-function-calling-itself.pdf) |
| `46:15` | Adding a stop: how the calls return | [💻 `02-function-calling-itself.py`](code/02-function-calling-itself.py) |
| `48:55` | What is recursion? (the mirror analogy) | — |
| `53:05` | Factorial: thinking recursively | [💻 `03-factorial.py`](code/03-factorial.py) · [📄 `03-factorial-and-recursion.pdf`](notes/03-factorial-and-recursion.pdf) |
| `1:04:00` | Stack memory and stack overflow | [💻 `03-factorial.py`](code/03-factorial.py) |
| `1:16:51` | PMI: principle of mathematical induction | [💻 `04-pmi-and-recursion.py`](code/04-pmi-and-recursion.py) · [📄 `04-understanding-pmi.pdf`](notes/04-understanding-pmi.pdf) |
| `1:32:00` | From PMI to a recursion recipe | — |
| `1:37:01` | Sum of the first N numbers | [💻 `05-sum-of-n-natural-numbers.py`](code/05-sum-of-n-natural-numbers.py) · [📄 `05-sum-of-natural-numbers.pdf`](notes/05-sum-of-natural-numbers.pdf) |
| `1:46:56` | Number of digits | [💻 `06-number-of-digits.py`](code/06-number-of-digits.py) |
| `1:55:26` | Fibonacci and the recursion tree | [💻 `07-fibonacci.py`](code/07-fibonacci.py) · [📄 `06-fibonacci-and-head-vs-tail.pdf`](notes/06-fibonacci-and-head-vs-tail.pdf) |
| `2:21:33` | Print 1 to N and N to 1 | [💻 `08-print-1-to-n.py`](code/08-print-1-to-n.py) · [💻 `08-print-n-to-1.py`](code/08-print-n-to-1.py) |
| `2:32:00` | Head vs tail recursion | [💻 `09-head-vs-tail-recursion.py`](code/09-head-vs-tail-recursion.py) |
| `2:38:00` | Recursion in a classroom: kids and notebooks | — |
| `2:43:48` | Assignments: sum of digits and power | [🧩 `10-assignment-sum-of-digits.py`](code/10-assignment-sum-of-digits.py) · [🧩 `11-assignment-power-of-a-number.py`](code/11-assignment-power-of-a-number.py) |

## Files

### Code

| File | What it shows |
|---|---|
| [💻 `01-intro-to-recursion.py`](code/01-intro-to-recursion.py) | Functions that call other functions in a chain, and a `printNum` with no stopping condition. Running this file ends in a RecursionError, which is the point of the demo. |
| [💻 `02-function-calling-itself.py`](code/02-function-calling-itself.py) | `printNum` calling itself with a stopping condition, so the calls return one by one. |
| [💻 `03-factorial.py`](code/03-factorial.py) | Recursive factorial, plus the unrolled `factorialone` to `factorialfour` version used to trace the call stack. |
| [💻 `04-pmi-and-recursion.py`](code/04-pmi-and-recursion.py) | A recursive function for 2 to the power n, written as the PMI plan: base case, induction hypothesis, then the step that uses it. |
| [💻 `05-sum-of-n-natural-numbers.py`](code/05-sum-of-n-natural-numbers.py) | Sum of the first N natural numbers with recursion. |
| [💻 `06-number-of-digits.py`](code/06-number-of-digits.py) | Counting the digits of a number recursively. |
| [💻 `07-fibonacci.py`](code/07-fibonacci.py) | Fibonacci with two recursive calls (the recursion tree). |
| [💻 `08-print-1-to-n.py`](code/08-print-1-to-n.py) | Print 1 to N: the order of the print and the recursive call decides the output. |
| [💻 `08-print-n-to-1.py`](code/08-print-n-to-1.py) | Print N down to 1. |
| [💻 `09-head-vs-tail-recursion.py`](code/09-head-vs-tail-recursion.py) | Factorial as head recursion, a tail attempt that goes wrong, and a correct tail version. |
| [🧩 `10-assignment-sum-of-digits.py`](code/10-assignment-sum-of-digits.py) | Assignment template with test cases. Implement `sum_of_digits` recursively. |
| [🧩 `11-assignment-power-of-a-number.py`](code/11-assignment-power-of-a-number.py) | Assignment template with test cases. Implement `power` recursively. |
| [✅ `10-assignment-sum-of-digits-solution.py`](solutions/10-assignment-sum-of-digits-solution.py) | A worked solution that implements `sum_of_digits` recursively, with the same tests. |
| [✅ `11-assignment-power-of-a-number-solution.py`](solutions/11-assignment-power-of-a-number-solution.py) | A worked solution that implements `power` recursively, with the same tests. |

### Notes (PDF)

| File | Pages | Size | What it is |
|---|---|---|---|
| [📄 `01-intro-to-recursion.pdf`](notes/01-intro-to-recursion.pdf) | 1 | 0.5 MB | Whiteboard notes: introduction to recursion. |
| [📄 `02-function-calling-itself.pdf`](notes/02-function-calling-itself.pdf) | 2 | 1.2 MB | Whiteboard notes: a function calling itself. |
| [📄 `03-factorial-and-recursion.pdf`](notes/03-factorial-and-recursion.pdf) | 3 | 1.9 MB | Whiteboard notes: factorial and the call stack. |
| [📄 `04-understanding-pmi.pdf`](notes/04-understanding-pmi.pdf) | 8 | 5.3 MB | Whiteboard notes: the principle of mathematical induction. |
| [📄 `05-sum-of-natural-numbers.pdf`](notes/05-sum-of-natural-numbers.pdf) | 1 | 0.7 MB | Whiteboard notes: sum of natural numbers. |
| [📄 `06-fibonacci-and-head-vs-tail.pdf`](notes/06-fibonacci-and-head-vs-tail.pdf) | 8 | 3.7 MB | Whiteboard notes: Fibonacci, head and tail recursion. |
| [📄 `introduction-to-data-structures.pdf`](notes/introduction-to-data-structures.pdf) | 3 | 3.5 MB | Whiteboard notes for the opening on data structures and algorithms. |
| [📄 `introduction-to-data-structures-v2.pdf`](notes/introduction-to-data-structures-v2.pdf) | 3 | 2.8 MB | A second version of the data structures and algorithms notes. |
| [📄 `fibonacci-recursion-notes.pdf`](notes/fibonacci-recursion-notes.pdf) | 3 | 2.0 MB | Whiteboard notes on Fibonacci recursion (3 pages). |

### Notebooks

| File | What it is |
|---|---|
| [📓 `recursion-class-notebook.ipynb`](notebooks/recursion-class-notebook.ipynb) | Class notebook with run outputs for the introduction to recursion. |
| [📓 `assignment-sum-of-digits.ipynb`](notebooks/assignment-sum-of-digits.ipynb) | Notebook version of the sum of digits assignment. |

## Try it yourself

1. Draw the call stack for `factorial(4)` on paper, then check it against the video at the factorial chapter.
2. Remove the base case from `02-function-calling-itself.py` and read the RecursionError. Then put it back.
3. Write `power2(base, n)` from the PMI idea: assume it works for `n - 1`, then use that.
4. Print the first 10 Fibonacci numbers and count how many calls `fibonacci(5)` makes.
5. Solve both assignment templates, then compare with the files in `solutions/`.

🎯 **Checkpoint:** [Checkpoint 1: Introduction to Recursion](../../assignments/A1-introduction-to-recursion.ipynb) (solutions: [here](../../assignments/solutions/A1-introduction-to-recursion.ipynb)).

---
[Recursion home](../README.md) · [Recursion and Arrays →](../02-recursion-and-arrays/)
