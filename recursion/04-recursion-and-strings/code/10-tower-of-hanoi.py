step =1

def tower_of_hanoi(n,source,destination,auxiliary):
    global step
    if(n==0):
        return 
    if(n==1):
        print(step ,source,'-->',destination)
        step+=1
        return

    tower_of_hanoi(n-1,source,auxiliary,destination)
    print(step,source,'-->',destination)
    step+=1
    tower_of_hanoi(n-1,auxiliary,destination,source)
        


n = 5
tower_of_hanoi(n,'source','destination','auxilliary')

# https://yongdanielliang.github.io/animation/web/TowerOfHanoi.html