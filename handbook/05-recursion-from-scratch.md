# 5. Recursion From Scratch

**Part 2: Recursion** · Beginner · about 9 minutes to read

> A function calling itself: the mirror story, the call stack frame by frame, the base case, stack overflow and Python's recursion limit.
**In the video:** [`41:40`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=2500s) A function calling itself · [`46:15`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=2775s) Adding a stop · [`48:55`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=2935s) What is recursion? · [`53:05`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=3185s) Factorial · [`1:04:00`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=3840s) Stack overflow  
**In this repo:** [Introduction to recursion: code, notes, notebooks](../recursion/01-introduction-to-recursion/)  
**Run the code from this chapter:** [`code/05-recursion-from-scratch.py`](code/05-recursion-from-scratch.py)  

---

## The most important topic in DSA

Recursion is where most people quietly give up on DSA. It is also the topic that unlocks **linked lists, trees, graphs, backtracking and dynamic programming**: all of them are recursion wearing different clothes. If you truly understand this chapter, half the handbook becomes easy.

So we go slowly, and we start with something you already know.

> **Before you continue:** you should be comfortable with what a function call does in memory. If not, read [Chapter 2](02-python-for-dsa.md) first. It takes ten minutes and it is the prerequisite for everything below.

---

## Story 1: the hall of mirrors

Stand between two mirrors facing each other. You see yourself, and behind that image another image of you, and behind that another, getting smaller, again and again.

How does that work? The first mirror shows you. The second mirror shows *the first mirror showing you*. The third shows *the second mirror showing the first mirror showing you*. Each mirror's picture **depends on the previous mirror's picture, which is the same kind of picture, just one step further**.

In the real world this goes on for ages and fades out. In a program it would go on **forever**, unless we add a rule: *"stop after the fifth mirror."* Keep that picture in your head. It contains the two ingredients of recursion:

1. **A repeated step** that refers to *itself* ("show what the previous mirror shows").
2. **A stopping rule** ("after this one, no more").

---

## Step 1: functions that call other functions

Before we meet recursion, look at something familiar: a function that calls *another* function. Imagine five functions that each print a number and hand over to the next.

```python
def print_one(num):
    print(num)

def print_two(num):
    print(num)
    print_one(num - 1)

def print_three(num):
    print(num)
    print_two(num - 1)

def print_four(num):
    print(num)
    print_three(num - 1)

def print_five(num):
    print(num)
    print_four(num - 1)

print_five(5)
print("hello world")
```

**Output**

```text
5
4
3
2
1
hello world
```

Notice three things:

1. `print_five` does not finish when it prints. It is **waiting** for `print_four` to complete. `print_four` is waiting for `print_three`. All five are alive in memory at the same moment, stacked up (chapter 2: the call stack).
2. Only `print_one` stops the chain, because it does **not** call anything further.
3. After the chain finishes, the waiting functions **return one by one in reverse order** and execution continues after the original call. That is why "hello world" prints last.

Now look at the five functions. They are almost identical. Each one is just "print the number, then do the same job for `num - 1`". Writing five functions is silly. We can ask **one function to call itself**.

---

## Step 2: a function that calls itself

```python
def print_num(num):
    print(num)
    print_num(num - 1)        # the same function, with a smaller number
```

Look at what we have built: `print_num(5)` prints 5 and then calls `print_num(4)`, which prints 4 and calls `print_num(3)`, and so on. Is there a stopping rule? No. Run it and see.

```python
def print_num(num):
    print(num)
    print_num(num - 1)

print_num(3)
```

**Output**

```text
3
2
1
0
-1
-2
-3
-4
-5
-6
-7
-8
-9
-10
-11
-12
-13
-14
-15
-16
-17
-18
-19
-20
-21
-22
-23
-24
-25
-26
-27
-28
-29
-30
-31
-32
-33
-34
-35
... (952 more lines)
-988
-989
RecursionError: maximum recursion depth exceeded
```

(Python prints 3, 2, 1, 0, -1, -2 and so on, until it stops us at a depth of about 1000. The output below is shortened.)

Think about what happened. Every call is waiting for the next one, so frames keep piling on the stack, until Python's safety net trips and raises a **`RecursionError`**. This is precisely the "mirrors with no stopping rule" situation.

> This is the single most common recursion bug in the world: **no base case, or a base case that is never reached.**

---

## Step 3: add the stopping rule (the base case)

