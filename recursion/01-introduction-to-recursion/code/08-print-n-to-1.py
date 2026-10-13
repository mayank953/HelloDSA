def printNto1(n):
    if(n<=0): # base Case
        return

    print(n)
    printNto1(n-1) # Recursion - Tail Recursion


printNto1(5)