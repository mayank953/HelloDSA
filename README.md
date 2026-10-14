# Hello DSA: Recursion 1

[![Watch on YouTube](https://img.shields.io/badge/YouTube-Watch%20the%20video-red?logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=BhaHEnpNujI)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**The complete code, whiteboard notes (PDF), notebooks and checkpoints for the Hello DSA video.** The video introduces data structures and
algorithms and then teaches recursion in four topics. Everything you see on screen is in the [`recursion/`](recursion/README.md) folder,
organised in the order of the video. Share your progress with **#HelloDSA**.

[![Hello DSA video](https://img.youtube.com/vi/BhaHEnpNujI/maxresdefault.jpg)](https://www.youtube.com/watch?v=BhaHEnpNujI)

## Contents

- [Start here](#start-here) · [Set up](#set-up) · [Prerequisite](#prerequisite-python)
- [The four topics](#the-four-topics) · [Chapter overview](#chapter-overview)
- [Checkpoint assignments](#checkpoint-assignments) · [Resources explained](#resources-explained)
- [Where to find everything](#where-to-find-everything) · [Go further](#go-further) · [FAQ](#faq)

## Start here

1. **Watch** the video and use the timestamps in the [chapter table](#chapter-overview) to jump around.
2. **Open the topic folder** for the part you are watching. Each one has the code, the notes (PDF), the notebooks and a page that lists them by chapter.
3. **Run the code yourself**, change it, and break it on purpose.
4. **Test yourself** with the [checkpoint assignments](assignments/README.md), then compare with the solutions.
5. **Want more?** See [Go further](#go-further) for the handbook, other DSA topics and the roadmap.

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

## The four topics

Open a topic to see its chapters, every code file with a description, the PDF notes with page counts, the class notebooks and practice tasks.

| # | Topic | Starts at | What you get |
|---|---|---|---|
| 1 | [Introduction to Recursion](recursion/01-introduction-to-recursion/) | [`0:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=0s) | 12 code files, 9 PDFs, 2 notebooks, a checkpoint |
| 2 | [Recursion and Arrays](recursion/02-recursion-and-arrays/) | [`2:50:40`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10240s) | 7 code files, 1 PDF, 1 notebook, a checkpoint |
| 3 | [Searching and Sorting with Recursion](recursion/03-searching-and-sorting/) | [`5:35:08`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=20108s) | 6 code files, 0 PDFs, 3 notebooks, a checkpoint |
| 4 | [Recursion and Strings](recursion/04-recursion-and-strings/) | [`7:46:50`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=28010s) | 10 code files, 1 PDF, 7 notebooks, a checkpoint |

The longer notes that run across the whole video are listed on the [recursion page](recursion/README.md#notes-that-cover-the-whole-series).

## Chapter overview

All 48 chapters of the video, each linked to the code and notes that go with it.

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
| The code for a video chapter | The [chapter table](#chapter-overview) above, or the topic page in [`recursion/`](recursion/) |
| The whiteboard notes (PDF) | `notes/` inside each topic, or [`recursion/notes/`](recursion/notes/) for the long notes |
| A runnable notebook with outputs | `notebooks/` inside each topic |
| Practice with instant feedback | [`assignments/`](assignments/README.md) |
| Every file and link in one table | [INDEX.md](INDEX.md) |

**Tips:** PDFs open in the browser on GitHub. For long PDFs, download the file for faster scrolling. Notebook and code file names start with a number that follows the video order.

## Go further

Once the recursion material feels comfortable, these sections take the same teaching style across the rest of DSA.

| Section | What it is |
|---|---|
| [Hello DSA Handbook](handbook/README.md) | 28 written chapters with runnable code: recursion and backtracking in more depth, every core data structure, sorting, dynamic programming, greedy algorithms, an interview playbook and DSA behind AI. |
| [More DSA topics](dsa-topics/README.md) | Notes and code for arrays, complexity, linked list, stack, queue, trees, hashmaps and dynamic programming. |
| [Practice sets](assignments/README.md#practice-sets-the-rest-of-the-handbook) | Auto-checked notebooks for backtracking, binary search, lists, stacks, queues, hashmaps, trees, heaps, graphs, DP and greedy. |
| [DSA + AI roadmap](roadmap/README.md) | A step-by-step study plan from your first loop to DSA for AI systems, with a 12-week schedule. |

## Repository layout

```
HelloDSA/
├── README.md                 you are here
├── INDEX.md                  every file and link in one table
├── requirements.txt          jupyterlab, numpy, matplotlib
├── recursion/                the video: code, notes, notebooks
│   ├── 01-introduction-to-recursion/   code/ notes/ notebooks/ solutions/
│   ├── 02-recursion-and-arrays/
│   ├── 03-searching-and-sorting/
│   ├── 04-recursion-and-strings/
│   └── notes/                long recursion notes (PDF)
├── assignments/              checkpoints for the video, plus further practice sets and solutions
├── handbook/                 28 chapters with runnable code
├── dsa-topics/               arrays, complexity, linked list, stack, queue, trees, hashmaps, DP
├── roadmap/                  the DSA + AI roadmap
└── scripts/                  maintainer tooling (learners can ignore)
```

The repository holds 124 code files and notebooks and 34 PDFs.

## FAQ

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
