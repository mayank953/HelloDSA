
def firstIndexOfAnElementBetter(l1,x,index):
    # 1. Base Case
    if(len(l1)==index):
        return -1
    
    if(l1[index]==x):
        return index
    
    return firstIndexOfAnElementBetter(l1,x,index+1)



def printAllIndicesOfAnElementHelper(l1,x,index):
    if(len(l1)==index):
        return
    
    printAllIndicesOfAnElementHelper(l1,x,index+1)

    if(l1[index]==x):
        print(index)


    



def printAllIndicesOfAnElement(l1,x):
    #Helper Function 
    printAllIndicesOfAnElementHelper(l1,x,0)





printAllIndicesOfAnElement([3,2,5,2,8,2,1],2)
