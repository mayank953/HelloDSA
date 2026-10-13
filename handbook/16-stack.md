# 16. Stacks

**Part 3: Data Structures** · Intermediate · about 8 minutes to read

> Last in, first out: implementation, balanced brackets, the monotonic stack, evaluating expressions, and why recursion is a stack in disguise.
**In this repo:** [Stack notebook and notes](../dsa-topics/stack/)  
**Run the code from this chapter:** [`code/16-stack.py`](code/16-stack.py)  

---

## A pile of plates

In a canteen, clean plates are stacked on a spring. You can only do two things: **put a plate on top**, or **take the top plate**. You never pull one from the middle, and you cannot reach the bottom plate without removing every plate above it.

The **last** plate placed is the **first** one taken. That rule has a name: **LIFO**, *Last In, First Out*. A data structure that follows it is a **stack**.

You use stacks constantly without noticing:

- the **Back** button in your browser (the last page you visited is the first one you return to),
- **Undo** in an editor (the last change is undone first),
- a stack of **open brackets** while a compiler reads code,
- the **call stack**: the pile of waiting function calls from chapters 2 and 5. Recursion *is* a stack, running on its own.

> A stack does only a few things, and each one is **O(1)**:
> **push** (add on top) · **pop** (remove and return the top) · **peek** (look at the top) · **is_empty**.

---

## Building a stack

### On a Python list

A Python list is already a stack if you use only its **end**: `append` pushes and `pop()` removes, both O(1) (chapter 14).

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, value):
        self._items.append(value)

    def pop(self):
        if not self._items:
            raise IndexError("pop from an empty stack")     # underflow
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at an empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

stack = Stack()
for plate in ["red", "green", "blue"]:
    stack.push(plate)

print(stack.peek(), len(stack))
print(stack.pop(), stack.pop(), stack.pop())
print(stack.is_empty())
```

**Output**

```text
blue 3
blue green red
True
```

Popping an empty stack is called **underflow**, and a good stack raises a clear error instead of returning garbage. (A stack with a fixed capacity also has **overflow** when you push onto a full one.)

### On a linked list

The top of the stack is the **head** of a linked list. Push is "insert at head" and pop is "delete at head": both **O(1)** with no resizing and no shifting (chapter 15).

```python
class Node:
    def __init__(self, data, next=None):
        self.data, self.next = data, next

class LinkedStack:
    def __init__(self):
        self._head = None
        self._size = 0

    def push(self, value):
        self._head = Node(value, self._head)     # the new node points at the old top
        self._size += 1

    def pop(self):
        if self._head is None:
            raise IndexError("pop from an empty stack")
        value = self._head.data
        self._head = self._head.next             # the old top is discarded
        self._size -= 1
        return value

    def __len__(self):
        return self._size

linked = LinkedStack()
for plate in [1, 2, 3]:
    linked.push(plate)
