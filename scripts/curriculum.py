"""Single source of truth for the Hello DSA repository layout.

* CHAPTERS : the video chapters (timestamp, title, topic, code files shown in that chapter)
* TOPICS   : the four recursion topics from the video, with their code, notes and notebooks
* SUBJECTS : more DSA topics (complexity, linked list, stack, queue, trees, hashmaps, ...)

Source paths are relative to the folder that holds "DSA Course" and "DSA Reference".
Timestamps come from reading the video transcript, so spot-check them against the video.
"""
from dataclasses import dataclass, field

CODE, TEMPLATE, NOTEBOOK, NOTES, SOLUTION = "code", "starter", "notebook", "notes", "solution"

REF = "DSA Reference/"
COURSE = "DSA Course/"
R1 = REF + "Recursion - Rerecord/1. Recursion/"
RREF = REF + "Recursion - Rerecord/Recursion - Ref/"
TS_SRC = REF + "Recursion - Rerecord/2. Time and Space Complexity/"
SP_SRC = REF + "Recursion - Rerecord/3. Space Complexity/"


@dataclass
class F:
    src: str      # path relative to the source root
    dest: str     # path relative to the topic/subject folder
    kind: str
    desc: str = ""


@dataclass
class Topic:
    key: str
    folder: str
    title: str
    blurb: str
    files: list = field(default_factory=list)
    tasks: list = field(default_factory=list)


@dataclass
class Subject:
    folder: str
    title: str
    blurb: str
    files: list = field(default_factory=list)
    links: list = field(default_factory=list)   # (label, url, what it is)
    prereq: str = ""


