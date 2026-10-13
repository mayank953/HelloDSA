def checkSorted(l1):
    if(len(l1)==0 or len(l1)==1):
        return True
    
    ans = checkSorted(l1[1:])

    if(l1[0] < l1[1]):
        return ans
    else:
        return False
    

def checkSorted2(l1):
    if(len(l1)==0 or len(l1)==1):
        return True
    
    if(l1[0] >= l1[1]):
        return False
    
    return checkSorted2(l1[1:])


l3 = [i for i in range(10000,1,-1) ]
# print(l3)
print(checkSorted2(l3))


