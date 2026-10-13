functionCallNumber = 1

def fibonicci(n):
    global functionCallNumber
    print("The function call is " + str(functionCallNumber) +" for " + str(n) )
    functionCallNumber+=1

    # print(n)
    if(n==0):
        return 1
    if(n==1):
        return 1

    last = fibonicci(n-1)
    secondLast = fibonicci(n-2)

    ans = last + secondLast

    return ans

print(fibonicci(4))