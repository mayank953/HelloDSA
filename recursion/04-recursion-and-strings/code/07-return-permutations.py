def return_permutations(s1):
    if(s1==''):  # Base Case
        return ['']

    currentChar = s1[0]
    permutationsOfSmallString = return_permutations(s1[1:]) # ['bc' ,'cb]

    allPermutations = []

    for eachPerm in permutationsOfSmallString:

        for position in range(0,len(eachPerm)+1):
            allPermutations.append(eachPerm[0:position] + currentChar + eachPerm[position:])

    return allPermutations



ans = return_permutations('abc')
print(ans)