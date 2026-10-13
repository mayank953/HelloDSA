"""16. Stacks

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 16-stack.py
"""

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

print(evaluate_postfix("5 3 -".split()), evaluate_postfix("8 2 /".split()))

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

def next_greater(numbers):
    answers = [-1] * len(numbers)
    waiting = []                              # indices of numbers still waiting for a bigger one
    for i, value in enumerate(numbers):
        while waiting and numbers[waiting[-1]] < value:
            answers[waiting.pop()] = value    # this newcomer is their answer
        waiting.append(i)
    return answers

print(next_greater([4, 5, 2, 25]), next_greater([13, 7, 6, 12]))

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

print('\n[all code in this chapter ran successfully]')
