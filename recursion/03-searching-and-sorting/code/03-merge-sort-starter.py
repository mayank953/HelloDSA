''' 
Sorting Using Recursion.

Merge Sort

'''

def Merge(l1,s,m,e):
    pass


def MergeSort(l1,s,e):
    if(s>=e):
        return
    
    m = s + (e-s)//2

    MergeSort(l1,s,m)
    MergeSort(l1,m+1,e)

    Merge(l1,s,m,e)
    
    return


l1 = [1,10,3,16,9,15]

l1 = [1,3,10,    9,15,16]

MergeSort(l1,0,len(l1)-1)