# ----------------------------------------------------------------------------- chapters
# (timestamp, title, topic key, code files shown in this chapter)
CHAPTERS = [
    ("0:00", "Welcome: why DSA still matters", "intro", []),
    ("2:21", "What are data structures?", "intro", ["notes:introduction-to-data-structures.pdf"]),
    ("15:05", "What is an algorithm?", "intro", ["notes:introduction-to-data-structures.pdf"]),
    ("22:10", "Why companies and software need DSA", "intro", []),
    ("24:38", "Why we start with recursion", "intro", []),
    ("26:19", "Revision: how functions work", "intro", []),
    ("29:55", "A function calling another function (the call stack)", "intro", ["code:01-intro-to-recursion.py", "notes:01-intro-to-recursion.pdf"]),
    ("41:40", "A function calling itself", "intro", ["code:02-function-calling-itself.py", "notes:02-function-calling-itself.pdf"]),
    ("46:15", "Adding a stop: how the calls return", "intro", ["code:02-function-calling-itself.py"]),
    ("48:55", "What is recursion? (the mirror analogy)", "intro", []),
    ("53:05", "Factorial: thinking recursively", "intro", ["code:03-factorial.py", "notes:03-factorial-and-recursion.pdf"]),
    ("1:04:00", "Stack memory and stack overflow", "intro", ["code:03-factorial.py"]),
    ("1:16:51", "PMI: principle of mathematical induction", "intro", ["code:04-pmi-and-recursion.py", "notes:04-understanding-pmi.pdf"]),
    ("1:32:00", "From PMI to a recursion recipe", "intro", []),
    ("1:37:01", "Sum of the first N numbers", "intro", ["code:05-sum-of-n-natural-numbers.py", "notes:05-sum-of-natural-numbers.pdf"]),
    ("1:46:56", "Number of digits", "intro", ["code:06-number-of-digits.py"]),
    ("1:55:26", "Fibonacci and the recursion tree", "intro", ["code:07-fibonacci.py", "notes:06-fibonacci-and-head-vs-tail.pdf"]),
    ("2:21:33", "Print 1 to N and N to 1", "intro", ["code:08-print-1-to-n.py", "code:08-print-n-to-1.py"]),
    ("2:32:00", "Head vs tail recursion", "intro", ["code:09-head-vs-tail-recursion.py"]),
    ("2:38:00", "Recursion in a classroom: kids and notebooks", "intro", []),
    ("2:43:48", "Assignments: sum of digits and power", "intro", ["code:10-assignment-sum-of-digits.py", "code:11-assignment-power-of-a-number.py"]),
    ("2:50:40", "Recursion with arrays: shrinking the problem", "arrays", ["notes:recursion-and-arrays.pdf"]),
    ("3:00:55", "Sum of an array", "arrays", ["code:01-sum-of-array.py"]),
    ("3:30:15", "Check if an array is sorted", "arrays", ["code:02-check-if-array-is-sorted.py"]),
    ("3:54:50", "First and last index of an element", "arrays", ["code:03-first-and-last-index.py"]),
    ("4:20:06", "All indices of a number", "arrays", ["code:04-all-indices-of-a-number.py"]),
    ("4:32:00", "Optimisation: pass an index instead of slicing", "arrays", ["code:04-all-indices-of-a-number.py"]),
    ("4:43:30", "Collecting answers in a list passed down", "arrays", ["code:05-collect-indices-in-a-passed-list.py"]),
    ("4:58:30", "Collecting answers in a global list", "arrays", ["code:06-collect-indices-in-a-global-list.py"]),
    ("5:04:55", "Returning a new list", "arrays", ["code:07-return-indices-as-a-new-list.py"]),
    ("5:35:08", "Linear search with recursion", "search-sort", ["code:01-linear-search.py"]),
    ("5:50:54", "Binary search with recursion", "search-sort", ["code:02-binary-search.py"]),
    ("6:12:30", "Merge sort: the idea", "search-sort", ["code:03-merge-sort-starter.py"]),
    ("6:27:56", "Merge sort: the approach step by step", "search-sort", ["code:03-merge-sort-starter.py"]),
    ("6:40:05", "Merge sort: code and debugging", "search-sort", ["code:04-merge-sort.py"]),
    ("7:11:17", "Quick sort: pivot and partition", "search-sort", ["code:05-quick-sort-starter.py"]),
    ("7:25:10", "Quick sort: code", "search-sort", ["code:06-quick-sort.py"]),
    ("7:46:50", "Recursion with strings: remove a character", "strings", ["code:01-remove-a-character.py", "notes:recursion-strings-and-questions.pdf"]),
    ("8:03:10", "Palindrome check", "strings", ["code:02-palindrome.py"]),
    ("8:30:09", "Substring vs subsequence", "strings", ["code:03-strings-substring-subsequence-starter.py"]),
    ("8:36:04", "Print all subsequences", "strings", ["code:04-print-all-subsequences.py"]),
    ("8:55:10", "Return all subsequences", "strings", ["code:05-return-all-subsequences.py"]),
    ("9:11:19", "Permutations: print them", "strings", ["code:06-print-permutations.py"]),
    ("9:34:25", "Permutations: return them", "strings", ["code:07-return-permutations.py"]),
    ("9:50:00", "Return all codes", "strings", ["code:08-return-all-codes.py"]),
    ("10:28:10", "Words from a phone number", "strings", ["code:09-words-from-a-phone-number.py"]),
    ("10:49:58", "Tower of Hanoi", "strings", ["code:10-tower-of-hanoi.py"]),
    ("11:08:12", "Wrap-up", "strings", []),
]

# ----------------------------------------------------------------------------- topics
I1 = R1 + "1. Introduction To Recursion/"
A1 = R1 + "2. Recursion and Arrays/"
S1 = R1 + "3. Recursion - Searching and Sorting/"
T1 = R1 + "4. Recursion and String/"

