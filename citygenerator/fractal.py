import random
import math
import copy
import numpy as np
from . import utils
from . import heights
from . import randomiser
from . import greenery


def streetwidth(n, randomness=0, layout="s", delta=1):
    """ Function that returns a random street width. The width depends on level of iteration.
    :param n: current number of blocks
    :param randomised: whether width is random number in interval or set width
    :param degree: degree of randomness
    :param layout: large, small or None
    :param delta: spatial resolution, default is 1 m
    :return: random street width
    """""
    # initialise street width, values in metres:
    boulevard = [27, 36]
    highstreet = [18, 30]
    residentialstreet = [12, 18]
    mews = [8, 12]

    if layout in ["large", "l"]:
        # chose street type by number of existing blocks:
        if n == 1:
            widths = boulevard
        elif 2 <= n <= 5:  # n can actually only be 4
            widths = highstreet
        elif 6 <= n <= 11:  # n can actually only be 7 or 10
            widths = residentialstreet
        else:
            widths = mews
    elif layout in ["small", "s"]:
        if n <= 4:
            widths = residentialstreet
        else:
            widths = mews
    else:
        # chose street type by number of existing blocks:
        if n == 1:
            widths = highstreet
        elif 2 <= n <= 8:  # n can actually only be 4 or 7
            widths = residentialstreet
        else:
            widths = mews
    
    # get a set of widths that are conform with the resolution
    interval = np.arange(widths[0], widths[1] + delta, delta)
    width = randomiser.draw_from_interval(interval, randomness, weight='mid')

    return width


def randomblock(blocks, xwidth, ywidth, order, minwidth=10):
    n = len(blocks)

    if order in ["random", "r"]:
        j = random.randrange(n)  # pick random block
        # test if block is large enough if not move to next one
        i = 0
        while (i <= 5 * n) and (xwidth >= (blocks[j][1] - blocks[j][0] - minwidth)) or \
                (ywidth >= (blocks[j][3] - blocks[j][2] - minwidth)):
            j = random.randrange(n)  # pick another random block
            i += 1
        # if we cannot find a block after 5n iterations, return none
        if i >= 5 * n:
            print("Warning: blocks are too small, further block division stopped.")
            return

    elif order in ["hierarchical", "h"]:
        j = 0
        # test if block is large enough if not move to next one
        while (j <= n) and (xwidth >= (blocks[j][1] - blocks[j][0] - minwidth)) or \
                (ywidth >= (blocks[j][3] - blocks[j][2] - minwidth)):
            j += 1
        # if all blocks are too small, return none
        if j >= n:
            print("Warning: blocks are too small, further block division stopped.")
            return

    elif order in ["cascade", "c"]:
        if n == 1:
            j = 0
        else:
            # find block with largest area amongst newest blocks
            bmax = np.argmax([utils.blockplan([block]) for block in blocks[-4:]])
            j = bmax + (n - 4)
            # if block is too small, return none
            if (j <= n) and (xwidth >= (blocks[j][1] - blocks[j][0] - minwidth)) or \
                    (ywidth >= (blocks[j][3] - blocks[j][2] - minwidth)):
                print("Warning: blocks are too small, further block division stopped.")
                return

    else:
        raise ValueError("The input order could not be found."
                         "Options for order are: 'random', 'hierarchical' and 'cascade'.")

    return j


def intersection(corners, width, randomness=0., minwidth=10, delta=1):
    # minwidth is dimensional parameter (in metres)

    lowcorner = corners[0] + minwidth + math.floor(width/delta/2)*delta
    highcorner = corners[1] - minwidth - math.ceil(width/delta/2)*delta
    # get a set of widths that are conform with the resolution
    interval = np.arange(lowcorner, highcorner + delta, delta)
    intersec = randomiser.draw_from_interval(interval, randomness, weight='mid')

    return intersec