Where should the countdown stop? Let us say we want to print from 5 down to 1, so when `num` becomes 0 we have nothing left to do.

```python
def print_num(num):
    if num == 0:               # the BASE CASE: the smallest problem, answered directly
        return
    print(num)
    print_num(num - 1)         # the RECURSIVE CASE: the same problem, one step smaller

print_num(5)
```

**Output**

```text
5
4
3
2
1
```

Two things in this tiny function are the heart of every recursion you will ever write:

| Part | Role | In the code |
|---|---|---|
| **Base case** | The problem is so small that we answer it directly, no more calls | `if num == 0: return` |
| **Recursive case** | The problem is bigger: do a little work and **call yourself on a smaller version** | `print(num)` then `print_num(num - 1)` |

If the base case is the brakes, the recursive case is the engine. You need both.

---

## Watching the stack grow and shrink

Reading about the stack is one thing. Let us *see* it. This tracer prints a line when a call starts and when it ends, with indentation showing the depth.

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

@trace
def countdown(num):
    if num == 0:
        return "done"
    return countdown(num - 1)

countdown(3)
```

**Output**

```text
call   countdown(3,)
    call   countdown(2,)
        call   countdown(1,)
            call   countdown(0,)
            return countdown(0,) -> done
        return countdown(1,) -> done
    return countdown(2,) -> done
return countdown(3,) -> done
```

Read the indentation. It goes **down** (each call is one step deeper), reaches the base case `countdown(0)` at the bottom, and then **comes back up** (each call returns to the one that was waiting). Every recursion has this "go down, come back up" shape. When you debug recursion, you are always asking: *what happens on the way down, and what happens on the way up?*

---

## Story 2: the factorial and the lazy manager

The factorial of a number is the product of all numbers from 1 to it. `5! = 5 × 4 × 3 × 2 × 1 = 120`.

Now notice something: `5! = 5 × (4!)`. The factorial of 5 is just 5 times the factorial of 4. **The big problem contains a smaller copy of itself.** That is the signal that recursion fits.

Think of a company with a chain of managers. You are asked, *"What is 5 factorial?"* You are lazy and clever. You say:

> "I know my part: multiply by 5. But I do not want to compute `4!`. **Hey, junior, bring me the answer for 4.** I will wait."

The junior says the same to *their* junior, and so on, until someone is asked for `1!`. That person says *"That is just 1. Here."* Now the answers come back up the chain, each person doing their one multiplication.

```python
@trace
def factorial(n):
    if n == 1:                       # base case: 1! is 1
        return 1
    small_answer = factorial(n - 1)  # "junior, bring me the answer for n - 1"
    return n * small_answer          # my own tiny job: multiply by n

factorial(4)
```

**Output**

```text
call   factorial(4,)
    call   factorial(3,)
        call   factorial(2,)
            call   factorial(1,)
            return factorial(1,) -> 1
        return factorial(2,) -> 2
    return factorial(3,) -> 6
return factorial(4,) -> 24
```

Read the trace again, top to bottom:

- `factorial(4)` calls `factorial(3)` and **waits**.
- `factorial(3)` calls `factorial(2)` and **waits**.
- `factorial(2)` calls `factorial(1)` and **waits**.
- `factorial(1)` answers `1` at once. The chain unwinds: `2 × 1 = 2`, then `3 × 2 = 6`, then `4 × 6 = 24`.

The variable name `small_answer` matters. We call it that on purpose. **Do not think about *how* `factorial(n - 1)` finds its answer.** In your mind, it just hands you the correct small answer. We will turn that habit into a rule in the next chapter.


---

## The memory picture: why waiting costs memory

Each waiting call is a **stack frame**: a little box in memory with its own `n` and its own `small_answer` (not yet filled in). Let us draw `factorial(4)` at the moment the deepest call starts:

```text
              +--------------------+
   top   ->   | factorial(1)  n=1  |   about to return 1
              +--------------------+
              | factorial(2)  n=2  |   waiting for small_answer
              +--------------------+
              | factorial(3)  n=3  |   waiting for small_answer
              +--------------------+
              | factorial(4)  n=4  |   waiting for small_answer
              +--------------------+
   bottom ->  | the program that called factorial(4) |
              +--------------------+
