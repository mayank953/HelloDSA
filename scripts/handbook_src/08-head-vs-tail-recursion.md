## One line that flips the whole output

Look at these two functions. They contain *exactly the same two lines*. Only the order differs.

```python
def print_down(n):
    if n == 0:
        return
    print(n)               # my work FIRST
    print_down(n - 1)      # then the recursive call

def print_up(n):
    if n == 0:
        return
    print_up(n - 1)        # the recursive call FIRST
    print(n)               # then my work

print("print_down(4):")
print_down(4)
print("print_up(4):")
print_up(4)
```

One counts down, the other counts up. Neither has a loop, neither builds a list, neither is "tricky". Why does swapping two lines reverse the output? This chapter answers that question, and the answer is one of the most useful mental models in recursion.

---

## The two halves of every recursive call

Think of each call as having **two moments**:

1. **On the way down.** The call has just started. It runs the lines *before* the recursive call.
2. **On the way up.** The recursive call has just returned. The call runs the lines *after* it.

The calls are stacked like plates, so the **first call starts first but finishes last**. That reverses the order of everything done on the way up.

Watch it with the tracer:

```python
depth = 0

def show(message):
    print("    " * depth + message)

def demo(n):
    global depth
    if n == 0:
        show("base case reached: time to climb back up")
        return
    show(f"going DOWN into n={n}")      # before the call
    depth += 1
    demo(n - 1)
    depth -= 1
    show(f"coming back UP out of n={n}")   # after the call

demo(3)
```

Read it as a story: *down* into 3, 2, 1, hit the bottom, then *up* out of 1, 2, 3. Lines before the call run in the order 3, 2, 1. Lines after the call run in the order 1, 2, 3, the **exact reverse**.

That is the whole secret:

| Where is your work? | When does it run? | Order |
|---|---|---|
| **Before** the recursive call | On the way **down** | Same order as the calls (`n, n−1, ..., 1`) |
| **After** the recursive call | On the way **up** | Reverse order (`1, ..., n−1, n`) |

```python hide
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print_down(3); print_up(3)
assert buf.getvalue().split() == ["3", "2", "1", "1", "2", "3"]
```

---

## Head and tail: the names

You will hear two names for these styles:

- **Head recursion** (the recursive call comes *first*, work comes after). The call is at the "head" of the function. `print_up` is head recursion. Everything meaningful happens while *returning*.
- **Tail recursion** (the work comes first, and the recursive call is the **very last thing**). `print_down` is tail recursion. Once it makes the call, it has nothing left to do.

The precise test for a **tail call** is: *after the recursive call returns, does the function do anything else with the result?* If it simply returns that result as it is, it is a tail call.

Take the factorial:

```python
def factorial_head(n):
    if n <= 1:
        return 1
    return n * factorial_head(n - 1)       # after the call returns, we still have to multiply by n
```

That `n *` waiting after the call means this is **not** a tail call. Every waiting frame remembers its `n`, and the answer is built **on the way up**: `1, then 2×1, then 3×2, then 4×6`.

Can we do the multiplication on the way **down** instead? Yes: carry the running product along as an extra argument, called an **accumulator**. Each call multiplies *before* it calls, and passes the product down:

```python
def factorial_tail(n, accumulator=1):
    if n <= 1:
        return accumulator                      # the answer is already complete when we hit the bottom
    return factorial_tail(n - 1, accumulator * n)   # nothing left to do after this call returns

print(factorial_head(6), factorial_tail(6))
```

Trace both for `n = 4` to *see* where the multiplications happen:

```python
depth = 0

def traced(fn):
    def wrapper(*args):
        global depth
        print("    " * depth + f"call   {fn.__name__}{args}")
        depth += 1
        result = fn(*args)
        depth -= 1
        print("    " * depth + f"return {fn.__name__}{args} -> {result}")
        return result
    wrapper.__name__ = fn.__name__
    return wrapper

@traced
def fact_head(n):
    if n <= 1:
        return 1
    return n * fact_head(n - 1)

@traced
def fact_tail(n, acc=1):
    if n <= 1:
        return acc
    return fact_tail(n - 1, acc * n)

print("--- head: the answer is built while returning ---")
fact_head(4)
print()
print("--- tail: the answer is built while going down ---")
fact_tail(4)
```

Look at the returns of the head version: `1, 2, 6, 24`, the product grows as the stack unwinds. Look at the tail version: the calls carry `acc = 1, 4, 12, 24` downward, and on the way back **every frame just passes the same final answer up unchanged**. There is no unfinished business left in any frame.

```python hide
depth = 0
assert factorial_head(10) == factorial_tail(10) == 3628800
```

### The video's "wrong tail" trap

Beginners often try to do the work first but forget to **carry** the result. For example:

```python
def fact_tail_wrong(n):
    if n <= 1:
        return 1
    product = n * 1              # "my work first"... but nothing carries `product` down the chain
    return fact_tail_wrong(n - 1)

print(fact_tail_wrong(5))        # always 1
```

The work must be **passed down** as an argument (the accumulator). If your "work first" result is stored in a local variable and the call does not receive it, the work is simply lost.

```python hide
assert fact_tail_wrong(5) == 1
```

---

## Why would anyone care about tail recursion?

