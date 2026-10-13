import sys
sys.setrecursionlimit(5000)


def sumOfNumbersTillN(n):
    if(n==1):
        return 1 #Base Case (1)
    
    smallAnswer = sumOfNumbersTillN(n-1) # Assume that I will get my answer

    ans = n + smallAnswer

    return ans





print(sumOfNumbersTillN(5))
print(sumOfNumbersTillN(1000))
