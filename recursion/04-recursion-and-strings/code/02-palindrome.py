def palindrome_helper(s1,start,end):
 
    if(start>=end):
        return True
    
    if(s1[start]!= s1[end]):
        return False
    
    return palindrome_helper(s1,start+1,end-1)
    

def palindrome(s1):
    return palindrome_helper(s1,0,len(s1)-1)



print(palindrome('nitinr'))