print(linked.pop(), linked.pop(), len(linked))
```

**Output**

```text
3 2 1
```


Both versions behave the same from the outside. That is the idea of an **abstract data type**: you care about *what* it does (push, pop, peek), not how it stores things.

---

## Problem 1: balanced brackets

**Question.** Is `"{[()]}"` valid? What about `"([)]"`? A string of brackets is valid if every opener is closed by the **same kind**, in the **right order**.

**Why a stack?** Think about nesting. The bracket you opened **last** must be the one you close **first**. "Last in, first out" is exactly that rule.

**Algorithm.** Read left to right.

- Opener (`(`, `[`, `{`): **push** it.
- Closer: **pop** the top and check that it is the matching opener. If the stack is empty, or the kinds do not match, the string is invalid.
- At the end, the stack must be empty (every opener got closed).

```python
def is_balanced(text, show=False):
    partner = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in partner:
            if not stack or stack.pop() != partner[ch]:
                return False
        if show:
            print(f"  read {ch!r}  stack = {stack}")
    return len(stack) == 0

print("{[()]}", is_balanced("{[()]}", show=True))
print("([)]", is_balanced("([)]", show=True))
```

**Output**

```text
  read '{'  stack = ['{']
  read '['  stack = ['{', '[']
  read '('  stack = ['{', '[', '(']
  read ')'  stack = ['{', '[']
  read ']'  stack = ['{']
  read '}'  stack = []
{[()]} True
  read '('  stack = ['(']
  read '['  stack = ['(', '[']
([)] False
```

Watch the stack grow as openers arrive and shrink as closers match. In `"([)]"` the closer `)` finds `[` on top, a mismatch, so it fails immediately.


**Cost.** One pass: **O(n)** time, **O(n)** space in the worst case (all openers).

---

## Problem 2: evaluate a postfix expression

We write maths as `3 + 4` (**infix**: the operator sits between the numbers). Computers prefer **postfix** (reverse Polish notation): `3 4 +`, where the operator comes **after** its two numbers. Postfix needs **no brackets and no precedence rules**: it is evaluated by a stack.

**Algorithm.** Read tokens left to right.

- A number: **push** it.
- An operator: **pop two numbers**, apply the operator, **push the result**.

The last item left is the answer.

```python
def evaluate_postfix(tokens):
    stack = []
    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            right = stack.pop()                 # the SECOND operand was pushed last, so it pops first
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(left / right)
        else:
            stack.append(float(token))
    return stack.pop()

# 2 * (3 + 4) - 5   is   2 3 4 + * 5 -   in postfix
print(evaluate_postfix("2 3 4 + * 5 -".split()))
```

**Output**

```text
9.0
```

**The trap everyone falls into:** the order of the two operands. The *first* pop gives the **right** operand. For `5 3 -` you want `5 − 3 = 2`, not `3 − 5`.

```python
print(evaluate_postfix("5 3 -".split()), evaluate_postfix("8 2 /".split()))
```

**Output**

```text
2.0 4.0
```

### Converting normal maths to postfix

Humans write infix. A second stack-based algorithm (the **shunting-yard** algorithm) converts it, honouring precedence and brackets:

- Numbers go straight to the output.
- An **operator** waits on a stack. Before it is pushed, pop every operator on the stack that has **higher or equal precedence** into the output.
- `(` is pushed; `)` pops operators to the output until the matching `(`.

```python
def to_postfix(expression):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    output, operators = [], []
    for token in expression.split():
        if token in precedence:
            while operators and operators[-1] != "(" and precedence[operators[-1]] >= precedence[token]:
                output.append(operators.pop())
            operators.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()                    # discard the "("
        else:
            output.append(token)               # a number
    while operators:
        output.append(operators.pop())
    return output

postfix = to_postfix("2 * ( 3 + 4 ) - 5")
print(postfix)
print(evaluate_postfix(postfix))
```

**Output**

```text
['2', '3', '4', '+', '*', '5', '-']
9.0
```


That is how calculators and compilers evaluate expressions.

---

## Problem 3: the next greater element (the monotonic stack)

**Question.** For each number in a list, find the **next number to its right that is bigger** (or `-1` if none). For `[4, 5, 2, 25]` the answer is `[5, 25, 25, -1]`.

**Story.** People stand in a line, all facing right. Each person wants to know **who is the first taller person ahead**. Instead of every person scanning ahead, we walk down the line **once** and keep a *waiting list* of people who have not yet found a taller person.

When a new person arrives who is taller than some people on the waiting list, they have just found their answer: **everyone shorter at the top of the waiting list gets resolved at once.** Then the newcomer joins the waiting list.

The waiting list is a stack, and notice something: **it is always in decreasing order** from bottom to top (a taller person would have resolved the shorter ones). That is why it is called a **monotonic stack**.

```python
def next_greater(numbers):
    answers = [-1] * len(numbers)
    waiting = []                              # indices of numbers still waiting for a bigger one
    for i, value in enumerate(numbers):
        while waiting and numbers[waiting[-1]] < value:
            answers[waiting.pop()] = value    # this newcomer is their answer
        waiting.append(i)
    return answers

print(next_greater([4, 5, 2, 25]), next_greater([13, 7, 6, 12]))
```

**Output**

```text
[5, 25, 25, -1] [-1, 12, 12, -1]
```

### Why is this O(n) when there is a `while` inside a `for`?

Look: every index is **pushed once** and **popped at most once**. The inner `while` loop does not restart from scratch; it pops things that stay popped. Over the whole run there are at most `n` pushes and `n` pops: `2n` operations in total, **amortised O(1)** per item.

Compare with the "scan to the right for every element" approach, counting real steps:

```python
def next_greater_brute(numbers):
    steps = 0
    answers = []
    for i in range(len(numbers)):
        found = -1
        for j in range(i + 1, len(numbers)):
            steps += 1
            if numbers[j] > numbers[i]:
                found = numbers[j]
                break
        answers.append(found)
    return answers, steps

def next_greater_stack_steps(numbers):
    steps = 0
    waiting = []
    for i, value in enumerate(numbers):
        while waiting and numbers[waiting[-1]] < value:
            waiting.pop()
            steps += 1
        waiting.append(i)
        steps += 1
    return steps

data = list(range(2000, 0, -1))              # descending: the worst case for the brute force
brute_answers, brute_steps = next_greater_brute(data)
print(f"brute force: {brute_steps:,} comparisons    stack: {next_greater_stack_steps(data):,} operations   (n = {len(data):,})")
```

**Output**

```text
brute force: 1,999,000 comparisons    stack: 2,000 operations   (n = 2,000)
```


### The same idea, a famous variation

*"Daily temperatures"*: for each day, how many days until a warmer day? Store **indices** and answer with the **distance**.

```python
def days_until_warmer(temperatures):
    answers = [0] * len(temperatures)
    waiting = []
    for i, temp in enumerate(temperatures):
        while waiting and temperatures[waiting[-1]] < temp:
            previous = waiting.pop()
            answers[previous] = i - previous      # the distance, not the value
        waiting.append(i)
    return answers

print(days_until_warmer([73, 74, 75, 71, 69, 72, 76, 73]))
```

**Output**

```text
[1, 1, 4, 2, 1, 1, 0, 0]
```


The monotonic stack solves a whole family: next greater, previous smaller, stock span, largest rectangle in a histogram. Whenever you see *"for each item, find the nearest item to its left/right that is bigger/smaller"*, think of it.

---

## Problem 4: a stack that knows its minimum

**Question.** Design a stack where `push`, `pop`, `peek` **and `get_min`** are all O(1).

**Idea.** Alongside each value, remember **the minimum of everything at or below it**. When an item is popped, the minimum of what remains is already stored one level down.

```python
class MinStack:
    def __init__(self):
        self._items = []                         # each entry is (value, minimum so far)

    def push(self, value):
        current_min = value if not self._items else min(value, self._items[-1][1])
        self._items.append((value, current_min))

    def pop(self):
        return self._items.pop()[0]

    def get_min(self):
        return self._items[-1][1]

ms = MinStack()
for v in [5, 3, 7, 3, 8]:
    ms.push(v)
print(ms.get_min())
ms.pop(); ms.pop()
print(ms.get_min())
ms.pop()
print(ms.get_min())
```

**Output**

```text
3
3
3
```


The pattern is "store extra information along with each element so a question about the *whole* stack is answered in O(1)". It costs O(n) extra space.

---

## Recursion *is* a stack

The call stack from chapter 2 is nothing mystical: it is a stack of frames. We can prove it by **removing recursion and managing the stack ourselves**.

`factorial(5)` has two phases: on the way **down** each call leaves a *pending multiplication*; on the way **up** they are performed in reverse. A stack holds exactly that:

```python
def factorial_with_stack(n):
    pending = []
    while n > 1:                        # "going down": remember the multiplication we still owe
        pending.append(n)
        n -= 1
    result = 1                          # the base case: 1! = 1
    while pending:                      # "coming back up": pay the debts in reverse order
        result *= pending.pop()
    return result

print(factorial_with_stack(5))
```

**Output**

```text
120
```

A more useful example: **flattening a nested list** like `[1, [2, [3, 4]], 5]`. The recursive solution is short. Here is the same thing with an explicit stack, which can handle nesting depths that would overflow Python's call stack:

```python
def flatten_recursive(items):
    flat = []
    for item in items:
        if isinstance(item, list):
            flat.extend(flatten_recursive(item))
        else:
            flat.append(item)
    return flat

def flatten_with_stack(items):
    flat = []
    stack = list(reversed(items))           # the top of the stack is the next item to handle
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(reversed(item))    # open the sub-list: its items go on top, in order
        else:
            flat.append(item)
    return flat

nested = [1, [2, [3, 4]], 5]
print(flatten_recursive(nested), flatten_with_stack(nested))
```

**Output**

```text
[1, 2, 3, 4, 5] [1, 2, 3, 4, 5]
```


The last hidden check flattens a list nested 5,000 levels deep with the explicit stack. The recursive version would have crashed with a `RecursionError`. This is the standard way to **convert a recursion into a loop**: replace the call stack with a stack of your own.

---

## Common mistakes

- **Popping or peeking an empty stack.** Always check `is_empty()` (or handle the exception).
- **Wrong operand order** in postfix evaluation (`right = pop()` first).
- **Forgetting the final emptiness check** in bracket matching: `"((("` never fails inside the loop.
- **Pushing values when you needed indices** (monotonic stack), then being unable to compute distances.
- **Using `list.pop(0)`** for a stack. That is a *queue* operation and costs O(n); a stack uses the **end**.
- **Treating "O(n) with a nested loop" as O(n²)** without checking whether each item is processed once (the monotonic stack).

---

## Practice

1. 🟢 Reverse a string using a stack. Reverse each word of a sentence in place.
2. 🟢 Check whether a string like `"a(b)c)"` has balanced round brackets and count how many brackets you must remove to fix it.
3. 🟡 Remove adjacent duplicates: `"abbaca" → "ca"`, using a stack.
4. 🟡 Decode a string like `"3[a2[c]]"` into `"accaccacc"`.
5. 🟡 Compute the **stock span**: for each day, how many consecutive earlier days had a price at most today's.
6. 🔴 **Largest rectangle in a histogram** with a monotonic stack in O(n).
7. 🔴 Implement a **queue using two stacks** (you will do it in chapter 17), and a **stack using two queues**.
8. 🔴 Simulate **recursion depth**: write the explicit-stack version of the recursive Fibonacci.

<details>
<summary>Hints</summary>

3. Push each character; if it equals the top, pop instead.
4. Keep a stack of `(text_so_far, repeat_count)`: on `[` push the current state, on `]` pop and multiply.
5. It is "previous greater element" in disguise: pop all days with price ≤ today; the span is `today - index of the new top`.
6. Keep indices of increasing bar heights; when a smaller bar arrives, pop and compute the rectangle that the popped bar spans.
</details>

---

[← 15. Linked Lists](15-linked-list.md) · [Handbook contents](README.md) · [17. Queues and Deques →](17-queue-and-deque.md)