def newcorners(corners, separation, width, delta):
    min1 = corners[0]
    max1 = separation - math.floor(width/delta/2)*delta
    min2 = separation + math.ceil(width/delta/2)*delta
    max2 = corners[1]
    return [min1, max1], [min2, max2]


def generate(xsize, ysize, zsize, imax, jtot, kmax, 
             pbuild, pgreen, pfrontal, order="random",
             layoutrandom=0., heightrandom=0.,
             margin=4, minwidth=5, minvolume=10,
             savesteps=False):
    # margin, minwidth and minvolume are currently all dimensional parameters,
    # think about this when setting standards!
    
    a0 = xsize * ysize  # domain size
    # resolution
    dx = xsize/imax
    dy = ysize/jtot
    dz = zsize/kmax
    percentage = pbuild + pgreen  # target build-up density
    blocks = []

    xwidth = streetwidth(n=1, randomness=layoutrandom, delta=dx)
    ywidth = streetwidth(n=1, randomness=layoutrandom, delta=dy)

    # main intersection in upper right corner
    ablocks = (xsize - xwidth) * (ysize - ywidth)
    blocks.append([margin, xsize + margin - xwidth, 
                   margin, ysize + margin - ywidth])

    generationsteps = []
    # to save intermediate layouts
    if savesteps is True:
        generationsteps.append(copy.deepcopy(blocks))

    # MAIN LOOP
    # split blocks until buildup surface area is small enough
    while ablocks > 1.1*(a0 * percentage):

        nbl = len(blocks)  # number of blocks

        # pick random street widths
        xwidth = streetwidth(n=nbl, randomness=layoutrandom, delta=dx)
        ywidth = streetwidth(n=nbl, randomness=layoutrandom, delta=dy)
        
        # pick block according to defined order. if none, order is random.
        j = randomblock(blocks=blocks, xwidth=xwidth, ywidth=ywidth, order=order, minwidth=2*minwidth)
        # if no suitable block found, return blocks as they are
        if j is None:
            break

        # pick random intersection point
        xintersection = intersection(corners=blocks[j][0:2], width=xwidth, randomness=layoutrandom, minwidth=minwidth, delta=dx)
        yintersection = intersection(corners=blocks[j][2:4], width=ywidth, randomness=layoutrandom, minwidth=minwidth, delta=dy)
            
        # create new block coordinates
        # takes [xmin xmax] of block j
        x1, x2 = newcorners(corners=blocks[j][0:2], separation=xintersection, width=xwidth, delta=dx)
        # takes [ymin ymax] of block j
        y1, y2 = newcorners(corners=blocks[j][2:4], separation=yintersection, width=ywidth, delta=dy)

        # put together 4 new blocks and add block area to list
        newblock1 = [*x1, *y1]  # for python<3.5: newblock1 = x1 + y1
        newblock2 = [*x2, *y1]
        newblock3 = [*x2, *y2]
        newblock4 = [*x1, *y2]

        # add new blocks to blocks list
        blocks.extend([newblock1, newblock2, newblock3, newblock4])

        # remove old block
        del blocks[j]

        # compute new block area
        ablocks = sum([utils.blockplan([b]) for b in blocks])

        if savesteps is True:
            generationsteps.append(copy.deepcopy(blocks))

    # define blocks that are greenspace
    tmpblocks, tmpgreen = greenery.convert(blocks=blocks, target=(pgreen * a0))

    # add heights to blocks and add zero height to greenery
    blocks3d, heightgenerationsteps = heights.generate(blocks=tmpblocks, target=(pfrontal * a0), randomness=heightrandom, maxheight=round(zsize/6), minvolume=minvolume, delta=dz, savesteps=savesteps)
    greenspace, greenheights = heights.generate(blocks=tmpgreen, target=0)
    
    if savesteps is True:
        generationsteps.extend(copy.deepcopy(heightgenerationsteps))
     
    return blocks3d, greenspace, generationsteps
