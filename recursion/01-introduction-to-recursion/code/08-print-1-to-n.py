def print1ToN(n):
    if(n<=0): # base Case
        return

    print1ToN(n-1) # Recursion Call - Head 

    print(n)

print1ToN(5)