TOPICS = [
    Topic("intro", "01-introduction-to-recursion", "Introduction to Recursion",
          "Starts with what data structures and algorithms are, then builds recursion from the ground up: function calls and the "
          "call stack, factorial, the principle of mathematical induction, Fibonacci, head versus tail recursion.",
          [
              F(I1 + "1. Intro To Recursion.py", "code/01-intro-to-recursion.py", CODE,
                "Functions that call other functions in a chain, and a `printNum` with no stopping condition. Running this file ends in a RecursionError, which is the point of the demo."),
              F(I1 + "2. function calling itself.py", "code/02-function-calling-itself.py", CODE,
                "`printNum` calling itself with a stopping condition, so the calls return one by one."),
              F(I1 + "3. Factorial with Recursion.py", "code/03-factorial.py", CODE,
                "Recursive factorial, plus the unrolled `factorialone` to `factorialfour` version used to trace the call stack."),
              F(I1 + "4. PMI and Recursion.py", "code/04-pmi-and-recursion.py", CODE,
                "A recursive function for 2 to the power n, written as the PMI plan: base case, induction hypothesis, then the step that uses it."),
              F(I1 + "5. Sum of n natural numbers.py", "code/05-sum-of-n-natural-numbers.py", CODE,
                "Sum of the first N natural numbers with recursion."),
              F(I1 + "6. Number of Digits.py", "code/06-number-of-digits.py", CODE,
                "Counting the digits of a number recursively."),
              F(I1 + "7. Fibonicci.py", "code/07-fibonacci.py", CODE,
                "Fibonacci with two recursive calls (the recursion tree)."),
              F(I1 + "8.Print 1 to N.py", "code/08-print-1-to-n.py", CODE,
                "Print 1 to N: the order of the print and the recursive call decides the output."),
              F(I1 + "8.1 Print N to 1.py", "code/08-print-n-to-1.py", CODE,
                "Print N down to 1."),
              F(I1 + "9. Head vs Tail Recursion.py", "code/09-head-vs-tail-recursion.py", CODE,
                "Factorial as head recursion, a tail attempt that goes wrong, and a correct tail version."),
              F(I1 + "8.2 Assignment - Sum of Digits.py", "code/10-assignment-sum-of-digits.py", TEMPLATE,
                "Assignment template with test cases. Implement `sum_of_digits` recursively."),
              F(I1 + "8.3 Assignment - Power of a number.py", "code/11-assignment-power-of-a-number.py", TEMPLATE,
                "Assignment template with test cases. Implement `power` recursively."),
              F(I1 + "1. Intro To Recursion.pdf", "notes/01-intro-to-recursion.pdf", NOTES, "Whiteboard notes: introduction to recursion."),
              F(I1 + "2. Function Calling itself.pdf", "notes/02-function-calling-itself.pdf", NOTES, "Whiteboard notes: a function calling itself."),
              F(I1 + "3. Factorial & Recursion.pdf", "notes/03-factorial-and-recursion.pdf", NOTES, "Whiteboard notes: factorial and the call stack."),
              F(I1 + "4. Understanding PMI for Recursion.pdf", "notes/04-understanding-pmi.pdf", NOTES, "Whiteboard notes: the principle of mathematical induction."),
              F(I1 + "5. Sum of Natural Numbers till N using Recursion.pdf", "notes/05-sum-of-natural-numbers.pdf", NOTES, "Whiteboard notes: sum of natural numbers."),
              F(I1 + "Fibonicci Number + Head vs Tail Recursion.pdf", "notes/06-fibonacci-and-head-vs-tail.pdf", NOTES, "Whiteboard notes: Fibonacci, head and tail recursion."),
              F(REF + "Intro To Data Structure/Intro To Data Structure.pdf", "notes/introduction-to-data-structures.pdf", NOTES, "Whiteboard notes for the opening on data structures and algorithms."),
              F(COURSE + "Intro To Data Structure/Intro To Data Structure.pdf", "notes/introduction-to-data-structures-v2.pdf", NOTES, "A second version of the data structures and algorithms notes."),
              F(COURSE + "Recursion/Introduction To Recursion/Class 1- Recursion.ipynb", "notebooks/recursion-class-notebook.ipynb", NOTEBOOK,
                "Class notebook with run outputs for the introduction to recursion."),
              F(COURSE + "Recursion/Introduction To Recursion/Assignment Question/Assignment.ipynb", "notebooks/assignment-sum-of-digits.ipynb", NOTEBOOK,
                "Notebook version of the sum of digits assignment."),
              F(COURSE + "Recursion/Introduction To Recursion/Recursion Fibonicci .pdf", "notes/fibonacci-recursion-notes.pdf", NOTES, "Whiteboard notes on Fibonacci recursion (3 pages)."),
          ],
          ["Draw the call stack for `factorial(4)` on paper, then check it against the video at the factorial chapter.",
           "Remove the base case from `02-function-calling-itself.py` and read the RecursionError. Then put it back.",
           "Write `power2(base, n)` from the PMI idea: assume it works for `n - 1`, then use that.",
           "Print the first 10 Fibonacci numbers and count how many calls `fibonacci(5)` makes.",
           "Solve both assignment templates, then compare with the files in `solutions/`."]),
    Topic("arrays", "02-recursion-and-arrays", "Recursion and Arrays",
          "Recursion on lists: shrink the list by one element, trust the recursive call, and combine. Sum, sorted check, first and last index, "
          "and four ways to collect all indices (print, pass a list down, use a global list, return a new list).",
          [
              F(A1 + "2.2 Sum of Array using Recursion.py", "code/01-sum-of-array.py", CODE, "Sum of a list: two head-style versions and a tail version with an accumulator."),
              F(A1 + "2.1 Check if Array is Sorted.py", "code/02-check-if-array-is-sorted.py", CODE, "Two recursive ways to check that a list is in increasing order, tried on a 10,000-element list."),
              F(A1 + "2.3 First and Last Indices of Element.py", "code/03-first-and-last-index.py", CODE, "First and last index of an element; -1 when it is absent."),
              F(A1 + "2.4 All indices of a number.py", "code/04-all-indices-of-a-number.py", CODE, "Print every index of a value, including the better version that passes an index instead of slicing."),
              F(A1 + "2.5 Update in List all Index of An Element.py", "code/05-collect-indices-in-a-passed-list.py", CODE, "Collect the indices in a list that is passed down the calls."),
              F(A1 + "2.6 Update Indices in a Global List.py", "code/06-collect-indices-in-a-global-list.py", CODE, "Collect the indices in a global list."),
              F(A1 + "2.7 Return All indices in a new List.py", "code/07-return-indices-as-a-new-list.py", CODE, "Return the indices as a new list built on the way back."),
              F(A1 + "Recursion and Arrays.pdf", "notes/recursion-and-arrays.pdf", NOTES, "Whiteboard notes for the arrays topic."),
              F(COURSE + "Recursion/Recursion and Arrays/Recursion With Arrays.ipynb", "notebooks/recursion-with-arrays-class-notebook.ipynb", NOTEBOOK,
                "Class notebook with run outputs for recursion with arrays."),
          ],
          ["Write `max_of_list(nums)` recursively, first by slicing and then with an index.",
           "Change `01-sum-of-array.py` to sum only the even numbers.",
           "Return the indices of a value in reverse order.",
           "Explain in one sentence why the global-list version is risky if you call it twice.",
           "Take the checkpoint: `assignments/A2-recursion-and-arrays.ipynb`."]),
    Topic("search-sort", "03-searching-and-sorting", "Searching and Sorting with Recursion",
          "Linear and binary search written recursively, then merge sort and quick sort: how to divide the problem, what the recursive call returns, "
          "and how to merge or partition. Starter scaffolds are included so you can fill in `Merge` and `partitionFunction` yourself.",
          [
              F(S1 + "1. LinearSearchUsingRecursion.py", "code/01-linear-search.py", CODE, "Linear search that returns True or False: one version carries an index, the other combines the answer on the way back."),
              F(S1 + "2. Binary Search using Recursion.py", "code/02-binary-search.py", CODE, "Binary search (True or False) with a helper that carries the start and end positions."),
              F(S1 + "MergeSortIntro.py", "code/03-merge-sort-starter.py", TEMPLATE, "Starter: `MergeSort` is written, `Merge` is left for you to fill in."),
              F(S1 + "3. Merge Sort.py", "code/04-merge-sort.py", CODE, "Complete merge sort (`Merge`, `MergeSortHelper`, `MergeSort`)."),
              F(S1 + "QuickSortIntro.py", "code/05-quick-sort-starter.py", TEMPLATE, "Starter: `QuickSort` is written, `partitionFunction` is left for you to fill in."),
              F(S1 + "4. Quick Sort.py", "code/06-quick-sort.py", CODE, "Complete quick sort with a partition function."),
              F(COURSE + "Recursion/Recursion and Arrays/Searching Using Recursion.ipynb", "notebooks/searching-class-notebook.ipynb", NOTEBOOK, "Class notebook: searching with recursion."),
              F(COURSE + "Recursion/Recursion and Arrays/Merge Sort Using Recursion.ipynb", "notebooks/merge-sort-class-notebook.ipynb", NOTEBOOK, "Class notebook: merge sort."),
              F(COURSE + "Recursion/Recursion and Arrays/QuickSortUsing Recursion.ipynb", "notebooks/quick-sort-class-notebook.ipynb", NOTEBOOK, "Class notebook: quick sort."),
          ],
          ["Count the calls binary search makes on a list of 1,000 sorted numbers.",
           "Finish `Merge` in `03-merge-sort-starter.py` without looking at `04-merge-sort.py`.",
           "Finish `partitionFunction` in `05-quick-sort-starter.py` and test it on a list with duplicates.",
           "Sort the same list with merge sort and quick sort and compare the number of comparisons.",
           "Take the checkpoint: `assignments/A3-searching-and-sorting.ipynb`."]),
    Topic("strings", "04-recursion-and-strings", "Recursion and Strings",
          "Strings and recursion: removing characters, palindromes, subsequences (take or skip), permutations (the plate analogy), decoding digit strings, "
          "phone keypad words, and the Tower of Hanoi. Each problem appears as a print version and a return version where it matters.",
          [
              F(T1 + "1. Recursion With Strings.py", "code/01-remove-a-character.py", CODE, "Remove every occurrence of a character, for example `z` from `abczz`."),
              F(T1 + "2. Palindrome.py", "code/02-palindrome.py", CODE, "Palindrome check with a start and end helper."),
              F(T1 + "3. Strings, Substring and Subsequence.py", "code/03-strings-substring-subsequence-starter.py", TEMPLATE, "Starter: notes on string, substring and subsequence, with an empty `return_subsequences`."),
              F(T1 + "5. Print all subsequences.py", "code/04-print-all-subsequences.py", CODE, "Print every subsequence using a \"taken so far\" parameter."),
              F(T1 + "4. Return Subsequences of a string.py", "code/05-return-all-subsequences.py", CODE, "Return all subsequences as a list."),
              F(T1 + "6. Permutations of a string.py", "code/06-print-permutations.py", CODE, "Print every permutation of a string."),
              F(T1 + "7. Return Permutations of a string.py", "code/07-return-permutations.py", CODE, "Return all permutations as a list."),
              F(T1 + "9. Return All Codes.py", "code/08-return-all-codes.py", CODE, "Decode a digit string into letters (1 is a, 26 is z) and return every possible word."),
              F(T1 + "8. Words from a phone number.py", "code/09-words-from-a-phone-number.py", CODE, "Every word that a phone-keypad number could spell."),
              F(T1 + "10. Tower of hanoi.py", "code/10-tower-of-hanoi.py", CODE, "Tower of Hanoi with a step counter."),
              F(COURSE + "Recursion/Recursion and Strings/Recursion Strings + Questions.pdf", "notes/recursion-strings-and-questions.pdf", NOTES, "Whiteboard notes and questions for strings (16 pages)."),
              F(COURSE + "Recursion/Recursion and Strings/Recursion with Strings.ipynb", "notebooks/recursion-with-strings-class-notebook.ipynb", NOTEBOOK, "Class notebook: recursion with strings."),
              F(COURSE + "Recursion/Recursion and Strings/Subsequences.ipynb", "notebooks/subsequences-class-notebook.ipynb", NOTEBOOK, "Class notebook: subsequences."),
              F(COURSE + "Recursion/Recursion and Strings/Permutations.ipynb", "notebooks/permutations-class-notebook.ipynb", NOTEBOOK, "Class notebook: permutations."),
              F(COURSE + "Recursion/Recursion and Strings/Print Letter Combination.ipynb", "notebooks/letter-combinations-class-notebook.ipynb", NOTEBOOK, "Class notebook: letter combinations from a keypad."),
              F(COURSE + "Recursion/Recursion and Strings/Print and return combinations.ipynb", "notebooks/print-and-return-codes-class-notebook.ipynb", NOTEBOOK, "Class notebook: decoding digits, printing and returning."),
              F(COURSE + "Recursion/Recursion and Strings/Tower Of hanoi.ipynb", "notebooks/tower-of-hanoi-class-notebook.ipynb", NOTEBOOK, "Class notebook: Tower of Hanoi."),
              F(RREF + "Recursion Question Reference/Questions", "notebooks/questions.ipynb", NOTEBOOK, "A longer practice notebook of recursion questions with code (63 cells)."),
          ],
          ["List all subsequences of `\"abcd\"` by hand using take or skip, then check the count (16).",
           "Write `reverse_string(s)` recursively.",
           "Count the permutations of a 4-letter word, then predict the count for 5 letters.",
           "Run `10-tower-of-hanoi.py` for 3, 4 and 5 disks and find the pattern in the number of moves.",
           "Take the checkpoint: `assignments/A4-recursion-and-strings.ipynb`."]),
]

