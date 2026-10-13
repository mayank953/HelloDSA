"""

Searching Using Recursion

1. Linear Search - Done
2. Binary Search

"""

def BinarySearchUsingRecursionHelper(l1,x,s,e):
    if(s>e):
        return False
    
    m = s + (e-s)//2

    if(l1[m]==x):
        return True

    if(x > l1[m]):
        return BinarySearchUsingRecursionHelper(l1,x,m+1,e)
    
    return BinarySearchUsingRecursionHelper(l1,x,s,m-1)


def BinarySearchUsingRecursion(l1,x):
    return BinarySearchUsingRecursionHelper(l1,x,0,len(l1)-1)

l1 = [i for i in range(10000000)] 

print(BinarySearchUsingRecursion(l1,100))