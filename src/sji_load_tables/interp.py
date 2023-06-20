import bisect

def interp(x,xp,fp,left=None,right=None):
    
    # Value out of bounds
    if x < xp[0]:
        return left
    if x > xp[-1]:
        return right
    
    # Special case where search value is first entry in xp
    if x == xp[0]:
        return fp[0]
        
    i = bisect.bisect_left(xp,x)
    return fp[i-1] + (fp[i]-fp[i-1])*((x-xp[i-1])/(xp[i]-xp[i-1]))

    
def run_examples():
    xp = [0,1,2,3,4,5]
    fp = [0,2,-6,6,333,20]    
    print(interp(-0.1,xp,fp))
    print(interp(0,xp,fp))
    print(interp(0.5,xp,fp))
    print(interp(1.0,xp,fp))
    print(interp(1.3,xp,fp))
    print(interp(5,xp,fp))
    print(interp(5.33,xp,fp))
    
if __name__ == '__main__':
    run_examples()