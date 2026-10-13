def power2(n):
    if(n==1): # base case (1)
        return 2

    smallAnswer = power2(n-1) # Assume (2) -> Induction Hypothesis

    ans = 2* smallAnswer # (3) using (2)

    return ans



print(power2(5))