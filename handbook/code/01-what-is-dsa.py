"""01. What Are Data Structures and Algorithms?

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 01-what-is-dsa.py
"""

names_list = ["Asha", "Ravi", "Meera", "Karan", "Zoya"]      # a list: sticky notes in a pile
names_set = {"Asha", "Ravi", "Meera", "Karan", "Zoya"}        # a set: the indexed diary

print("Karan" in names_list)   # Python checks the notes one by one until it finds Karan
print("Karan" in names_set)    # Python jumps straight to the right place
print("Nobody" in names_list)  # to say 'no', the list has to read every single note

def steps_to_find_in_list(items, target):
    """How many items do we look at before we can answer?"""
    steps = 0
    for item in items:
        steps += 1
        if item == target:
            break
    return steps

friends = [f"friend{i}" for i in range(1_000_000)]

print("first friend:", steps_to_find_in_list(friends, "friend0"))
print("last friend :", steps_to_find_in_list(friends, "friend999999"))
print("not a friend:", steps_to_find_in_list(friends, "stranger"))

def linear_checks(sorted_numbers, target):
    checks = 0
    for value in sorted_numbers:
        checks += 1
        if value == target:
            return checks
    return checks

def binary_checks(sorted_numbers, target):
    low, high, checks = 0, len(sorted_numbers) - 1, 0
    while low <= high:
        mid = (low + high) // 2
        checks += 1
        if sorted_numbers[mid] == target:
            return checks
        if sorted_numbers[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return checks

numbers = list(range(10_000_000))
print("linear scan :", linear_checks(numbers, 7_654_321), "checks")
print("binary search:", binary_checks(numbers, 7_654_321), "checks")

# Tiny practice: the method on a very small problem.
# Problem: "sum all numbers in a list".
#
# Step 2 (examples):   [] -> 0     [4] -> 4     [4, 1, 7] -> 12
# Step 3 (smaller):    the sum of [4, 1, 7] = 4 + (the sum of [1, 7])
# Step 4 (assume):     somebody hands me the sum of [1, 7] = 8
# Step 5 (my part):    add my own 4 to it -> 12
# Step 6 (base case):  the sum of an empty list is 0
def total(numbers):
    if len(numbers) == 0:
        return 0
    return numbers[0] + total(numbers[1:])

print(total([4, 1, 7]))

print('\n[all code in this chapter ran successfully]')
