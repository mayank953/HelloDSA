
ansList=[]


def UpdateAllIndicesOfAnElementInGlobalList(l1,x,index):
    if(len(l1)==index):
        return
    
    if(l1[index]==x):
        ansList.append(index)

    UpdateAllIndicesOfAnElementInGlobalList(l1,x,index+1)




UpdateAllIndicesOfAnElementInGlobalList([3,2,5,2,8,2,1],2,0)

print(ansList)