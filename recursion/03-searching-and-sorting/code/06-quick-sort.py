

def partitionFunction(l1,s,e):
    pivot = l1[e]

    i = s
    rightPosition = s

    while(i <= e-1):
        if(l1[i]<pivot):
            rightPosition +=1
        i+=1 
    l1[rightPosition] , l1[e] = l1[e] , l1[rightPosition]
    pivotIndex = rightPosition
    # Now make sure that everything smaller than pivot to left and greater to right
    start = s
    end = e

    while(start<pivotIndex and end > pivotIndex):
        if(l1[start]< pivot):
            start+=1
        elif(l1[end] >= pivot):
            end-=1
        else:
            l1[start],l1[end] = l1[end], l1[start]
            start+=1
            end-=1
    
    return pivotIndex

# l1=[3,6,7,2,1,4,5]

# partitionFunction(l1,0,len(l1)-1)
# print(l1)



def QuickSort(l1,s,e):
    if(s>=e):
        return
    
    pivotIndex = partitionFunction(l1,s,e)

    QuickSort(l1,s,pivotIndex-1)
    QuickSort(l1,pivotIndex+1,e)
    return


l1=[3,6,7,2,1,4,5,4]


QuickSort(l1,0,len(l1)-1)
print(l1)