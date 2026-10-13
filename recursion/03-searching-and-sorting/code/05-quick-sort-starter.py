'''
Sorting Using Recursion

Merge Sort  ✅
     
Quick Sort



'''

def partitionFunction(l1,s,e):
    pass  

def QuickSort(l1,s,e):
    if(s>=e):
        return
    
    pivotIndex = partitionFunction(l1,s,e)

    QuickSort(l1,s,pivotIndex-1)
    QuickSort(l1,pivotIndex+1,e)
    return


l1=[3,6,7,2,1,4,5]

QuickSort(l1,0,len(l1)-1)
print(l1)