# Hello DSA

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Master Data Structures and Algorithms the visual way.** The complete code, whiteboard notes, practice and a DSA + AI roadmap
for the **Hello DSA** video on recursion. Share your progress with **#HelloDSA**.

> 👋 **Coming from the video?** Start with [Recursion: complete code and notes](recursion/README.md). Every chapter below links to the
> exact code file and the notes for it. New to all of this? Follow the [DSA + AI roadmap](roadmap/README.md).


## Contents

- [Start here](#start-here) · [Set up](#set-up) · [Prerequisite](#prerequisite-python)
- [What the video covers](#what-the-video-covers) · [Chapter overview](#chapter-overview)
- [Recursion: complete code and notes](#recursion-complete-code-and-notes) · [Checkpoint assignments](#checkpoint-assignments)
- [More DSA topics](#more-dsa-topics) · [DSA + AI roadmap](roadmap/README.md)
- [Resources explained](#resources-explained) · [Where to find everything](#where-to-find-everything)
- [Repository layout](#repository-layout) · [FAQ](#faq)

## Start here

1. **Watch** the video and use the timestamps in the [chapter table](#chapter-overview) to jump around.
2. **Open the topic folder** for the part you are watching. Each one has the code, the notes (PDF) and a page that lists them by chapter.
3. **Run the code yourself**, change it, and break it on purpose.
4. **Test yourself** with the checkpoint assignments, then compare with the solutions.
5. **Plan what comes next** with the [roadmap](roadmap/README.md).

## Set up

You need Python 3.9 or newer. The recursion code uses only the standard library, so you can run a file with one command:

```bash
git clone https://github.com/mayank953/hello-dsa.git
cd hello-dsa
python3 recursion/01-introduction-to-recursion/code/03-factorial.py
```

For the notebooks and assignments:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

No install? Download the ZIP (*Code*, then *Download ZIP*) or upload a notebook to [Google Colab](https://colab.research.google.com/).

## Prerequisite: Python

The video assumes you know Python functions, scope and slicing. If any of that is new, the free
[Hello Python course](https://github.com/mayank953/python-ai-crash-course) covers it: [functions](https://github.com/mayank953/python-ai-crash-course/tree/main/python/37-intro-to-functions),
[scope](https://github.com/mayank953/python-ai-crash-course/tree/main/python/41-variable-scope) and [slicing](https://github.com/mayank953/python-ai-crash-course/tree/main/python/09-concatenation-slicing).

## What the video covers

The video starts with an introduction to data structures and algorithms and then goes deep on recursion in four topics.

| # | Topic | Starts at | What you get |
|---|---|---|---|
| 1 | [Introduction to Recursion](recursion/01-introduction-to-recursion/) | `0:00` | 12 code files, 9 PDFs, 2 notebooks, a checkpoint |
| 2 | [Recursion and Arrays](recursion/02-recursion-and-arrays/) | `2:50:40` | 7 code files, 1 PDF, 1 notebook, a checkpoint |
| 3 | [Searching and Sorting with Recursion](recursion/03-searching-and-sorting/) | `5:35:08` | 6 code files, 0 PDFs, 3 notebooks, a checkpoint |
| 4 | [Recursion and Strings](recursion/04-recursion-and-strings/) | `7:46:50` | 10 code files, 1 PDF, 7 notebooks, a checkpoint |

## Chapter overview

All 48 chapters, each linked to the code and notes that go with it.

<details>
<summary><b>Show the full chapter table</b></summary>

| Time | Chapter | Code and notes |
|------|---------|----------------|
| `0:00` | Welcome: why DSA still matters | — |
| `2:21` | What are data structures? | [📄 `introduction-to-data-structures.pdf`](recursion/01-introduction-to-recursion/notes/introduction-to-data-structures.pdf) |
| `15:05` | What is an algorithm? | [📄 `introduction-to-data-structures.pdf`](recursion/01-introduction-to-recursion/notes/introduction-to-data-structures.pdf) |
| `22:10` | Why companies and software need DSA | — |
| `24:38` | Why we start with recursion | — |
| `26:19` | Revision: how functions work | — |
| `29:55` | A function calling another function (the call stack) | [💻 `01-intro-to-recursion.py`](recursion/01-introduction-to-recursion/code/01-intro-to-recursion.py) · [📄 `01-intro-to-recursion.pdf`](recursion/01-introduction-to-recursion/notes/01-intro-to-recursion.pdf) |
| `41:40` | A function calling itself | [💻 `02-function-calling-itself.py`](recursion/01-introduction-to-recursion/code/02-function-calling-itself.py) · [📄 `02-function-calling-itself.pdf`](recursion/01-introduction-to-recursion/notes/02-function-calling-itself.pdf) |
| `46:15` | Adding a stop: how the calls return | [💻 `02-function-calling-itself.py`](recursion/01-introduction-to-recursion/code/02-function-calling-itself.py) |
| `48:55` | What is recursion? (the mirror analogy) | — |
| `53:05` | Factorial: thinking recursively | [💻 `03-factorial.py`](recursion/01-introduction-to-recursion/code/03-factorial.py) · [📄 `03-factorial-and-recursion.pdf`](recursion/01-introduction-to-recursion/notes/03-factorial-and-recursion.pdf) |
| `1:04:00` | Stack memory and stack overflow | [💻 `03-factorial.py`](recursion/01-introduction-to-recursion/code/03-factorial.py) |
| `1:16:51` | PMI: principle of mathematical induction | [💻 `04-pmi-and-recursion.py`](recursion/01-introduction-to-recursion/code/04-pmi-and-recursion.py) · [📄 `04-understanding-pmi.pdf`](recursion/01-introduction-to-recursion/notes/04-understanding-pmi.pdf) |
| `1:32:00` | From PMI to a recursion recipe | — |
| `1:37:01` | Sum of the first N numbers | [💻 `05-sum-of-n-natural-numbers.py`](recursion/01-introduction-to-recursion/code/05-sum-of-n-natural-numbers.py) · [📄 `05-sum-of-natural-numbers.pdf`](recursion/01-introduction-to-recursion/notes/05-sum-of-natural-numbers.pdf) |
| `1:46:56` | Number of digits | [💻 `06-number-of-digits.py`](recursion/01-introduction-to-recursion/code/06-number-of-digits.py) |
| `1:55:26` | Fibonacci and the recursion tree | [💻 `07-fibonacci.py`](recursion/01-introduction-to-recursion/code/07-fibonacci.py) · [📄 `06-fibonacci-and-head-vs-tail.pdf`](recursion/01-introduction-to-recursion/notes/06-fibonacci-and-head-vs-tail.pdf) |
| `2:21:33` | Print 1 to N and N to 1 | [💻 `08-print-1-to-n.py`](recursion/01-introduction-to-recursion/code/08-print-1-to-n.py) · [💻 `08-print-n-to-1.py`](recursion/01-introduction-to-recursion/code/08-print-n-to-1.py) |
| `2:32:00` | Head vs tail recursion | [💻 `09-head-vs-tail-recursion.py`](recursion/01-introduction-to-recursion/code/09-head-vs-tail-recursion.py) |
| `2:38:00` | Recursion in a classroom: kids and notebooks | — |
| `2:43:48` | Assignments: sum of digits and power | [🧩 `10-assignment-sum-of-digits.py`](recursion/01-introduction-to-recursion/code/10-assignment-sum-of-digits.py) · [🧩 `11-assignment-power-of-a-number.py`](recursion/01-introduction-to-recursion/code/11-assignment-power-of-a-number.py) |
| `2:50:40` | Recursion with arrays: shrinking the problem | [📄 `recursion-and-arrays.pdf`](recursion/02-recursion-and-arrays/notes/recursion-and-arrays.pdf) |
| `3:00:55` | Sum of an array | [💻 `01-sum-of-array.py`](recursion/02-recursion-and-arrays/code/01-sum-of-array.py) |
| `3:30:15` | Check if an array is sorted | [💻 `02-check-if-array-is-sorted.py`](recursion/02-recursion-and-arrays/code/02-check-if-array-is-sorted.py) |
| `3:54:50` | First and last index of an element | [💻 `03-first-and-last-index.py`](recursion/02-recursion-and-arrays/code/03-first-and-last-index.py) |
| `4:20:06` | All indices of a number | [💻 `04-all-indices-of-a-number.py`](recursion/02-recursion-and-arrays/code/04-all-indices-of-a-number.py) |
| `4:32:00` | Optimisation: pass an index instead of slicing | [💻 `04-all-indices-of-a-number.py`](recursion/02-recursion-and-arrays/code/04-all-indices-of-a-number.py) |
| `4:43:30` | Collecting answers in a list passed down | [💻 `05-collect-indices-in-a-passed-list.py`](recursion/02-recursion-and-arrays/code/05-collect-indices-in-a-passed-list.py) |
| `4:58:30` | Collecting answers in a global list | [💻 `06-collect-indices-in-a-global-list.py`](recursion/02-recursion-and-arrays/code/06-collect-indices-in-a-global-list.py) |
| `5:04:55` | Returning a new list | [💻 `07-return-indices-as-a-new-list.py`](recursion/02-recursion-and-arrays/code/07-return-indices-as-a-new-list.py) |
| `5:35:08` | Linear search with recursion | [💻 `01-linear-search.py`](recursion/03-searching-and-sorting/code/01-linear-search.py) |
| `5:50:54` | Binary search with recursion | [💻 `02-binary-search.py`](recursion/03-searching-and-sorting/code/02-binary-search.py) |
| `6:12:30` | Merge sort: the idea | [🧩 `03-merge-sort-starter.py`](recursion/03-searching-and-sorting/code/03-merge-sort-starter.py) |
| `6:27:56` | Merge sort: the approach step by step | [🧩 `03-merge-sort-starter.py`](recursion/03-searching-and-sorting/code/03-merge-sort-starter.py) |
| `6:40:05` | Merge sort: code and debugging | [💻 `04-merge-sort.py`](recursion/03-searching-and-sorting/code/04-merge-sort.py) |
| `7:11:17` | Quick sort: pivot and partition | [🧩 `05-quick-sort-starter.py`](recursion/03-searching-and-sorting/code/05-quick-sort-starter.py) |
| `7:25:10` | Quick sort: code | [💻 `06-quick-sort.py`](recursion/03-searching-and-sorting/code/06-quick-sort.py) |
| `7:46:50` | Recursion with strings: remove a character | [💻 `01-remove-a-character.py`](recursion/04-recursion-and-strings/code/01-remove-a-character.py) · [📄 `recursion-strings-and-questions.pdf`](recursion/04-recursion-and-strings/notes/recursion-strings-and-questions.pdf) |
| `8:03:10` | Palindrome check | [💻 `02-palindrome.py`](recursion/04-recursion-and-strings/code/02-palindrome.py) |
| `8:30:09` | Substring vs subsequence | [🧩 `03-strings-substring-subsequence-starter.py`](recursion/04-recursion-and-strings/code/03-strings-substring-subsequence-starter.py) |
| `8:36:04` | Print all subsequences | [💻 `04-print-all-subsequences.py`](recursion/04-recursion-and-strings/code/04-print-all-subsequences.py) |
| `8:55:10` | Return all subsequences | [💻 `05-return-all-subsequences.py`](recursion/04-recursion-and-strings/code/05-return-all-subsequences.py) |
| `9:11:19` | Permutations: print them | [💻 `06-print-permutations.py`](recursion/04-recursion-and-strings/code/06-print-permutations.py) |
| `9:34:25` | Permutations: return them | [💻 `07-return-permutations.py`](recursion/04-recursion-and-strings/code/07-return-permutations.py) |
| `9:50:00` | Return all codes | [💻 `08-return-all-codes.py`](recursion/04-recursion-and-strings/code/08-return-all-codes.py) |
| `10:28:10` | Words from a phone number | [💻 `09-words-from-a-phone-number.py`](recursion/04-recursion-and-strings/code/09-words-from-a-phone-number.py) |
| `10:49:58` | Tower of Hanoi | [💻 `10-tower-of-hanoi.py`](recursion/04-recursion-and-strings/code/10-tower-of-hanoi.py) |
| `11:08:12` | Wrap-up | — |

</details>

## Recursion: complete code and notes

Open a topic to see its chapters, every code file with a description, the PDF notes with page counts, the class notebooks and practice tasks.

| # | Topic | Starts at | What you get |
|---|---|---|---|
| 1 | [Introduction to Recursion](recursion/01-introduction-to-recursion/) | `0:00` | 12 code files, 9 PDFs, 2 notebooks, a checkpoint |
| 2 | [Recursion and Arrays](recursion/02-recursion-and-arrays/) | `2:50:40` | 7 code files, 1 PDF, 1 notebook, a checkpoint |
| 3 | [Searching and Sorting with Recursion](recursion/03-searching-and-sorting/) | `5:35:08` | 6 code files, 0 PDFs, 3 notebooks, a checkpoint |
| 4 | [Recursion and Strings](recursion/04-recursion-and-strings/) | `7:46:50` | 10 code files, 1 PDF, 7 notebooks, a checkpoint |

The longer notes that run across the whole series are listed on the [recursion page](recursion/README.md#notes-that-cover-the-whole-series).

## Checkpoint assignments

Test yourself at the end of each topic. Every problem has a check cell that tells you instantly whether you got it right, and whether you really used recursion.

| Checkpoint | After | Problems | Starter | Solutions |
|---|---|---|---|---|
| Introduction to Recursion | Introduction to Recursion | 5 | [notebook](assignments/A1-introduction-to-recursion.ipynb) | [solutions](assignments/solutions/A1-introduction-to-recursion.ipynb) |
| Recursion and Arrays | Recursion and Arrays | 5 | [notebook](assignments/A2-recursion-and-arrays.ipynb) | [solutions](assignments/solutions/A2-recursion-and-arrays.ipynb) |
| Searching and Sorting | Searching and Sorting with Recursion | 5 | [notebook](assignments/A3-searching-and-sorting.ipynb) | [solutions](assignments/solutions/A3-searching-and-sorting.ipynb) |
| Recursion and Strings | Recursion and Strings | 6 | [notebook](assignments/A4-recursion-and-strings.ipynb) | [solutions](assignments/solutions/A4-recursion-and-strings.ipynb) |

The two assignments from the video (sum of digits and power) have starter files with tests and worked solutions in
[`01-introduction-to-recursion`](recursion/01-introduction-to-recursion/).

## More DSA topics

The same notes and code for the topics around recursion, so you can keep going after the video.

| Topic | What's inside | Files |
|---|---|---|
| [Arrays](dsa-topics/arrays/) | How arrays work under the hood: a short set of notes and a notebook that builds a dynamic array (a Python-list look-alike) from scratch with `ctypes`. | 1 code file or notebook, 1 PDF |
| [Time and Space Complexity](dsa-topics/time-and-space-complexity/) | Big-O in practice: how to count the work an algorithm does, why growth rate matters on large inputs, and how recursion uses memory. Notebooks time real code (merge sort against bubble sort) and plot the growth. | 10 code file or notebooks, 4 PDFs |
| [Linked List](dsa-topics/linked-list/) | Build a singly linked list step by step: the node, taking input, length, insert, delete and search, each written iteratively and recursively. The complete code notebook puts everything in one place. | 9 code file or notebooks, 4 PDFs |
| [Stack](dsa-topics/stack/) | The last-in, first-out structure, built on a list, an array, a dynamic array and a linked list. | 1 code file or notebook, 1 PDF |
| [Queue](dsa-topics/queue/) | The first-in, first-out structure, built on an array, a list and a linked list. | 1 code file or notebook, 1 PDF |
| [Trees](dsa-topics/trees/) | Generic trees, binary trees and binary search trees: nodes, traversals (inorder, preorder), and BST operations, nearly all of them recursive. | 5 code file or notebooks, 5 PDFs |
| [Hashmaps](dsa-topics/hashmaps/) | Hash tables from the ground up: hashing, collisions, and open addressing with linear probing. | 2 code file or notebooks, 1 PDF |
| [Dynamic Programming](dsa-topics/dynamic-programming/) | A starting point for dynamic programming: the prerequisites (recursion, lists, 2D lists, indexing) and the Fibonacci recursion that DP optimises. | 1 code file or notebook, 0 PDFs |

See the [DSA topics page](dsa-topics/README.md) for the suggested order, or the [roadmap](roadmap/README.md) for the full plan.

## Resources explained

Links used in the video and the code, and what each one is good for.

| Resource | What it is | Use it for | Video |
|---|---|---|---|
| [Hello Python: the Python course](https://github.com/mayank953/python-ai-crash-course) | The free Python course this DSA series builds on. Use it if functions, scope or slicing feel shaky. | Prerequisite | `26:19` |
| [Hello Python: functions](https://github.com/mayank953/python-ai-crash-course/tree/main/python/37-intro-to-functions) | Lessons 37 to 44 cover defining functions, arguments, scope, lambda, map, filter and reduce. | Chapters on functions and the call stack | `26:19` |
| [Hello Python: variable scope](https://github.com/mayank953/python-ai-crash-course/tree/main/python/41-variable-scope) | Local versus global variables. It matters for the global-list approach. | Collecting answers in a global list | `4:58:30` |
| [Hello Python: slicing](https://github.com/mayank953/python-ai-crash-course/tree/main/python/09-concatenation-slicing) | Slicing with start, stop and step, used all through the arrays and strings topics. | Recursion with arrays and strings | `2:50:40` |
| [Python docs: sys.setrecursionlimit](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit) | Why Python stops a runaway recursion and how the limit can be changed. | Stack memory and stack overflow | `1:04:00` |
| [Tower of Hanoi animation](https://yongdanielliang.github.io/animation/web/TowerOfHanoi.html) | An interactive animation. Pick the number of disks and watch the moves. | Tower of Hanoi | `10:49:58` |
| [LeetCode: Pow(x, n)](https://leetcode.com/problems/powx-n/) | A harder version of the power assignment (negative exponents, very large inputs). | Assignments: sum of digits and power | `2:43:48` |
| [LeetCode: Add Digits](https://leetcode.com/problems/add-digits/) | A related digit problem: keep adding the digits until one digit is left. | Assignments: sum of digits and power | `2:43:48` |
| [Desmos graph of growth rates](https://www.desmos.com/calculator/l99rykuzx8) | Plot O(1), O(log n), O(n), O(n log n) and O(n^2) to see how quickly each one grows. | Time and space complexity |  |
| [Big-O Cheat Sheet](https://www.bigocheatsheet.com) | One-page summary of the complexity of common algorithms and data structures. | Time and space complexity |  |
| [BST animation](https://yongdanielliang.github.io/animation/web/BST.html) | Watch inserts, searches and deletes on a binary search tree step by step. | Trees |  |

> Some of these sites block automated link checkers. If one does not open, search for its title.

## Where to find everything

| You want | Go to |
|---|---|
| The code for a video chapter | The chapter table above, or the topic page in [`recursion/`](recursion/) |
| The whiteboard notes (PDF) | `notes/` inside each topic, or [`recursion/notes/`](recursion/notes/) for the long notes |
| A runnable notebook with outputs | `notebooks/` inside each topic |
| Practice with instant feedback | [`assignments/`](assignments/README.md) |
| Linked list, stack, queue, trees, hashmaps, complexity | [`dsa-topics/`](dsa-topics/README.md) |
| A study plan | [`roadmap/`](roadmap/README.md) |
| Every file and link in one table | [INDEX.md](INDEX.md) |

**Tips:** PDFs open in the browser on GitHub. For long PDFs, download the file for faster scrolling. Notebook and code file names start with a number that follows the video order.

## Repository layout

```
hello-dsa/
├── README.md                 you are here
├── INDEX.md                  every file and link in one table
├── requirements.txt          jupyterlab, numpy, matplotlib
├── roadmap/                  the DSA + AI roadmap
├── recursion/                the video: code, notes, notebooks
│   ├── 01-introduction-to-recursion/   code/ notes/ notebooks/ solutions/
│   ├── 02-recursion-and-arrays/
│   ├── 03-searching-and-sorting/
│   ├── 04-recursion-and-strings/
│   └── notes/                long recursion notes (PDF)
├── assignments/              four checkpoints and solutions
├── dsa-topics/               arrays, complexity, linked list, stack, queue, trees, hashmaps, DP
└── scripts/                  maintainer tooling (learners can ignore)
```

The repository holds 88 code files and notebooks and 34 PDFs.

## FAQ

**Which file matches the part of the video I am on?** Use the [chapter table](#chapter-overview). It lists the code file and notes for every chapter.

**A starter file fails when I run it.** That is intended: starters and assignment templates have blanks for you to fill. `01-intro-to-recursion.py` ends in a RecursionError on purpose, to show what happens without a stopping condition.

**The PDFs are large.** They are whiteboard notes saved as images. Clone the repository once, or download single files from GitHub.

**Do I need to know recursion before the other DSA topics?** For linked list, trees and dynamic programming, yes. Stack, queue, hashmaps and complexity are friendlier first steps. The [roadmap](roadmap/README.md) shows the order.

**I found a mistake.** Open an [issue](https://github.com/mayank953/hello-dsa/issues) with the file name and what happened.

## Contributing

Corrections and clearer explanations are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Released under the [MIT License](LICENSE). Created by **Mayank Aggarwal**. If this helped you, star the repo and share it with
#HelloDSA.
