def sumArray(l1):
    # print(l1)
    if(len(l1)==0):
        return 0
    sumOfLeftOverArray = sumArray(l1[1:])
    ans = sumOfLeftOverArray+l1[0]
    return ans

def sumArray2(l1):

    if(len(l1)==0):
        return 0

    ans =  l1[0] + sumArray(l1[1:])

    return ans


def sumArray_Tail(l1,accumulator=0):
    if(len(l1)==0):
        return accumulator
    
    accumulator += l1[0]

    return sumArray_Tail(l1[1:],accumulator)



print(sumArray([1,2,3,4,5]))

print(sumArray([]))
print(sumArray2([1,2,3,4,5]))
print(sumArray_Tail([]))
print(sumArray_Tail([1,2,3,4,5]))
