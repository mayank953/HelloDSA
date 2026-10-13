def return_subsequences(s1):
    if(s1==''): # base Case 
        ans = ['']
        return ans
    
    smallAns = return_subsequences(s1[1:]) # [ b,c ,bc,'']
    myChar = s1[0]
    ans = []
    ans.extend(smallAns) # ans = [ b,c ,bc,'']

    for eachPermutation in smallAns:
        ans.append(myChar + eachPermutation)
    
    return ans



s1 = 'abcd'
l1 = return_subsequences(s1)

print(l1)


