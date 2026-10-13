"""15. Linked Lists

All runnable code from this chapter of the Hello DSA Handbook, in order.
Run it with: python 15-linked-list.py
"""

class Node:
    def __init__(self, data, next=None):
        self.data = data          # the value stored in this node
        self.next = next          # the next node (or None at the end)

# Build 7 -> 2 -> 9 by hand, from the back to the front.
third = Node(9)
second = Node(2, third)
head = Node(7, second)

print(head.data, head.next.data, head.next.next.data, head.next.next.next)

def from_list(items):
    head = None
    for value in reversed(items):          # build from the back so each new node points at the rest
        head = Node(value, head)
    return head

def to_list(head):
    items = []
    while head is not None:                # walk until we fall off the end
        items.append(head.data)
        head = head.next
    return items

def show(head):
    parts = []
    while head is not None:
        parts.append(str(head.data))
        head = head.next
    print(" -> ".join(parts + ["None"]))

show(from_list([7, 2, 9, 4]))

def length(head):
    count, current = 0, head
    while current is not None:
        count += 1
        current = current.next
    return count

def get_at(head, index):
    """Walk `index` steps to find a value, and count the steps taken."""
    steps, current = 0, head
    while current is not None and steps < index:
        current = current.next
        steps += 1
    return (current.data if current else None), steps

big = from_list(list(range(1, 100_001)))
print("length:", length(big))
print("value at index 99,999 needed", get_at(big, 99_999)[1], "steps (an array needs 1)")

def length_recursive(head):
    if head is None:                          # base case: the empty list has length 0
        return 0
    return 1 + length_recursive(head.next)    # my node, plus the length of the rest

def sum_recursive(head):
    if head is None:
        return 0
    return head.data + sum_recursive(head.next)

def print_reversed(head):
    if head is None:
        return
    print_reversed(head.next)                 # the rest FIRST (chapter 8: work after the call)
    print(head.data, end=" ")                 # then me, on the way back up

values = from_list([7, 2, 9, 4])
print(length_recursive(values), sum_recursive(values))
print_reversed(values)
print()

def insert_at_head(head, value):
    return Node(value, head)                   # O(1): the new node points at the old head

def insert_at_tail(head, value):
    new_node = Node(value)
    if head is None:
        return new_node
    current = head
    while current.next is not None:            # walk to the last node: O(n)
        current = current.next
    current.next = new_node
    return head

def insert_at(head, index, value):
    if index == 0:
        return Node(value, head)
    current = head
    for _ in range(index - 1):                 # stop at the node just BEFORE the spot
        if current is None:
            raise IndexError("index out of range")
        current = current.next
    if current is None:
        raise IndexError("index out of range")
    current.next = Node(value, current.next)   # new node -> rest, THEN front -> new node (one line, safe)
    return head

lst = from_list([7, 2, 9])
lst = insert_at_head(lst, 1)
lst = insert_at_tail(lst, 4)
lst = insert_at(lst, 2, 5)
show(lst)

def insert_recursive(head, index, value):
    if index == 0:                                         # this is the spot
        return Node(value, head)
    if head is None:
        raise IndexError("index out of range")
    head.next = insert_recursive(head.next, index - 1, value)   # assume: the rest handles it
    return head                                            # my node stays; reconnect to the updated rest

demo = from_list([7, 2, 9])
demo = insert_recursive(demo, 1, 5)
show(demo)

def delete_at(head, index):
    if head is None:
        raise IndexError("index out of range")
    if index == 0:
        return head.next                       # the head is removed: the next node becomes the head
    current = head
    for _ in range(index - 1):
        current = current.next
        if current is None:
            raise IndexError("index out of range")
    if current.next is None:
        raise IndexError("index out of range")
    current.next = current.next.next           # skip over the doomed node
    return head

def delete_value(head, value):
    """Recursive: remove the first node holding `value`."""
    if head is None:
        return None
    if head.data == value:
        return head.next
    head.next = delete_value(head.next, value)
    return head

lst2 = from_list([7, 2, 9, 4])
lst2 = delete_at(lst2, 1)
lst2 = delete_value(lst2, 4)
show(lst2)

def reverse(head):
    previous, current = None, head
    while current is not None:
        following = current.next        # save the rest BEFORE we break the link
        current.next = previous         # flip the arrow
        previous = current              # move both pointers forward
        current = following
    return previous                     # the old tail is the new head

show(reverse(from_list([1, 2, 3, 4])))

def reverse_recursive(head):
    if head is None or head.next is None:         # base case: 0 or 1 nodes are already reversed
        return head
    new_head = reverse_recursive(head.next)       # assume: the rest, reversed. head.next is now its LAST node
    head.next.next = head                         # my part: make that last node point back at me
    head.next = None                              # I am now the tail
    return new_head

show(reverse_recursive(from_list([1, 2, 3, 4])))

def middle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next                 # one step
        fast = fast.next.next            # two steps
    return slow

print(middle(from_list([1, 2, 3, 4, 5])).data, middle(from_list([1, 2, 3, 4])).data)

def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:                  # they met: there must be a loop
            return True
    return False

looped = from_list([1, 2, 3, 4, 5])
tail = looped
while tail.next:
    tail = tail.next
tail.next = looped.next.next              # link the last node back to node "3"
print(has_cycle(looped), has_cycle(from_list([1, 2, 3])))

def merge_sorted(a, b):
    dummy = Node(0)                       # a placeholder to hang the result on
    tail = dummy
    while a is not None and b is not None:
        if a.data <= b.data:
            tail.next, a = a, a.next      # take the smaller node
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a is not None else b # attach whatever is left
    return dummy.next

show(merge_sorted(from_list([1, 4, 6]), from_list([2, 3, 7, 9])))

def remove_nth_from_end(head, n):
    dummy = Node(0, head)
    front = back = dummy
    for _ in range(n + 1):                # get `front` n+1 steps ahead
        front = front.next
    while front is not None:              # move both until front falls off the end
        front = front.next
        back = back.next
    back.next = back.next.next            # `back` is just before the doomed node
    return dummy.next

show(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2))

def is_palindrome_list(head):
    if head is None or head.next is None:
        return True
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow, fast = slow.next, fast.next.next
    second_half = reverse(slow.next)           # reverse everything after the middle
    first, second, answer = head, second_half, True
    while second is not None:
        if first.data != second.data:
            answer = False
            break
        first, second = first.next, second.next
    slow.next = reverse(second_half)           # put the list back the way we found it
    return answer

print(is_palindrome_list(from_list([1, 2, 3, 2, 1])), is_palindrome_list(from_list([1, 2, 3])))

print('\n[all code in this chapter ran successfully]')