```

Only the **top** frame is running. The ones below wait. When the top finishes, its frame is *popped* and the one under it resumes **at the exact line where it was waiting**.

That is also why very deep recursion is dangerous. Ask for `factorial(100000)` and you ask for 100,000 stacked frames.

```python
def factorial_plain(n):
    if n == 1:
        return 1
    return n * factorial_plain(n - 1)

factorial_plain(5000)
```

**Output**

```text
RecursionError: maximum recursion depth exceeded
```

Python refuses at roughly depth 1000. The name of the popular website **Stack Overflow** comes from exactly this: a stack that has overflowed.

> You can raise the limit with `sys.setrecursionlimit`, but that only postpones the problem. If you need a depth of a million, use a loop or a smarter algorithm.

---

## Recursion vs a loop: same job, different mindset

Everything we did can be written with a loop. Why bother with recursion?

```python
def factorial_loop(n):
    answer = 1
    for number in range(2, n + 1):
        answer *= number
    return answer

print(factorial_loop(5))
```

**Output**

```text
120
```

For factorial, the loop is perfectly fine (and uses O(1) space). Recursion wins when the problem **naturally contains smaller copies of itself in more than one place**:

- A folder contains folders that contain folders.
- A tree has subtrees that have subtrees.
- "All arrangements of a word" is a letter followed by all arrangements of the rest.
- A game position is a move followed by a smaller game.

For those, a recursive solution is often five lines where a loop-based one is fifty. Recursion is a **way of thinking**: *"assume I can already solve the smaller version; how do I finish?"*

---

## The recursion checklist

When you write (or read) a recursive function, tick these boxes:

1. **Base case.** What is the smallest input I can answer directly? Does the function stop there?
2. **Smaller problem.** Does every recursive call move *closer* to the base case (smaller `n`, shorter list, fewer characters)?
3. **Trust.** Do I assume the recursive call returns the correct answer for the smaller input, without peeking inside?
4. **My part.** What small job does *this* call do with that answer?
5. **Return.** Does every path return a value (if the function should return one)?

```python
# Tick the boxes for this function. Where is each one?
def sum_to(n):
    if n == 0:                    # 1. base case
        return 0
    small_answer = sum_to(n - 1)  # 2. smaller problem, 3. trust
    return n + small_answer       # 4. my part, 5. return

print(sum_to(10))
```

**Output**

```text
55
```


---

## Common mistakes

- **No base case**, or one that the inputs can never reach (`if n == 0` but you call it with `-1`). Always ask: *can `n` skip over my base case?*
- **Not moving toward the base case.** `f(n)` calling `f(n)` is an infinite loop in disguise.
- **Forgetting `return`.** Writing `factorial(n - 1) * n` without `return` gives `None`.
- **Peeking inside the recursive call** and trying to simulate it all in your head. Trust it. Verify with a trace on a *tiny* input.
- **Printing when you should return**, or the other way round (see chapter 9).
- **Two base cases needed, only one written.** Fibonacci needs both `0` and `1` (chapter 7).

---

## Practice

1. 🟢 Write `print_1_to_n(n)` with recursion that prints the numbers in **increasing** order. *(Hint: you may need to move one line. We study why in chapter 8.)*
2. 🟢 Write `count_down(n)` that prints `n, n-1, ..., 1` and then `"liftoff"`.
3. 🟢 Write `power_of_two(n)` that returns 2ⁿ using the recursion `2ⁿ = 2 × 2ⁿ⁻¹`. What is the base case?
4. 🟡 Trace `factorial(5)` on paper: draw the stack of frames at the deepest point.
5. 🟡 What happens if you call the *correct* `factorial` with `n = 0`? With `n = -3`? Fix both.
6. 🔴 Write a recursive function `digits_in(n)` that returns how many digits a positive integer has, using `n // 10`.

<details>
<summary>Hints and answers</summary>

1. Call yourself first with `n - 1`, then print `n`. Whatever comes *after* the recursive call happens on the way back up.
3. Base case: `n == 0` returns 1 (because 2⁰ = 1).
5. The version above starts at `1`, so `0` and negative numbers never reach the base case: infinite recursion. Fix: `if n <= 1: return 1` (and decide what a negative factorial should do).
6. `if n < 10: return 1`, otherwise `1 + digits_in(n // 10)`.
</details>

---

[← 4. Space Complexity: Counting the Memory](04-space-complexity.md) · [Handbook contents](README.md) · [6. PMI and the Recursion Recipe →](06-pmi-and-the-recursion-recipe.md)
