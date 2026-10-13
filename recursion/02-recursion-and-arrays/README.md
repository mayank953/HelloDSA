# 2. Recursion and Arrays

Recursion on lists: shrink the list by one element, trust the recursive call, and combine. Sum, sorted check, first and last index, and four ways to collect all indices (print, pass a list down, use a global list, return a new list).

**Video:** starts at [`2:50:40`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10240s)

## Chapters

| Time | Chapter | Code and notes |
|------|---------|----------------|
| [`2:50:40`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10240s) | Recursion with arrays: shrinking the problem | [📄 `recursion-and-arrays.pdf`](notes/recursion-and-arrays.pdf) |
| [`3:00:55`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=10855s) | Sum of an array | [💻 `01-sum-of-array.py`](code/01-sum-of-array.py) |
| [`3:30:15`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=12615s) | Check if an array is sorted | [💻 `02-check-if-array-is-sorted.py`](code/02-check-if-array-is-sorted.py) |
| [`3:54:50`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=14090s) | First and last index of an element | [💻 `03-first-and-last-index.py`](code/03-first-and-last-index.py) |
| [`4:20:06`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=15606s) | All indices of a number | [💻 `04-all-indices-of-a-number.py`](code/04-all-indices-of-a-number.py) |
| [`4:32:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=16320s) | Optimisation: pass an index instead of slicing | [💻 `04-all-indices-of-a-number.py`](code/04-all-indices-of-a-number.py) |
| [`4:43:30`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=17010s) | Collecting answers in a list passed down | [💻 `05-collect-indices-in-a-passed-list.py`](code/05-collect-indices-in-a-passed-list.py) |
| [`4:58:30`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=17910s) | Collecting answers in a global list | [💻 `06-collect-indices-in-a-global-list.py`](code/06-collect-indices-in-a-global-list.py) |
| [`5:04:55`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=18295s) | Returning a new list | [💻 `07-return-indices-as-a-new-list.py`](code/07-return-indices-as-a-new-list.py) |

## Files

### Code

| File | What it shows |
|---|---|
| [💻 `01-sum-of-array.py`](code/01-sum-of-array.py) | Sum of a list: two head-style versions and a tail version with an accumulator. |
| [💻 `02-check-if-array-is-sorted.py`](code/02-check-if-array-is-sorted.py) | Two recursive ways to check that a list is in increasing order, tried on a 10,000-element list. |
| [💻 `03-first-and-last-index.py`](code/03-first-and-last-index.py) | First and last index of an element; -1 when it is absent. |
| [💻 `04-all-indices-of-a-number.py`](code/04-all-indices-of-a-number.py) | Print every index of a value, including the better version that passes an index instead of slicing. |
| [💻 `05-collect-indices-in-a-passed-list.py`](code/05-collect-indices-in-a-passed-list.py) | Collect the indices in a list that is passed down the calls. |
| [💻 `06-collect-indices-in-a-global-list.py`](code/06-collect-indices-in-a-global-list.py) | Collect the indices in a global list. |
| [💻 `07-return-indices-as-a-new-list.py`](code/07-return-indices-as-a-new-list.py) | Return the indices as a new list built on the way back. |

### Notes (PDF)

| File | Pages | Size | What it is |
|---|---|---|---|
| [📄 `recursion-and-arrays.pdf`](notes/recursion-and-arrays.pdf) | 16 | 7.7 MB | Whiteboard notes for the arrays topic. |

### Notebooks

| File | What it is |
|---|---|
| [📓 `recursion-with-arrays-class-notebook.ipynb`](notebooks/recursion-with-arrays-class-notebook.ipynb) | Class notebook with run outputs for recursion with arrays. |

## Try it yourself

1. Write `max_of_list(nums)` recursively, first by slicing and then with an index.
2. Change `01-sum-of-array.py` to sum only the even numbers.
3. Return the indices of a value in reverse order.
4. Explain in one sentence why the global-list version is risky if you call it twice.
5. Take the checkpoint: `assignments/A2-recursion-and-arrays.ipynb`.

🎯 **Checkpoint:** [Checkpoint 2: Recursion and Arrays](../../assignments/A2-recursion-and-arrays.ipynb) (solutions: [here](../../assignments/solutions/A2-recursion-and-arrays.ipynb)).

---
[← Introduction to Recursion](../01-introduction-to-recursion/) · [Recursion home](../README.md) · [Searching and Sorting with Recursion →](../03-searching-and-sorting/)
