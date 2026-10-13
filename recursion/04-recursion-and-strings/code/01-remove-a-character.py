def remove_character(s1,ch):
    if(len(s1)==0 or s1==''):
        return s1
    
    smallAnswer = remove_character(s1[1:],ch)

    if(s1[0]==ch):
        return smallAnswer
    else:
        return s1[0] + smallAnswer
    


s1 = "abczz"
ans = remove_character(s1,'z')
print(ans)