# notes that cover the whole recursion series (shared folder recursion/notes/)
MASTER_NOTES = [
    F(RREF + "Intro To Recursion - ref/Recursion (from Fibonacii) - Youtube.pdf", "recursion-from-fibonacci-youtube.pdf", NOTES, "Full recursion notes, starting from Fibonacci."),
    F(RREF + "Intro To Recursion - ref/Recursion (from Fibonacii) Copy Ref.pdf", "recursion-from-fibonacci-copy-ref.pdf", NOTES, "Recursion notes, reference copy."),
    F(RREF + "Intro To Recursion - ref/Recursion (from Fibonacii) Ref Final.pdf", "recursion-from-fibonacci-ref-final.pdf", NOTES, "Recursion notes, final reference version."),
    F(RREF + "Intro To Recursion - ref/Recursion - Ref Notes.pdf", "recursion-ref-notes.pdf", NOTES, "Short reference notes, including the principle of mathematical induction."),
    F(RREF + "Recursion and String Ref/Recursion (from Fibonacii) Ref.pdf", "recursion-from-fibonacci-ref-with-strings.pdf", NOTES, "Recursion notes that continue into strings."),
    F(COURSE + "Recursion/Recursion and Arrays/Recursion (from Fibonacii) - Youtube.pdf", "recursion-from-fibonacci-34-pages.pdf", NOTES, "The longest set of recursion notes."),
]

