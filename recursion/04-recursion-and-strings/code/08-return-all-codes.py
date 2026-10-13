def get_char(value):
    if(value<=0 or value>26):
        return ""
    
    return chr(97+value-1)


def return_all_codes(input):
    if(input==''):     # base case
        return ['']
    
    if(len(input)==1):
        singleChar = get_char(int(input))
        return [singleChar]


    singleDigit = int(input[0:1])
    doubleDigit = int(input[0:2]) 
    mainAns = []

    ansWithoutFirstDigit = return_all_codes(input[1:])

    for eachAns in ansWithoutFirstDigit:
        mainAns.append(get_char(singleDigit)+eachAns)


    if(doubleDigit>=10 and doubleDigit<=26):
        ansWithoutDoubleDigit  = return_all_codes(input[2:])
        for eachAns in ansWithoutDoubleDigit:
            mainAns.append(get_char(doubleDigit)+eachAns)

    return mainAns


ans = return_all_codes('123')
print(ans)