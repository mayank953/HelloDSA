# Hello DSA

[![Watch on YouTube](https://img.shields.io/badge/YouTube-Watch%20the%20video-red?logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=BhaHEnpNujI)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Master Data Structures and Algorithms the visual way.** A complete **28-chapter handbook** (recursion to dynamic programming, graphs and the DSA
behind AI), the full code and whiteboard notes from the **Hello DSA** video, auto-checked practice, and a DSA + AI roadmap.
Share your progress with **#HelloDSA**.

> 👋 **Coming from the video?** Every chapter of the video links to its code file and notes in the [chapter table](#chapter-overview),
> and the [recursion folder](recursion/README.md) has everything from the video in one place.
>
> 📘 **Want to go deeper than the video?** The [Hello DSA Handbook](handbook/README.md) explains every topic in the same story-first style, with runnable code.
>
> 🧭 **New to all of this?** Follow the [DSA + AI roadmap](roadmap/README.md).

[![Hello DSA video](https://img.youtube.com/vi/BhaHEnpNujI/maxresdefault.jpg)](https://www.youtube.com/watch?v=BhaHEnpNujI)

## Contents

- [Start here](#start-here) · [Set up](#set-up) · [Prerequisite](#prerequisite-python)
- [The Hello DSA Handbook](#the-hello-dsa-handbook)
- [What the video covers](#what-the-video-covers) · [Chapter overview](#chapter-overview)
- [Recursion: complete code and notes](#recursion-complete-code-and-notes) · [Checkpoint assignments](#checkpoint-assignments)
- [More DSA topics](#more-dsa-topics) · [DSA + AI roadmap](roadmap/README.md)
- [Resources explained](#resources-explained) · [Where to find everything](#where-to-find-everything)
- [Repository layout](#repository-layout) · [FAQ](#faq)

## Start here

1. **Watch** the video and use the timestamps in the [chapter table](#chapter-overview) to jump around.
2. **Read the matching [handbook](handbook/README.md) chapter** for the full explanation (each chapter lists the video timestamps it covers).
3. **Open the topic folder** for the part you are watching. Each one has the code, the notes (PDF) and a page that lists them by chapter.
4. **Run the code yourself**, change it, and break it on purpose.
5. **Test yourself** with the [assignments](assignments/README.md), then compare with the solutions.
6. **Plan what comes next** with the [roadmap](roadmap/README.md).

## Set up

You need Python 3.9 or newer. The recursion code uses only the standard library, so you can run a file with one command:

```bash
git clone https://github.com/mayank953/HelloDSA.git
cd HelloDSA
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

## The Hello DSA Handbook

The video teaches recursion in depth. The **handbook** takes the same teaching style across the *whole* subject: foundations, recursion and
backtracking, every core data structure, sorting and searching, dynamic programming, greedy algorithms, an interview playbook, and how it all
shows up inside AI systems. Every code example is executed when this repository is built, so the outputs you read are real.

### Part 1: Foundations

| # | Chapter | Level | Read | What you will learn |
|---|---|---|---|---|
| 1 | [What Are Data Structures and Algorithms?](handbook/01-what-is-dsa.md) | Beginner | 8 min | Why DSA still matters, what a data structure and an algorithm really are, and the eight-step Hello DSA Method you will reuse on every problem. |
| 2 | [Python You Need for DSA](handbook/02-python-for-dsa.md) | Beginner | 6 min | How a function call really works in memory (the call stack), references and mutability, slicing costs, and the Python habits that make DSA code clean. |
| 3 | [Time Complexity: Counting the Work](handbook/03-time-complexity.md) | Beginner | 9 min | Count steps instead of seconds. Big-O from first principles, loops, nested loops, logarithms, best and worst case, with exact step counts. |
| 4 | [Space Complexity: Counting the Memory](handbook/04-space-complexity.md) | Intermediate | 7 min | Auxiliary space, the memory a recursion uses, the hidden cost of slicing, and the time versus space trade-off. |

### Part 2: Recursion

| # | Chapter | Level | Read | What you will learn |
|---|---|---|---|---|
| 5 | [Recursion From Scratch](handbook/05-recursion-from-scratch.md) | Beginner | 9 min | A function calling itself: the mirror story, the call stack frame by frame, the base case, stack overflow and Python's recursion limit. |
| 6 | [PMI and the Recursion Recipe](handbook/06-pmi-and-the-recursion-recipe.md) | Beginner | 10 min | Why recursion works (mathematical induction) and the three-part recipe: base case, assume, do your part. Applied to sum, power, digits and GCD. |
| 7 | [Fibonacci and Recursion Trees](handbook/07-fibonacci-and-recursion-trees.md) | Intermediate | 7 min | Draw the recursion tree, count the calls, see why naive Fibonacci explodes, and meet memoization for the first time. |
| 8 | [Head vs Tail Recursion and the Order of Work](handbook/08-head-vs-tail-recursion.md) | Intermediate | 7 min | Why swapping two lines flips the output, the print 1 to N and N to 1 pair, tail recursion with an accumulator, and what Python does (and does not do) about it. |
| 9 | [Recursion on Arrays](handbook/09-recursion-on-arrays.md) | Intermediate | 9 min | Shrink the list by one, trust the recursive call, combine. Sum, sorted check, first and last index, and the four ways to return many answers. |
| 10 | [Searching and Sorting with Recursion](handbook/10-searching-and-sorting-with-recursion.md) | Intermediate | 10 min | Linear and binary search, merge sort (divide, conquer, merge) and quick sort (pivot and partition), with the recurrences that give their running time. |
| 11 | [Recursion on Strings](handbook/11-recursion-on-strings.md) | Intermediate | 7 min | Remove a character, palindromes, and the take-or-skip idea behind subsequences, with the wedding-plate story. |
| 12 | [The Choices Tree: Permutations, Codes, Keypads and Hanoi](handbook/12-the-choices-tree.md) | Advanced | 11 min | Problems where every step offers several choices. Permutations, decoding digit strings, phone keypad words, and the Tower of Hanoi. |
| 13 | [Backtracking: Choose, Explore, Undo](handbook/13-backtracking.md) | Advanced | 9 min | The pattern behind N-Queens, subsets with a target sum, combinations, balanced brackets and maze paths. Choose, explore, undo. |

### Part 3: Data Structures

| # | Chapter | Level | Read | What you will learn |
|---|---|---|---|---|
| 14 | [Arrays and Lists](handbook/14-arrays-and-lists.md) | Beginner | 8 min | How a dynamic array works, why append is cheap on average, and the patterns every array question uses: prefix sums, two pointers, sliding window, Kadane. |
| 15 | [Linked Lists](handbook/15-linked-list.md) | Intermediate | 8 min | Nodes and pointers, insert and delete, reversing, the slow and fast pointer trick, cycle detection and merging, with the recursion view. |
| 16 | [Stacks](handbook/16-stack.md) | Intermediate | 8 min | Last in, first out: implementation, balanced brackets, the monotonic stack, evaluating expressions, and why recursion is a stack in disguise. |
| 17 | [Queues and Deques](handbook/17-queue-and-deque.md) | Intermediate | 6 min | First in, first out: circular queues, deques, a queue from two stacks, and the sliding window maximum. |
| 18 | [Hashmaps](handbook/18-hashmaps.md) | Intermediate | 8 min | Hash functions, collisions, chaining and linear probing, load factor, and the classic patterns: frequency counting, two-sum, grouping anagrams. |
| 19 | [Trees and Binary Trees](handbook/19-trees.md) | Intermediate | 9 min | Tree vocabulary, recursive thinking on trees, the four traversals, height, diameter, and the questions that use them. |
| 20 | [Binary Search Trees](handbook/20-binary-search-trees.md) | Intermediate | 8 min | Search, insert and delete in a BST, validating one, finding the lowest common ancestor, and why balance matters. |
| 21 | [Heaps and Priority Queues](handbook/21-heaps.md) | Intermediate | 8 min | The always-ready minimum: heapify, push and pop, heap sort, and top-k problems with Python's heapq. |
| 22 | [Graphs](handbook/22-graphs.md) | Advanced | 10 min | Representations, breadth-first and depth-first search, connected components, cycle detection, topological sort and shortest paths. |

### Part 4: Algorithms

| # | Chapter | Level | Read | What you will learn |
|---|---|---|---|---|
| 23 | [Sorting Algorithms Compared](handbook/23-sorting-compared.md) | Intermediate | 8 min | Bubble, selection, insertion, merge, quick and counting sort side by side: how they work, what they cost, which are stable. |
| 24 | [Binary Search Beyond Sorted Arrays](handbook/24-binary-search-beyond.md) | Advanced | 8 min | Lower and upper bound, rotated arrays, and binary search on the answer. |
| 25 | [Dynamic Programming](handbook/25-dynamic-programming.md) | Advanced | 12 min | From recursion with a memory to tables: climbing stairs, house robber, coin change, knapsack, longest common subsequence, edit distance. |
| 26 | [Greedy Algorithms](handbook/26-greedy.md) | Intermediate | 10 min | Pick the best-looking choice at every step, when that is provably enough, and when it quietly fails. |
| 27 | [Patterns and the Interview Playbook](handbook/27-patterns-and-interview-playbook.md) | Intermediate | 11 min | Eleven patterns that cover most questions, a checklist for the first five minutes of an interview, and a practice plan. |

### Part 5: DSA in the AI Era

| # | Chapter | Level | Read | What you will learn |
|---|---|---|---|---|
| 28 | [DSA Behind AI](handbook/28-dsa-behind-ai.md) | Intermediate | 10 min | Top-k with a heap, similarity search, LRU caches, tries for tokenizers, graphs for knowledge, queues for batching, and cost thinking for model calls. |

[Open the handbook](handbook/README.md) for learning paths (following the video, interview preparation, struggling with recursion, and more).

## What the video covers

The video starts with an introduction to data structures and algorithms and then goes deep on recursion in four topics.

| # | Topic | Starts at | What you get |
|---|---|---|---|
| 1 | [Introduction to Recursion](recursion/01-introduction-to-recursion/) | [`0:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=0s) | 12 code files, 9 PDFs, 2 notebooks, a checkpoint |
| 2 | [Recursion and Arrays](recursion/02-recursion-and-arrays/) | [`2:50:40`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10240s) | 7 code files, 1 PDF, 1 notebook, a checkpoint |
| 3 | [Searching and Sorting with Recursion](recursion/03-searching-and-sorting/) | [`5:35:08`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=20108s) | 6 code files, 0 PDFs, 3 notebooks, a checkpoint |
| 4 | [Recursion and Strings](recursion/04-recursion-and-strings/) | [`7:46:50`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=28010s) | 10 code files, 1 PDF, 7 notebooks, a checkpoint |

## Chapter overview

All 48 chapters, each linked to the code and notes that go with it.

<details>
<summary><b>Show the full chapter table</b></summary>

| Time | Chapter | Code and notes |
|------|---------|----------------|
| [`0:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=0s) | Welcome: why DSA still matters | — |
| [`2:21`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=141s) | What are data structures? | [📄 `introduction-to-data-structures.pdf`](recursion/01-introduction-to-recursion/notes/introduction-to-data-structures.pdf) |
| [`15:05`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=905s) | What is an algorithm? | [📄 `introduction-to-data-structures.pdf`](recursion/01-introduction-to-recursion/notes/introduction-to-data-structures.pdf) |
| [`22:10`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=1330s) | Why companies and software need DSA | — |
| [`24:38`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=1478s) | Why we start with recursion | — |
| [`26:19`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=1579s) | Revision: how functions work | — |
| [`29:55`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=1795s) | A function calling another function (the call stack) | [💻 `01-intro-to-recursion.py`](recursion/01-introduction-to-recursion/code/01-intro-to-recursion.py) · [📄 `01-intro-to-recursion.pdf`](recursion/01-introduction-to-recursion/notes/01-intro-to-recursion.pdf) |
| [`41:40`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=2500s) | A function calling itself | [💻 `02-function-calling-itself.py`](recursion/01-introduction-to-recursion/code/02-function-calling-itself.py) · [📄 `02-function-calling-itself.pdf`](recursion/01-introduction-to-recursion/notes/02-function-calling-itself.pdf) |
| [`46:15`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=2775s) | Adding a stop: how the calls return | [💻 `02-function-calling-itself.py`](recursion/01-introduction-to-recursion/code/02-function-calling-itself.py) |
| [`48:55`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=2935s) | What is recursion? (the mirror analogy) | — |
| [`53:05`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=3185s) | Factorial: thinking recursively | [💻 `03-factorial.py`](recursion/01-introduction-to-recursion/code/03-factorial.py) · [📄 `03-factorial-and-recursion.pdf`](recursion/01-introduction-to-recursion/notes/03-factorial-and-recursion.pdf) |
| [`1:04:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=3840s) | Stack memory and stack overflow | [💻 `03-factorial.py`](recursion/01-introduction-to-recursion/code/03-factorial.py) |
| [`1:16:51`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=4611s) | PMI: principle of mathematical induction | [💻 `04-pmi-and-recursion.py`](recursion/01-introduction-to-recursion/code/04-pmi-and-recursion.py) · [📄 `04-understanding-pmi.pdf`](recursion/01-introduction-to-recursion/notes/04-understanding-pmi.pdf) |
| [`1:32:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=5520s) | From PMI to a recursion recipe | — |
| [`1:37:01`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=5821s) | Sum of the first N numbers | [💻 `05-sum-of-n-natural-numbers.py`](recursion/01-introduction-to-recursion/code/05-sum-of-n-natural-numbers.py) · [📄 `05-sum-of-natural-numbers.pdf`](recursion/01-introduction-to-recursion/notes/05-sum-of-natural-numbers.pdf) |
| [`1:46:56`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=6416s) | Number of digits | [💻 `06-number-of-digits.py`](recursion/01-introduction-to-recursion/code/06-number-of-digits.py) |
| [`1:55:26`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=6926s) | Fibonacci and the recursion tree | [💻 `07-fibonacci.py`](recursion/01-introduction-to-recursion/code/07-fibonacci.py) · [📄 `06-fibonacci-and-head-vs-tail.pdf`](recursion/01-introduction-to-recursion/notes/06-fibonacci-and-head-vs-tail.pdf) |
| [`2:21:33`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=8493s) | Print 1 to N and N to 1 | [💻 `08-print-1-to-n.py`](recursion/01-introduction-to-recursion/code/08-print-1-to-n.py) · [💻 `08-print-n-to-1.py`](recursion/01-introduction-to-recursion/code/08-print-n-to-1.py) |
| [`2:32:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=9120s) | Head vs tail recursion | [💻 `09-head-vs-tail-recursion.py`](recursion/01-introduction-to-recursion/code/09-head-vs-tail-recursion.py) |
| [`2:38:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=9480s) | Recursion in a classroom: kids and notebooks | — |
| [`2:43:48`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=9828s) | Assignments: sum of digits and power | [🧩 `10-assignment-sum-of-digits.py`](recursion/01-introduction-to-recursion/code/10-assignment-sum-of-digits.py) · [🧩 `11-assignment-power-of-a-number.py`](recursion/01-introduction-to-recursion/code/11-assignment-power-of-a-number.py) |
| [`2:50:40`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10240s) | Recursion with arrays: shrinking the problem | [📄 `recursion-and-arrays.pdf`](recursion/02-recursion-and-arrays/notes/recursion-and-arrays.pdf) |
| [`3:00:55`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10855s) | Sum of an array | [💻 `01-sum-of-array.py`](recursion/02-recursion-and-arrays/code/01-sum-of-array.py) |
| [`3:30:15`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=12615s) | Check if an array is sorted | [💻 `02-check-if-array-is-sorted.py`](recursion/02-recursion-and-arrays/code/02-check-if-array-is-sorted.py) |
| [`3:54:50`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=14090s) | First and last index of an element | [💻 `03-first-and-last-index.py`](recursion/02-recursion-and-arrays/code/03-first-and-last-index.py) |
| [`4:20:06`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=15606s) | All indices of a number | [💻 `04-all-indices-of-a-number.py`](recursion/02-recursion-and-arrays/code/04-all-indices-of-a-number.py) |
| [`4:32:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=16320s) | Optimisation: pass an index instead of slicing | [💻 `04-all-indices-of-a-number.py`](recursion/02-recursion-and-arrays/code/04-all-indices-of-a-number.py) |
| [`4:43:30`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=17010s) | Collecting answers in a list passed down | [💻 `05-collect-indices-in-a-passed-list.py`](recursion/02-recursion-and-arrays/code/05-collect-indices-in-a-passed-list.py) |
| [`4:58:30`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=17910s) | Collecting answers in a global list | [💻 `06-collect-indices-in-a-global-list.py`](recursion/02-recursion-and-arrays/code/06-collect-indices-in-a-global-list.py) |
| [`5:04:55`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=18295s) | Returning a new list | [💻 `07-return-indices-as-a-new-list.py`](recursion/02-recursion-and-arrays/code/07-return-indices-as-a-new-list.py) |
| [`5:35:08`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=20108s) | Linear search with recursion | [💻 `01-linear-search.py`](recursion/03-searching-and-sorting/code/01-linear-search.py) |
| [`5:50:54`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=21054s) | Binary search with recursion | [💻 `02-binary-search.py`](recursion/03-searching-and-sorting/code/02-binary-search.py) |
| [`6:12:30`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=22350s) | Merge sort: the idea | [🧩 `03-merge-sort-starter.py`](recursion/03-searching-and-sorting/code/03-merge-sort-starter.py) |
| [`6:27:56`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=23276s) | Merge sort: the approach step by step | [🧩 `03-merge-sort-starter.py`](recursion/03-searching-and-sorting/code/03-merge-sort-starter.py) |
| [`6:40:05`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=24005s) | Merge sort: code and debugging | [💻 `04-merge-sort.py`](recursion/03-searching-and-sorting/code/04-merge-sort.py) |
| [`7:11:17`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=25877s) | Quick sort: pivot and partition | [🧩 `05-quick-sort-starter.py`](recursion/03-searching-and-sorting/code/05-quick-sort-starter.py) |
| [`7:25:10`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=26710s) | Quick sort: code | [💻 `06-quick-sort.py`](recursion/03-searching-and-sorting/code/06-quick-sort.py) |
| [`7:46:50`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=28010s) | Recursion with strings: remove a character | [💻 `01-remove-a-character.py`](recursion/04-recursion-and-strings/code/01-remove-a-character.py) · [📄 `recursion-strings-and-questions.pdf`](recursion/04-recursion-and-strings/notes/recursion-strings-and-questions.pdf) |
| [`8:03:10`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=28990s) | Palindrome check | [💻 `02-palindrome.py`](recursion/04-recursion-and-strings/code/02-palindrome.py) |
| [`8:30:09`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=30609s) | Substring vs subsequence | [🧩 `03-strings-substring-subsequence-starter.py`](recursion/04-recursion-and-strings/code/03-strings-substring-subsequence-starter.py) |
| [`8:36:04`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=30964s) | Print all subsequences | [💻 `04-print-all-subsequences.py`](recursion/04-recursion-and-strings/code/04-print-all-subsequences.py) |
| [`8:55:10`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=32110s) | Return all subsequences | [💻 `05-return-all-subsequences.py`](recursion/04-recursion-and-strings/code/05-return-all-subsequences.py) |
| [`9:11:19`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=33079s) | Permutations: print them | [💻 `06-print-permutations.py`](recursion/04-recursion-and-strings/code/06-print-permutations.py) |
| [`9:34:25`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=34465s) | Permutations: return them | [💻 `07-return-permutations.py`](recursion/04-recursion-and-strings/code/07-return-permutations.py) |
| [`9:50:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=35400s) | Return all codes | [💻 `08-return-all-codes.py`](recursion/04-recursion-and-strings/code/08-return-all-codes.py) |
| [`10:28:10`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=37690s) | Words from a phone number | [💻 `09-words-from-a-phone-number.py`](recursion/04-recursion-and-strings/code/09-words-from-a-phone-number.py) |
| [`10:49:58`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=38998s) | Tower of Hanoi | [💻 `10-tower-of-hanoi.py`](recursion/04-recursion-and-strings/code/10-tower-of-hanoi.py) |
| [`11:08:12`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=40092s) | Wrap-up | — |

</details>

## Recursion: complete code and notes

Open a topic to see its chapters, every code file with a description, the PDF notes with page counts, the class notebooks and practice tasks.

| # | Topic | Starts at | What you get |
|---|---|---|---|
| 1 | [Introduction to Recursion](recursion/01-introduction-to-recursion/) | [`0:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=0s) | 12 code files, 9 PDFs, 2 notebooks, a checkpoint |
| 2 | [Recursion and Arrays](recursion/02-recursion-and-arrays/) | [`2:50:40`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10240s) | 7 code files, 1 PDF, 1 notebook, a checkpoint |
| 3 | [Searching and Sorting with Recursion](recursion/03-searching-and-sorting/) | [`5:35:08`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=20108s) | 6 code files, 0 PDFs, 3 notebooks, a checkpoint |
| 4 | [Recursion and Strings](recursion/04-recursion-and-strings/) | [`7:46:50`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=28010s) | 10 code files, 1 PDF, 7 notebooks, a checkpoint |

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

### Practice sets for the rest of the handbook

More auto-checked notebooks, one set for each group of chapters:

| Practice set | Covers | Problems | Starter | Solutions |
|---|---|---|---|---|
| Backtracking and Binary Search | Handbook chapters 13 and 24 | 6 | [notebook](assignments/B1-backtracking-and-search.ipynb) | [solutions](assignments/solutions/B1-backtracking-and-search.ipynb) |
| Linked Lists, Stacks and Queues | Handbook chapters 15 to 17 | 6 | [notebook](assignments/B2-lists-stacks-queues.ipynb) | [solutions](assignments/solutions/B2-lists-stacks-queues.ipynb) |
| Hashmaps, Trees and Heaps | Handbook chapters 18 to 21 | 7 | [notebook](assignments/B3-hashmaps-trees-heaps.ipynb) | [solutions](assignments/solutions/B3-hashmaps-trees-heaps.ipynb) |
| Graphs, Dynamic Programming and Greedy | Handbook chapters 22, 25 and 26 | 7 | [notebook](assignments/B4-graphs-dp-greedy.ipynb) | [solutions](assignments/solutions/B4-graphs-dp-greedy.ipynb) |

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
| [Hello Python: the Python course](https://github.com/mayank953/python-ai-crash-course) | The free Python course this DSA series builds on. Use it if functions, scope or slicing feel shaky. | Prerequisite | [`26:19`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=1579s) |
| [Hello Python: functions](https://github.com/mayank953/python-ai-crash-course/tree/main/python/37-intro-to-functions) | Lessons 37 to 44 cover defining functions, arguments, scope, lambda, map, filter and reduce. | Chapters on functions and the call stack | [`26:19`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=1579s) |
| [Hello Python: variable scope](https://github.com/mayank953/python-ai-crash-course/tree/main/python/41-variable-scope) | Local versus global variables. It matters for the global-list approach. | Collecting answers in a global list | [`4:58:30`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=17910s) |
| [Hello Python: slicing](https://github.com/mayank953/python-ai-crash-course/tree/main/python/09-concatenation-slicing) | Slicing with start, stop and step, used all through the arrays and strings topics. | Recursion with arrays and strings | [`2:50:40`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10240s) |
| [Python docs: sys.setrecursionlimit](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit) | Why Python stops a runaway recursion and how the limit can be changed. | Stack memory and stack overflow | [`1:04:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=3840s) |
| [Tower of Hanoi animation](https://yongdanielliang.github.io/animation/web/TowerOfHanoi.html) | An interactive animation. Pick the number of disks and watch the moves. | Tower of Hanoi | [`10:49:58`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=38998s) |
| [LeetCode: Pow(x, n)](https://leetcode.com/problems/powx-n/) | A harder version of the power assignment (negative exponents, very large inputs). | Assignments: sum of digits and power | [`2:43:48`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=9828s) |
| [LeetCode: Add Digits](https://leetcode.com/problems/add-digits/) | A related digit problem: keep adding the digits until one digit is left. | Assignments: sum of digits and power | [`2:43:48`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=9828s) |
| [Desmos graph of growth rates](https://www.desmos.com/calculator/l99rykuzx8) | Plot O(1), O(log n), O(n), O(n log n) and O(n^2) to see how quickly each one grows. | Time and space complexity |  |
| [Big-O Cheat Sheet](https://www.bigocheatsheet.com) | One-page summary of the complexity of common algorithms and data structures. | Time and space complexity |  |
| [BST animation](https://yongdanielliang.github.io/animation/web/BST.html) | Watch inserts, searches and deletes on a binary search tree step by step. | Trees |  |

> Some of these sites block automated link checkers. If one does not open, search for its title.

## Where to find everything

| You want | Go to |
|---|---|
| A full explanation of a topic, with runnable code | The [handbook](handbook/README.md) |
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
HelloDSA/
├── README.md                 you are here
├── INDEX.md                  every file and link in one table
├── requirements.txt          jupyterlab, numpy, matplotlib
├── handbook/                 28 chapters with runnable code (handbook/code/)
├── roadmap/                  the DSA + AI roadmap
├── recursion/                the video: code, notes, notebooks
│   ├── 01-introduction-to-recursion/   code/ notes/ notebooks/ solutions/
│   ├── 02-recursion-and-arrays/
│   ├── 03-searching-and-sorting/
│   ├── 04-recursion-and-strings/
│   └── notes/                long recursion notes (PDF)
├── assignments/              four checkpoints, four practice sets and solutions
├── dsa-topics/               arrays, complexity, linked list, stack, queue, trees, hashmaps, DP
└── scripts/                  maintainer tooling (learners can ignore)
```

The repository holds 124 code files and notebooks and 34 PDFs.

## FAQ

**How is the handbook different from the video?** The video teaches recursion with live coding; the handbook covers the whole subject in written form with the same story-first approach, and adds backtracking, data structures, graphs, DP, greedy, patterns and DSA for AI. Each chapter says which video timestamps it matches.

**Which file matches the part of the video I am on?** Use the [chapter table](#chapter-overview). It lists the code file and notes for every chapter.

**A starter file fails when I run it.** That is intended: starters and assignment templates have blanks for you to fill. `01-intro-to-recursion.py` ends in a RecursionError on purpose, to show what happens without a stopping condition.

**The PDFs are large.** They are whiteboard notes saved as images. Clone the repository once, or download single files from GitHub.

**Do I need to know recursion before the other DSA topics?** For linked list, trees and dynamic programming, yes. Stack, queue, hashmaps and complexity are friendlier first steps. The [roadmap](roadmap/README.md) shows the order.

**I found a mistake.** Open an [issue](https://github.com/mayank953/HelloDSA/issues) with the file name and what happened.

## Contributing

Corrections and clearer explanations are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Released under the [MIT License](LICENSE). Created by **Mayank Aggarwal**. If this helped you, star the repo and share it with
#HelloDSA.
