def ReturnAllIndicesAsAList(l1,x,index):
    if(len(l1) == index):
        return []

    smallList = ReturnAllIndicesAsAList(l1,x,index+1)
    
    if(l1[index]==x):
        smallList.insert(0,index)
    
    return smallList

ansList = ReturnAllIndicesAsAList([3,2,5,2,8,2,1],2,0) 

print(ansList)

# [1,3,5]