A tail call has a lovely property: the waiting frame has **nothing left to do**, so in principle it could be *thrown away* before the recursive call begins, since nobody will ever come back to it. A compiler can then reuse the same frame for the next call, turning the recursion into a plain loop with **O(1) stack space**. This is called **tail call optimisation (TCO)**.

Languages built around recursion do this (Scheme, Erlang, and others; Kotlin and Scala for self-calls with `tailrec`/annotations).

**Python does not.** This is a deliberate decision by the language designers (it keeps tracebacks readable). So a tail-recursive function in Python still uses one frame per call:

```python expect-error
def count_tail(n, accumulator=0):
    if n == 0:
        return accumulator
    return count_tail(n - 1, accumulator + 1)      # a perfect tail call

count_tail(5000)
```

Even though it is a textbook tail call, Python raises `RecursionError`. So in Python:

- Tail recursion is a **useful way to think** and a skill interviewers like to see.
- It is **not** a way to save stack space. If you need that, write the loop.

Converting a tail-recursive function to a loop is mechanical: *the arguments become variables, and the recursive call becomes "update the variables and go back to the top".*

```python
def count_loop(n, accumulator=0):
    while n != 0:                       # the base case becomes the loop condition
        n, accumulator = n - 1, accumulator + 1    # the "call" becomes an update
    return accumulator

print(count_loop(5000), count_loop(10 ** 6))
```

```python hide
assert count_loop(10 ** 6) == 10 ** 6
```

---

## The order matters in more than printing

The up-versus-down idea shows up in many places:

**Building a list in a chosen order**

```python
def count_up(n):
    if n == 0:
        return []
    return count_up(n - 1) + [n]       # smaller list first, then append mine -> increasing

def count_down(n):
    if n == 0:
        return []
    return [n] + count_down(n - 1)     # mine first, then the smaller list -> decreasing

print(count_up(5))
print(count_down(5))
```

**Reversing a string with recursion**

```python
def reverse(text):
    if len(text) <= 1:
        return text
    return reverse(text[1:]) + text[0]      # reverse the rest, then put my first character at the END

print(reverse("recursion"))
```

**Visiting a tree** (chapter 19). *Preorder* does its work **before** recursing into the children; *postorder* does it **after**; *inorder* does it **between** the left and right child. Same three positions, same idea. If you understand this chapter, tree traversals are free.

```python hide
assert count_up(5) == [1, 2, 3, 4, 5] and count_down(5) == [5, 4, 3, 2, 1]
assert reverse("recursion") == "noisrucer"
```

---

## A classroom picture: kids and notebooks

Picture a line of kids standing one behind the other, each holding a notebook of homework. The teacher stands in front and wants *all* the notebooks collected in a neat pile.

**Head style (work after the call).** The teacher asks the first kid for *everything*. That kid says *"I will hand over mine, but first let me get the ones behind me"*, and asks the next kid, who asks the next, and so on. Only when the **last kid** hands a notebook forward do the others add theirs, one by one, *on the way back*. The pile is built while the notebooks travel forward.

**Tail style (work before the call).** Each kid puts their own notebook on top of the pile **first**, and then hands the **whole pile** to the kid behind them. When the last kid receives the pile, it is already complete, and he walks it straight to the teacher. The pile is built while it travels backward; nobody has to remember anything.

The pile that gets passed along is the **accumulator**. That one picture explains tail recursion. If an interviewer asks you to explain it, tell this story: it works because everyone understands it.

---

## Common mistakes

- **Putting the line on the wrong side of the call**, then being surprised the order is reversed. Whenever output order is wrong, check which side of the recursive call it sits on.
- **Calling something "tail recursive" when work remains** after the call (`n * f(n-1)` is not a tail call; the `n *` happens after).
- **Expecting Python to optimise tail calls.** It will not. Use a loop for very deep tail recursions.
- **Forgetting to pass the accumulator** (the "wrong tail" trap above), or forgetting its initial value.
- **Doing the work in the base case only** and wondering why the rest is lost.

---

## Practice

1. 🟢 Write `print_digits_left_to_right(n)` and `print_digits_right_to_left(n)` using only `n // 10` and `n % 10`. Which one needs the work *after* the call?
2. 🟢 Write a recursive function that prints a string's characters in **reverse**, without building a new string.
3. 🟡 Write the tail-recursive sum of a list, `sum_tail(items, accumulator=0)`. Convert it to a loop.
4. 🟡 Predict the output, then check: a function that prints `n`, calls itself with `n − 1`, and then prints `n` again, called with `n = 3`.
5. 🟡 Write `print_binary(n)` that prints the binary digits of `n` from most significant to least using recursion. *(Hint: it is the same as `print_digits_left_to_right`, but base 2.)*
6. 🔴 Is `return fib_tail(n - 1, b, a + b)` a tail call? Write Fibonacci with two accumulators, and confirm it runs in O(n) time without a memo.

<details>
<summary>Hints and answers</summary>

1. Left to right needs the call first (`print_digits_left_to_right(n // 10)`, then print `n % 10`). Right to left prints `n % 10` first.
4. It prints `3 2 1 1 2 3`: the first print of each call happens going down, the second going up.
6. Yes: the call is the last thing and nothing is done with the result. `fib_tail(n, a=0, b=1)`: base case `n == 0` returns `a`; otherwise `fib_tail(n - 1, b, a + b)`.
</details>
