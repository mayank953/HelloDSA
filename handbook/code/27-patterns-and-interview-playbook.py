"""27. Patterns and the Interview Playbook

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 27-patterns-and-interview-playbook.py
"""

def target_complexity(n):
    """A rule of thumb: the slowest running time that is still comfortable for input size n."""
    if n <= 10:
        return "O(n!)"
    if n <= 25:
        return "O(2^n)"
    if n <= 500:
        return "O(n^3)"
    if n <= 10_000:
        return "O(n^2)"
    if n <= 1_000_000:
        return "O(n log n)"
    return "O(n) or O(log n)"

for n in [8, 20, 300, 5_000, 200_000, 10_000_000]:
    print(f"n up to {n:>10,}: aim for {target_complexity(n)}")

def max_subarray_cubic(items):
    steps, best = 0, items[0]
    for start in range(len(items)):
        for end in range(start, len(items)):
            total = 0
            for k in range(start, end + 1):          # re-add the whole stretch each time
                total += items[k]
                steps += 1
            best = max(best, total)
    return best, steps

def max_subarray_quadratic(items):
    steps, best = 0, items[0]
    for start in range(len(items)):
        total = 0
        for end in range(start, len(items)):         # extend the previous total by one item
            total += items[end]
            steps += 1
            best = max(best, total)
    return best, steps

def max_subarray_linear(items):
    steps, best, current = 0, items[0], items[0]
    for value in items[1:]:
        current = max(value, current + value)        # Kadane: drop a stretch that hurts
        best = max(best, current)
        steps += 1
    return best, steps

data = [(i * 37) % 19 - 9 for i in range(120)]       # a reproducible mix of negatives and positives
for solve in (max_subarray_cubic, max_subarray_quadratic, max_subarray_linear):
    answer, steps = solve(data)
    print(f"{solve.__name__:<24} answer {answer:>3}   steps {steps:>9,}")

import random
rng = random.Random(27)
for _ in range(500):
    small = [rng.randint(-9, 9) for _ in range(rng.randint(1, 12))]
    assert max_subarray_linear(small)[0] == max_subarray_cubic(small)[0]
print("the fast solution agrees with the brute force on 500 random inputs")

print('\n[all code in this chapter ran successfully]')
