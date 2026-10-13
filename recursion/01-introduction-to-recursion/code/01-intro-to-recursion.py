def printNum(num):
    print(num)
    printNum(num-1)

def printNumfour(num):
    print(num)
    printNumthree(num-1)

def printNumthree(num):
    print(num)
    printNumtwo(num-1)


def printNumtwo(num):
    print(num)
    printNumone(num-1)


def printNumone(num):
    print(num)



printNum(5)
print("hello World")

