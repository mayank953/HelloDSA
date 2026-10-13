"""08. Head vs Tail Recursion and the Order of Work

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 08-head-vs-tail-recursion.py
"""

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

def factorial_head(n):
    if n <= 1:
        return 1
    return n * factorial_head(n - 1)       # after the call returns, we still have to multiply by n

def factorial_tail(n, accumulator=1):
    if n <= 1:
        return accumulator                      # the answer is already complete when we hit the bottom
    return factorial_tail(n - 1, accumulator * n)   # nothing left to do after this call returns

print(factorial_head(6), factorial_tail(6))

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

def fact_tail_wrong(n):
    if n <= 1:
        return 1
    product = n * 1              # "my work first"... but nothing carries `product` down the chain
    return fact_tail_wrong(n - 1)

print(fact_tail_wrong(5))        # always 1

def count_loop(n, accumulator=0):
    while n != 0:                       # the base case becomes the loop condition
        n, accumulator = n - 1, accumulator + 1    # the "call" becomes an update
    return accumulator

print(count_loop(5000), count_loop(10 ** 6))

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

def reverse(text):
    if len(text) <= 1:
        return text
    return reverse(text[1:]) + text[0]      # reverse the rest, then put my first character at the END

print(reverse("recursion"))

print('\n[all code in this chapter ran successfully]')
