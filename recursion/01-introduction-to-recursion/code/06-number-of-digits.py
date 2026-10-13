def number_of_digits(n):
    if(n>=1 and n<=9):
        return 1
    elif (n==0):
        return 1
    
    smallNumber = int(n/10)
    smallAnswer = number_of_digits(smallNumber)

    ans = 1 + smallAnswer

    return ans



print(number_of_digits(0))
print(number_of_digits(123))
print(number_of_digits(542624))

