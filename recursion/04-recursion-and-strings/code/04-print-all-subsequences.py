'''
Print all Subsequences of a given string
'''


def print_subsequences(s1,takenSoFar):
    if(s1=='' or len(s1)==0):
        print(takenSoFar)
        return
    
    currentChar = s1[0]
    smallInput = s1[1:]

    print_subsequences(smallInput,takenSoFar + currentChar)
    print_subsequences(smallInput,takenSoFar)

    return     


s1 = 'abc'
print_subsequences(s1,'')
