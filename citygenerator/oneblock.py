import math


def generate(xsize, ysize, lp, lf,
            margin=8, zmargin=0, exact=False):

    '''Function that generates a single block from the input parameters.
    Required:
    :param xsize, ysize:  horizontal domain size.
    :param lp: building area density.
    :param lf: frontal aspect ratio.
    Optional:
    :param margin: margin at the domain boarder.
    :param exact: -True for most exact lp
                -False for approximate area that is closer to a square'''
    
    # initialise blocks and block area
    a0 = xsize * ysize
    atarget = a0 * lp
    htarget = a0 * lf

    ytmp = math.floor(math.sqrt(atarget))
    
    if exact is True:
        testrange = range(ytmp)
    else:
        testrange = range(round(0.1*xsize))
        
    for i in testrange:
        y = ytmp - i
        xtmp = atarget/y
        if xtmp == round(xtmp):
            break
    x = round(xtmp)
    
    z = round(htarget/y)

    blocks =  [[margin, x+margin, margin, y+margin, zmargin, z+zmargin]]

    return blocks
