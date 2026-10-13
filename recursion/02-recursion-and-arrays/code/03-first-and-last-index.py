def firstIndexOfAnElement(l1,x):
    # 1. Base Case
    if(len(l1)==0):
        return -1
    
    if(l1[0]==x):
        return 0
    
    ansFromRecursion =  firstIndexOfAnElement(l1[1:],x)

    if(ansFromRecursion==-1):
        return ansFromRecursion
    else:
        return ansFromRecursion +1



def lastIndexOfAnElement(l1,x):
    # 1. Base Case
    if(len(l1)==0):
        return -1
    

print(firstIndexOfAnElement([3,2,5,2,8,2,1],2))
print(firstIndexOfAnElement([3,2,5,2,8,2,1],10))
print(firstIndexOfAnElement([3,2,5,2,8,2,1],1))