# 6. PMI and the Recursion Recipe

**Part 2: Recursion** · Beginner · about 10 minutes to read

> Why recursion works (mathematical induction) and the three-part recipe: base case, assume, do your part. Applied to sum, power, digits and GCD.
**In the video:** [`1:16:51`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=4611s) PMI · [`1:32:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=5520s) From PMI to a recursion recipe · [`1:37:01`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=5821s) Sum of N numbers · [`1:46:56`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=6416s) Number of digits  
**In this repo:** [Introduction to recursion](../recursion/01-introduction-to-recursion/)  
**Run the code from this chapter:** [`code/06-pmi-and-the-recursion-recipe.py`](code/06-pmi-and-the-recursion-recipe.py)  

---

## The question that bothers everyone

In the last chapter we wrote `small_answer = factorial(n - 1)` and told you: *"trust it, do not look inside."*

A sensible person asks: **"Why should I trust it? The function is not finished yet. It is still being written!"**

That is the right question. The answer comes from an idea you may have met in school mathematics and promptly forgotten: the **Principle of Mathematical Induction (PMI)**. It is the reason recursion is *correct*, not just convenient. And once you see it, you will never fear a recursive question again.

---

## Dominoes: the intuition behind PMI

Line up a million dominoes. You want to prove that **all of them fall**. You do not check them one by one. You prove just two things:

1. **The first domino falls.** (Someone pushes it.)
2. **If any domino falls, the next one falls too.** (They are spaced so that a falling domino always hits its neighbour.)

Those two facts are enough. Domino 1 falls, so domino 2 falls, so domino 3 falls... all the way down the line, no matter how long.

PMI is exactly this, written for statements:

| Step in PMI | In words | The domino picture |
|---|---|---|
| **Base case** | Show the statement is true for the smallest value (say `n = 1`) | The first domino falls |
| **Assumption** (induction hypothesis) | **Assume** it is true for some value `k` | Suppose domino `k` falls |
| **Induction step** | **Prove** it is therefore true for `k + 1`, using that assumption | ...then domino `k + 1` falls too |

Then it is true for **every** `n`.

### A real PMI proof (and why the assumption is fair)

Claim: **1 + 2 + 3 + … + n = n(n + 1) / 2** for every positive integer n.

- **Base case, n = 1.** The left side is `1`. The right side is `1 × 2 / 2 = 1`. ✔
- **Assume** it is true for `n = k`: `1 + 2 + … + k = k(k + 1) / 2`.
- **Prove for `n = k + 1`.** Start with the left side:
  `1 + 2 + … + k + (k + 1)`
  The first part is exactly what we assumed, so replace it:
  `= k(k + 1)/2 + (k + 1)`
  `= (k + 1)(k/2 + 1)`
  `= (k + 1)(k + 2)/2`.
  That is `n(n + 1)/2` with `n = k + 1`. ✔

Notice the key move: **we used the assumption for `k` to prove `k + 1`. We never proved `k` itself in that step.** And that is not cheating, because the base case makes the first one true, which makes the second one true, and so on. The assumption is *fair* because the chain starts from something solid.

```python
# Let the computer double-check the formula for a few thousand values of n.
for n in range(1, 3001):
    assert sum(range(1, n + 1)) == n * (n + 1) // 2
print("formula holds for n = 1 ... 3000")
```

**Output**

```text
formula holds for n = 1 ... 3000
```

---

## From PMI to recursion: it is the same thing

Now put the two side by side.

| PMI proof | Recursive function |
|---|---|
| **Base case:** true for the smallest `n` | **Base case:** answer the smallest input directly |
| **Assume** true for `k` | **Assume** the recursive call `f(n − 1)` returns the **correct answer** for the smaller input |
| **Prove** true for `k + 1` using the assumption | **Use** that answer to build the answer for `n` |

Recursion *is* induction, run as a program. That is why you may **trust** the smaller call: if your base case is right, and your step is right *assuming* the smaller call is right, then by induction **every call is right**.

This turns writing a recursive function into a **three-step recipe**. This is the recipe of the whole course:

> ### The Recursion Recipe
> 1. **Base case.** What is the smallest input, and what is its answer?
> 2. **Assume.** Pretend `f(smaller input)` already gives the correct answer. Do not look inside.
> 3. **Do your part.** Combine that answer with whatever small work *this* call must do, to get the answer for `n`.

Many people try to hold the whole call chain in their heads and drown. **Do not.** Hold three things only: *base case, assume, do your part.* Draw a tiny trace afterwards to check yourself.

Let us use the recipe on real problems. Same template every time: **question, smaller problem, assume, my part, base case, trace, code.**

```python
depth = 0

def trace(fn):
    def wrapper(*args):
        global depth
        print("    " * depth + f"call   {fn.__name__}{args}")
        depth += 1
        result = fn(*args)
        depth -= 1
        print("    " * depth + f"return {fn.__name__}{args} -> {result}")
        return result
    return wrapper
```

---

## Problem 1: the sum of the first N numbers

**Question.** Given `n`, return `1 + 2 + … + n`.

**Smaller problem.** The sum up to `n` is `n` plus the sum up to `n − 1`.

**Assume.** Somebody hands you `sum_to(n − 1)`. Perfect, you do not care how.

**My part.** Add my own `n` to it.

**Base case.** `sum_to(0)` is `0` (nothing to add).

**Story.** You are collecting coins. You hold the coins from your own stall (`n` coins) and ask the stall before you for *its* total, which already includes all the earlier stalls. You just add yours.

```python
@trace
def sum_to(n):
    if n == 0:                         # base case
        return 0
    small_answer = sum_to(n - 1)       # assume: this is 1 + ... + (n - 1)
    return n + small_answer            # my part: add n

sum_to(4)
```

**Output**

```text
call   sum_to(4,)
    call   sum_to(3,)
        call   sum_to(2,)
            call   sum_to(1,)
                call   sum_to(0,)
                return sum_to(0,) -> 0
            return sum_to(1,) -> 1
        return sum_to(2,) -> 3
    return sum_to(3,) -> 6
return sum_to(4,) -> 10
```


The trace shows the shape you now know: four calls go down, then the sums come back up as `0 → 1 → 3 → 6 → 10`.

**Cost.** There are `n + 1` calls and each does constant work: **O(n) time**. The stack is `n + 1` frames deep: **O(n) space**. (The formula `n(n + 1)/2` from the PMI proof does it in O(1). Recursion is not always the best tool, but it teaches the habit.)

---

## Problem 2: x raised to the power n

**Question.** Compute `base ** exponent` for a non-negative integer exponent, *without* using `**`.

**Smaller problem.** `xⁿ = x × xⁿ⁻¹`.

**Assume.** `power(x, n − 1)` is correct.

**My part.** Multiply by `x`.

**Base case.** `x⁰ = 1`, for any `x`.

```python
def power(base, exponent):
    if exponent == 0:                          # base case: anything to the power 0 is 1
        return 1
    small_answer = power(base, exponent - 1)   # assume: base ** (exponent - 1)
    return base * small_answer                 # my part

print(power(2, 10), power(5, 0), power(3, 4))
```

**Output**

```text
1024 1 81
```


This takes `exponent` calls: **O(n)**. Can we do better? Yes, if we choose a **smaller problem that shrinks faster**.

### Faster: halve the exponent instead of subtracting one

`2¹⁰ = 2⁵ × 2⁵`: a half-sized problem, solved **once**, then squared.

**Smaller problem.** When n is even, `x^n = (x^(n/2))²`. When n is odd, `x^n = x × (x^((n−1)/2))²`.

```python
def fast_power(base, exponent):
    if exponent == 0:
        return 1
    half = fast_power(base, exponent // 2)     # assume: base ** (exponent // 2)
    if exponent % 2 == 0:
        return half * half                     # even exponent: just square the half
    return half * half * base                  # odd exponent: one extra base

print(fast_power(2, 10), fast_power(3, 5), fast_power(2, 1000) == 2 ** 1000)
```

**Output**

```text
1024 243 True
```

How many calls does `fast_power(2, 1000)` make? The exponent halves each time: 1000, 500, 250, ... about ten calls instead of a thousand.


**Cost.** **O(log n) time** and **O(log n) stack**, and it never hits Python's recursion limit. (This is the idea behind the harder LeetCode problem *Pow(x, n)* linked in the repo.)

**Careful!** The trap is calling `fast_power` **twice** (`fast_power(b, n//2) * fast_power(b, n//2)`). That brings the cost back to O(n), because you re-solve the same half. Always store the half in a variable.

---

## Problem 3: the number of digits

**Question.** How many digits does the positive integer `n` have? (`12345 → 5`.)

**Smaller problem.** Chop off the last digit: `n // 10`. `12345 // 10 = 1234`: same question, one digit shorter.

**Assume.** `count_digits(1234)` gives `4`.

**My part.** Add 1 for the digit I chopped off.

**Base case.** A single-digit number (`n < 10`) has exactly `1` digit.

**Story.** A train with some coaches. Ask the driver of the *front part* (all coaches except the last) how many coaches it has, then add the last coach.

```python
@trace
def count_digits(n):
    if n < 10:                              # base case: one digit left
        return 1
    small_answer = count_digits(n // 10)    # assume: digits of the number without its last digit
    return 1 + small_answer                 # my part

count_digits(2468)
```

**Output**

```text
call   count_digits(2468,)
    call   count_digits(246,)
        call   count_digits(24,)
            call   count_digits(2,)
            return count_digits(2,) -> 1
        return count_digits(24,) -> 2
    return count_digits(246,) -> 3
return count_digits(2468,) -> 4
```


**Edge cases to test (the video's habit).** `0` has one digit (`0 < 10`, so base case: 1 ✔). A negative number? Decide: use `abs(n)` first.

**Cost.** The number of calls equals the number of digits, which is about `log₁₀ n`. So this is **O(log n)**, a very good one. (Remember from chapter 3: "number of digits" is a logarithm, not `n`.)

---

## Problem 4: the sum of the digits

**Question.** `sum_of_digits(1234) = 1 + 2 + 3 + 4 = 10`.

Same shape as before. You can peel off the **last** digit with `n % 10` and shrink with `n // 10`.

**Smaller problem.** The number without its last digit: `n // 10`.

**Assume.** `sum_of_digits(n // 10)` is correct.

**My part.** Add the digit I peeled off: `n % 10`.

**Base case.** `n < 10` is its own digit sum.

```python
def sum_of_digits(n):
    n = abs(n)                               # ignore a minus sign
    if n < 10:
        return n
    small_answer = sum_of_digits(n // 10)
    return n % 10 + small_answer

print(sum_of_digits(1234), sum_of_digits(0), sum_of_digits(-987), sum_of_digits(1_000_000_000))
```

**Output**

```text
10 0 24 1
```


This is the first assignment from the video. The other one was *power*, which you have just done.

---

## Problem 5: the greatest common divisor (Euclid)

**Question.** The largest number that divides both `a` and `b`. `gcd(48, 18) = 6`.

This is a famous one because the smaller problem is *not* "subtract one". Euclid noticed something beautiful:

> The common divisors of `a` and `b` are exactly the common divisors of `b` and `a % b`.

So `gcd(48, 18) = gcd(18, 12) = gcd(12, 6) = gcd(6, 0) = 6`.

**Assume.** `gcd(b, a % b)` is correct.

**My part.** Nothing to add: the answer is *the same number*. (Sometimes your part is just "pass it up".)

**Base case.** When `b` is `0`, the answer is `a`.

```python
@trace
def gcd(a, b):
    if b == 0:                    # base case
        return a
    return gcd(b, a % b)          # assume: this is the answer; my part: nothing more to do

gcd(48, 18)
```

**Output**

```text
call   gcd(48, 18)
    call   gcd(18, 12)
        call   gcd(12, 6)
            call   gcd(6, 0)
            return gcd(6, 0) -> 6
        return gcd(12, 6) -> 6
    return gcd(18, 12) -> 6
return gcd(48, 18) -> 6
```


**Cost.** The remainder shrinks very fast, at least halving every two steps, so it is **O(log n)**.

---

## A summary of the five

| Problem | Smaller problem | My part | Base case | Time |
|---|---|---|---|---|
| Sum to n | `n − 1` | add `n` | `0 → 0` | O(n) |
| Power (simple) | `exponent − 1` | multiply by `base` | `0 → 1` | O(n) |
| Power (fast) | `exponent // 2` | square it (and one extra `base` if odd) | `0 → 1` | O(log n) |
| Digits count | `n // 10` | add 1 | `n < 10 → 1` | O(log n) |
| Digit sum | `n // 10` | add `n % 10` | `n < 10 → n` | O(log n) |
| GCD | `(b, a % b)` | nothing | `b == 0 → a` | O(log n) |

Look at the pattern: **the smaller problem and your part change from question to question, but the *recipe* never does.**

---

## How to find the smaller problem

This is the real skill. A few reliable tricks:

- **Remove one item.** From a number (`n − 1`), a list (`items[1:]`), a string (`s[1:]`).
- **Chop a digit.** `n // 10` shrinks a number by one digit.
- **Cut in half.** Exponent, list, search range.
- **Fix one choice and recurse on what is left.** (This is the backbone of subsets and permutations.)

Ask yourself: *"If I magically had the answer for the smaller version, what is the least I would still have to do?"* If that "least" is small and obvious, you have found it.

---

## Common mistakes

- **Not trusting the recursive call.** If you catch yourself unrolling the calls in your head, stop. Use the recipe, then verify with a tiny trace.
- **Wrong base case** (answer off by one: `sum_to(1) = 1`, not `0`, if you stop at 1).
- **A step that does not shrink** the problem or shrinks past the base case.
- **Calling the recursive function twice** when once is enough (`fast_power`).
- **Forgetting the zero and negative edge cases.**

---

## Practice

1. 🟢 `product_of_digits(n)` (assume no zeros are a problem). What is the base case?
2. 🟢 `count_digit(n, d)`: how many times does digit `d` appear in `n`?
3. 🟢 `sum_of_squares(n)`: 1² + 2² + … + n².
4. 🟡 `reverse_number(n)`: `1234 → 4321`. *(Hint: carry an accumulator, or compute the length first.)*
5. 🟡 `is_power_of_two(n)` using `n // 2` recursively.
6. 🟡 `to_binary(n)`: the binary string of `n`. *(Hint: last bit is `n % 2`.)*
7. 🔴 Prove with PMI that `2ⁿ ≥ n + 1` for all `n ≥ 0`, then write a recursive function to count how many times you can halve `n` before reaching 1 (and check it against `math.log2`).

<details>
<summary>Hints</summary>

1. Base: a single digit is its own product. Step: `(n % 10) * product_of_digits(n // 10)`.
4. Use `reverse_helper(n, accumulator)`: each step moves the last digit of `n` onto the right end of the accumulator.
5. A power of two greater than 1 is even, and half of it is also a power of two. Base: `1 → True`, odd (≠1) or `0 → False`.
7. PMI: base `2⁰ = 1 ≥ 1`. Assume `2ᵏ ≥ k + 1`; then `2ᵏ⁺¹ = 2·2ᵏ ≥ 2k + 2 ≥ k + 2`.
</details>

You can check your solutions for the first few against the auto-checked notebook [Checkpoint 1](../assignments/A1-introduction-to-recursion.ipynb).

---

[← 5. Recursion From Scratch](05-recursion-from-scratch.md) · [Handbook contents](README.md) · [7. Fibonacci and Recursion Trees →](07-fibonacci-and-recursion-trees.md)
