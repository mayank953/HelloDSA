"""05. Recursion From Scratch

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 05-recursion-from-scratch.py
"""

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

def print_num(num):
    print(num)
    print_num(num - 1)        # the same function, with a smaller number

def print_num(num):
    if num == 0:               # the BASE CASE: the smallest problem, answered directly
        return
    print(num)
    print_num(num - 1)         # the RECURSIVE CASE: the same problem, one step smaller

print_num(5)

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

@trace
def factorial(n):
    if n == 1:                       # base case: 1! is 1
        return 1
    small_answer = factorial(n - 1)  # "junior, bring me the answer for n - 1"
    return n * small_answer          # my own tiny job: multiply by n

factorial(4)

def factorial_loop(n):
    answer = 1
    for number in range(2, n + 1):
        answer *= number
    return answer

print(factorial_loop(5))

# Tick the boxes for this function. Where is each one?
def sum_to(n):
    if n == 0:                    # 1. base case
        return 0
    small_answer = sum_to(n - 1)  # 2. smaller problem, 3. trust
    return n + small_answer       # 4. my part, 5. return

print(sum_to(10))

print('\n[all code in this chapter ran successfully]')
