import sys
# print(sys.getrecursionlimit())


# sys.setrecursionlimit(100)

def factorial(n):

    smallAns = factorialfour(n-1)
    ans = n*smallAns
    return ans 

def factorialfour(n):
    smallAns = factorialthree(n-1)
    ans = n*smallAns
    return ans 

def factorialthree(n):
    smallAns = factorialtwo(n-1)
    ans = n*smallAns
    return ans 
def factorialtwo(n):

    smallAns = factorialone(n-1)
    ans = n*smallAns
    return ans 

def factorialone(n):

    
    return 1 

print(factorial(5))