def factHead(n):
    if(n==0):
        return 1
    smallAnswer = factHead(n-1)

    finalAnswer = n * smallAnswer

    return finalAnswer

print(factHead(5))

def factTailWrong(n):
    if(n==0):
        return 1

    return n * factTailWrong(n-1)

def factTail(n,accumulator = 1):
    if(n==0):
        return accumulator
    
    accumulator = accumulator * n

    return factTail(n-1,accumulator)

