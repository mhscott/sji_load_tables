import bisect

def interp(x,xp,fp,left=None,right=None):
    '''Linear interpolation from a list
    
    Parameters:
        x: The input value
        xp: The input list
        fp: The output list
        left: The value to return if x is less than the first value in xp (default None)
        right: The value to return if x is greaterh than the last value in xp (default None)
    '''
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
