# 3. Searching and Sorting with Recursion

Linear and binary search written recursively, then merge sort and quick sort: how to divide the problem, what the recursive call returns, and how to merge or partition. Starter scaffolds are included so you can fill in `Merge` and `partitionFunction` yourself.

**Video:** starts at [`5:35:08`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=20108s)

## Chapters

| Time | Chapter | Code and notes |
|------|---------|----------------|
| [`5:35:08`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=20108s) | Linear search with recursion | [💻 `01-linear-search.py`](code/01-linear-search.py) |
| [`5:50:54`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=21054s) | Binary search with recursion | [💻 `02-binary-search.py`](code/02-binary-search.py) |
| [`6:12:30`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=22350s) | Merge sort: the idea | [🧩 `03-merge-sort-starter.py`](code/03-merge-sort-starter.py) |
| [`6:27:56`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=23276s) | Merge sort: the approach step by step | [🧩 `03-merge-sort-starter.py`](code/03-merge-sort-starter.py) |
| [`6:40:05`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=24005s) | Merge sort: code and debugging | [💻 `04-merge-sort.py`](code/04-merge-sort.py) |
| [`7:11:17`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=25877s) | Quick sort: pivot and partition | [🧩 `05-quick-sort-starter.py`](code/05-quick-sort-starter.py) |
| [`7:25:10`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=26710s) | Quick sort: code | [💻 `06-quick-sort.py`](code/06-quick-sort.py) |

## Files

### Code

| File | What it shows |
|---|---|
| [💻 `01-linear-search.py`](code/01-linear-search.py) | Linear search that returns True or False: one version carries an index, the other combines the answer on the way back. |
| [💻 `02-binary-search.py`](code/02-binary-search.py) | Binary search (True or False) with a helper that carries the start and end positions. |
| [🧩 `03-merge-sort-starter.py`](code/03-merge-sort-starter.py) | Starter: `MergeSort` is written, `Merge` is left for you to fill in. |
| [💻 `04-merge-sort.py`](code/04-merge-sort.py) | Complete merge sort (`Merge`, `MergeSortHelper`, `MergeSort`). |
| [🧩 `05-quick-sort-starter.py`](code/05-quick-sort-starter.py) | Starter: `QuickSort` is written, `partitionFunction` is left for you to fill in. |
| [💻 `06-quick-sort.py`](code/06-quick-sort.py) | Complete quick sort with a partition function. |

### Notebooks

| File | What it is |
|---|---|
| [📓 `searching-class-notebook.ipynb`](notebooks/searching-class-notebook.ipynb) | Class notebook: searching with recursion. |
| [📓 `merge-sort-class-notebook.ipynb`](notebooks/merge-sort-class-notebook.ipynb) | Class notebook: merge sort. |
| [📓 `quick-sort-class-notebook.ipynb`](notebooks/quick-sort-class-notebook.ipynb) | Class notebook: quick sort. |

## Try it yourself

1. Count the calls binary search makes on a list of 1,000 sorted numbers.
2. Finish `Merge` in `03-merge-sort-starter.py` without looking at `04-merge-sort.py`.
3. Finish `partitionFunction` in `05-quick-sort-starter.py` and test it on a list with duplicates.
4. Sort the same list with merge sort and quick sort and compare the number of comparisons.
5. Take the checkpoint: `assignments/A3-searching-and-sorting.ipynb`.

🎯 **Checkpoint:** [Checkpoint 3: Searching and Sorting](../../assignments/A3-searching-and-sorting.ipynb) (solutions: [here](../../assignments/solutions/A3-searching-and-sorting.ipynb)).

---
[← Recursion and Arrays](../02-recursion-and-arrays/) · [Recursion home](../README.md) · [Recursion and Strings →](../04-recursion-and-strings/)