# ----------------------------------------------------------------------------- more DSA
LL = REF + "Linked List/"
TR = REF + "Trees/"

SUBJECTS = [
    Subject("arrays", "Arrays",
            "How arrays work under the hood: a short set of notes and a notebook that builds a dynamic array (a Python-list look-alike) from scratch with `ctypes`.",
            [F(REF + "Untitled Folder/Introduction to arrays copy.pdf", "notes/introduction-to-arrays.pdf", NOTES, "Whiteboard notes on arrays."),
             F(REF + "Untitled Folder/Untitled.ipynb", "notebooks/custom-dynamic-array.ipynb", NOTEBOOK, "A `CustomList` built with `ctypes`: resizing, append, indexing.")]),
    Subject("time-and-space-complexity", "Time and Space Complexity",
            "Big-O in practice: how to count the work an algorithm does, why growth rate matters on large inputs, and how recursion uses memory. "
            "Notebooks time real code (merge sort against bubble sort) and plot the growth.",
            [F(TS_SRC + "1. Merge Sort vs Bubble Sort.ipynb", "notebooks/01-merge-sort-vs-bubble-sort.ipynb", NOTEBOOK, "Times merge sort against bubble sort on growing inputs."),
             F(TS_SRC + "2. Large input Understanding.ipynb", "notebooks/02-large-input-understanding.ipynb", NOTEBOOK, "Times bubble sort, fits the time equation, and shows why lower-order terms stop mattering on large inputs."),
             F(TS_SRC + "3. Time Complexity of Algorithms.ipynb", "notebooks/03-time-complexity-of-algorithms.ipynb", NOTEBOOK, "Insertion sort and its time complexity."),
             F(TS_SRC + "Time Complexity Questions With Solutions.ipynb", "notebooks/04-time-complexity-questions-with-solutions.ipynb", NOTEBOOK, "Practice questions on time complexity."),
             F(SP_SRC + "Space Complexity.ipynb", "notebooks/05-space-complexity.ipynb", NOTEBOOK, "Space complexity, using insertion sort as the example."),
             F(COURSE + "Time and Space Complexity/Time and Space Complexity Class.ipynb", "notebooks/time-and-space-complexity-class-notebook.ipynb", NOTEBOOK, "Class notebook for time and space complexity."),
             F(COURSE + "Time and Space Complexity/Time complexity.ipynb", "notebooks/time-complexity-class-notebook.ipynb", NOTEBOOK, "Class notebook with timing experiments."),
             F(COURSE + "Time and Space Complexity/Time complexity Question.ipynb", "notebooks/time-complexity-questions-1.ipynb", NOTEBOOK, "Time complexity questions."),
             F(COURSE + "Time and Space Complexity/Time Complexity Question 2.ipynb", "notebooks/time-complexity-questions-2.ipynb", NOTEBOOK, "More time complexity questions."),
             F(REF + "Time and Space Complexity/Time Complexity Question 2.ipynb", "notebooks/time-complexity-questions-2-reference.ipynb", NOTEBOOK, "Reference version of the second question set."),
             F(TS_SRC + "Complexity Analysis and Time Complexity.pdf", "notes/complexity-analysis-and-time-complexity.pdf", NOTES, "Whiteboard notes on complexity analysis."),
             F(SP_SRC + "Space Complexity.pdf", "notes/space-complexity.pdf", NOTES, "Whiteboard notes on space complexity."),
             F(REF + "Time and Space Complexity/TC & SC Reference.pdf", "notes/time-and-space-complexity-reference.pdf", NOTES, "Reference notes for time and space complexity."),
             F(COURSE + "Time and Space Complexity/Time and space class final.pdf", "notes/time-and-space-class-final.pdf", NOTES, "Class notes for time and space complexity.")],
            links=[("Desmos graph of growth rates", "https://www.desmos.com/calculator/l99rykuzx8", "Plot O(1), O(log n), O(n), O(n log n), O(n^2) and compare how fast they grow."),
                   ("Big-O Cheat Sheet", "https://www.bigocheatsheet.com", "A one-page summary of the complexity of common algorithms and data structures.")]),
    Subject("linked-list", "Linked List",
            "Build a singly linked list step by step: the node, taking input, length, insert, delete and search, each written iteratively and recursively. "
            "The complete code notebook puts everything in one place.",
            [F(LL + "1. Code 1.ipynb", "notebooks/01-creating-a-node.ipynb", NOTEBOOK, "The `Node` class and `print_LL`."),
             F(LL + "2 . Take Input.ipynb", "notebooks/02-take-input.ipynb", NOTEBOOK, "Taking input to build a linked list (`take_input` and the better version)."),
             F(LL + "3. Length of LL.ipynb", "notebooks/03-length.ipynb", NOTEBOOK, "Length of a linked list, iteratively and recursively."),
             F(LL + "4 .Insert in Linked List.ipynb", "notebooks/04-insert.ipynb", NOTEBOOK, "Insert at the head, the tail and an index, each iteratively and recursively."),
             F(LL + "Delete.ipynb", "notebooks/05-delete.ipynb", NOTEBOOK, "Delete at the head, the tail, an index or by value, each iteratively and recursively."),
             F(LL + "Search.ipynb", "notebooks/06-search.ipynb", NOTEBOOK, "Search by value and by index, iteratively and recursively."),
             F(LL + "Complete Code.ipynb", "notebooks/complete-code.ipynb", NOTEBOOK, "All linked list code in one notebook."),
             F(COURSE + "Linked List/Input a LL.ipynb", "notebooks/input-a-linked-list-class-notebook.ipynb", NOTEBOOK, "Class notebook: input of a linked list."),
             F(COURSE + "Linked List/LinkedList.ipynb", "notebooks/linked-list-basics-class-notebook.ipynb", NOTEBOOK, "Class notebook: linked list basics."),
             F(LL + "Linked List.pdf", "notes/linked-list.pdf", NOTES, "Whiteboard notes (22 pages)."),
             F(LL + "Linked List Till Mid.pdf", "notes/linked-list-till-mid.pdf", NOTES, "Whiteboard notes up to the middle of the topic."),
             F(LL + "Linked List Questions + Types.pdf", "notes/linked-list-questions-and-types.pdf", NOTES, "Questions and types of linked lists."),
             F(COURSE + "Linked List/Linked List Part 1.pdf", "notes/linked-list-part-1.pdf", NOTES, "Class notes, part 1.")],
            prereq="Recursion (the main course) helps a lot for the insert and delete chapters."),
    Subject("stack", "Stack",
            "The last-in, first-out structure, built on a list, an array, a dynamic array and a linked list.",
            [F(REF + "Stack/All Stacks Code.ipynb", "notebooks/all-stacks-code.ipynb", NOTEBOOK, "A stack built on a list, an array, a dynamic array and a linked list."),
             F(REF + "Stack/Stack Reference.pdf", "notes/stack-reference.pdf", NOTES, "Whiteboard notes on stacks.")]),
    Subject("queue", "Queue",
            "The first-in, first-out structure, built on an array, a list and a linked list.",
            [F(REF + "Queue/All Code Queue.ipynb", "notebooks/all-code-queue.ipynb", NOTEBOOK, "A queue built on an array, a list and a linked list."),
             F(REF + "Queue/Queue DS Reference.pdf", "notes/queue-reference.pdf", NOTES, "Whiteboard notes on queues.")]),
    Subject("trees", "Trees",
            "Generic trees, binary trees and binary search trees: nodes, traversals (inorder, preorder), and BST operations, nearly all of them recursive.",
            [F(TR + "All Tree Code.ipynb", "notebooks/all-tree-code.ipynb", NOTEBOOK, "Generic trees: printing, input (normal and level-wise), height, nodes at a depth, level-wise print, preorder and postorder."),
             F(TR + "Binary Tree All Codes.ipynb", "notebooks/binary-tree-all-codes.ipynb", NOTEBOOK, "Binary trees: input, level-wise print, preorder, inorder and postorder traversals, height and diameter."),
             F(TR + "Binary Search Tree.ipynb", "notebooks/binary-search-tree.ipynb", NOTEBOOK, "Binary search tree: search, insert, find min and max, and checking whether a tree is a BST."),
             F(TR + "Real World Example Tree.py", "code/real-world-example-tree.py", CODE, "A tree built from a real-world example."),
             F(TR + "Types of Binary Tree.py", "code/types-of-binary-tree.py", CODE, "ASCII diagrams of the types of binary tree (full, perfect, complete, balanced, degenerate). Run it to print them."),
             F(TR + "Generic Trees Ref Notes.pdf", "notes/generic-trees-reference-notes.pdf", NOTES, "Notes on generic trees."),
             F(TR + "Binary Tree Reference Notes.pdf", "notes/binary-tree-reference-notes.pdf", NOTES, "Reference notes on binary trees."),
             F(TR + "Binary Tree.pdf", "notes/binary-tree.pdf", NOTES, "Whiteboard notes on binary trees."),
             F(TR + "inorder and preorder.pdf", "notes/inorder-and-preorder.pdf", NOTES, "Inorder and preorder traversals."),
             F(TR + "Binary Search Tree Reference.pdf", "notes/binary-search-tree-reference.pdf", NOTES, "Reference notes on binary search trees.")],
            links=[("BST animation", "https://yongdanielliang.github.io/animation/web/BST.html", "Watch inserts, searches and deletes on a binary search tree step by step.")],
            prereq="Recursion (the main course): tree code is recursion on nodes."),
    Subject("hashmaps", "Hashmaps",
            "Hash tables from the ground up: hashing, collisions, and open addressing with linear probing.",
            [F(REF + "Hashmaps/Linear Probing.py", "code/linear-probing.py", CODE, "A hash table that resolves collisions with linear probing."),
             F(REF + "Hashmaps/Untitled.ipynb", "notebooks/hashmap-overview.ipynb", NOTEBOOK, "A key-value diagram, hashmap practice functions (frequency count, group anagrams, intersection, duplicates, first non-repeating character) and a `HashMap` class built on a linked list."),
             F(REF + "Hashmaps/Hashmaps Reference.pdf", "notes/hashmaps-reference.pdf", NOTES, "Whiteboard notes on hashmaps.")]),
    Subject("dynamic-programming", "Dynamic Programming",
            "A starting point for dynamic programming: the prerequisites (recursion, lists, 2D lists, indexing) and the Fibonacci recursion that DP optimises.",
            [F(REF + "DP/DP Codes.ipynb", "notebooks/dp-codes.ipynb", NOTEBOOK, "Prerequisites and a recursive Fibonacci to build on.")],
            prereq="Finish the recursion course first."),
]
