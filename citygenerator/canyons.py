import numpy as np
import copy
import math
import operator
import matplotlib.pyplot as plt
import seaborn as sns
import citygenerator as cgen


def getcanyons(blocks, limits):

    if blocks:  # if blocks not empty list
        # move blocks into left corner
        initblocks = sorted(blocks, key=operator.itemgetter(2,0))
        xshift = initblocks[0][0]  # first block xmin
        yshift = initblocks[0][2]  # first block ymin
        allblocks = cgen.utils.blockshift(initblocks, limits, xshift, yshift)
        fullcanyons = generate(allblocks, limits)
        # shift back
        canyons = cgen.utils.blockshift(fullcanyons, limits, -xshift, -yshift)
    else:
        canyons = [limits]
        fullcanyons = [limits]
        
    return canyons, fullcanyons


def generate(blocks, limits):
    
    testblocks = copy.deepcopy(blocks)
    x0 = limits[0]
    imax = limits[1]
    y0 = limits[2]
    jtot = limits[3]
    canyons = []

    for block in testblocks:
        # 1. compare to other blocks and find all in same row
        samerow = []
        for otherblock in blocks:
            # show which blocks are at same y-heights:
            if block[2] <= otherblock[2] < block[3]:
                samerow.append(otherblock)
            # block[2] truely smaller than otherblock[3] to 
            # not catch the ones that end where my block begins
            elif block[2] < otherblock[3] <= block[3]:
                samerow.append(otherblock)
            elif otherblock[2] <= block[2] < otherblock[3]:
                samerow.append(otherblock)
            elif otherblock[2] < block[3] <= otherblock[3]:
                samerow.append(otherblock)

        # 2. find closest block in y: sort first by y then by x
        samerow = sorted(samerow, key=operator.itemgetter(2,0))
        for otherblock in samerow:
        # show only blocks with larger x start. because we sorted,
        # the first hit should always be the next block in y-line
            if block[1] <= otherblock[0]:
                nextblocky = copy.deepcopy(otherblock)
                # when first block in same row found, break and go to next
                break
            # no block with larger x, we are at end of line
            else:
                # imaginative block with same y coordinates as original block
                # and xcoordinates at domain end
                nextblocky = [imax, imax, block[2], block[3]] 

        # 3. find closest block in x: sort first by x then by y
        samerow = sorted(samerow, key=operator.itemgetter(0,2))
        for otherblock in samerow:
        # show only blocks with larger x start. because we sorted,
        # the first hit should always be the next block in x-line
        # less or equal to also get adjecent blocks
            if block[1] <= otherblock[0]:
                nextblockx = copy.deepcopy(otherblock)
                # when first block in same row found, break and go to next
                break
            # no block with larger x, we are at end of line
            else:
                # imaginative block with same y coordinates as original block
                # and xcoordinates at domain end
                nextblockx = [imax, imax, block[2], block[3]]

        # 4. choose the right next block
        # compare x and y next blocks:
        if nextblockx == nextblocky:
            nextblock = copy.deepcopy(nextblocky)

        # if xblock is same shape as block just shifted then use it
        elif block[2:4] == nextblockx[2:4]:
            nextblock = copy.deepcopy(nextblockx)

        # if x block is adjecent to block or some block overlap
        # choose y block and make it smaller by x block
        elif block[2] < nextblockx[2] and nextblockx[2] < nextblocky[3]:
            nextblock = copy.deepcopy(nextblocky)
            nextblock[3] = nextblockx[2]

        else:
            print("Canyon case that has not been defined!")
            nextx1 = min(nextblockx[0], nextblocky[0])
            nextx2 = min(nextblockx[1], nextblocky[1])
            nexty1 = min(nextblockx[2], nextblocky[2])
            nexty2 = min(nextblockx[3], nextblocky[3])
            nextblock = [nextx1, nextx2, nexty1, nexty2]

        # 5. if ymax of first block is larger define leftover block
        if nextblock[3] < block[3]:
            # adjecent
            if block[1] == nextblockx[0]:
                # and in corner
                if nextblock[3] == nextblockx[2]:
                    leftblock = [block[0], nextblockx[0], nextblockx[3], block[3]]
                else:
                    leftblock = [block[0], nextblockx[0], nextblockx[2], block[3]]
            else:
                leftblock = [block[0], nextblock[0], nextblock[3], block[3]]
                nextblock[3] = block[3]

            # if not just a line:
            if leftblock[3] > leftblock[2]:
                testblocks.append(leftblock)   
        # set nextblock ymax to first block ymax
        elif nextblock[3] > block[3]:
            nextblock[3] = block[3]

        # 6. check if there is a street canyon with no other blocks
        if block[2] < nextblockx[2] and block[2] < nextblocky[2]:
            nextblock = [imax, imax, block[2], nextblock[2]]

        # 7. define canyon in between
        # canyon x coordinates: xmin of first block, xmax of next block
        cxmin = block[1]
        cxmax = nextblock[0]
        # canyon y coordinates: ymin of first block, ymax of next block
        cymin = block[2]
        cymax = nextblock[3]
        canyon = [cxmin, cxmax, cymin, cymax]
        canyons.append(canyon)

    # 8. find canyon onlys
    # now sort first x then y
    allxblocks = sorted(blocks, key=operator.itemgetter(0,2))
    # find all blocks in first x column
    x1col = []
    for block in allxblocks:
        if block[0] == x0 and not all(b == 0 for b in block):
            x1col.append(block)

    cymins = [block[3] for block in x1col]
    ymaxs = [block[2] for block in x1col]
    cymaxs = [*ymaxs[1:], jtot] # discard first ymax and use jtot as final value

    for cymin, cymax in zip(cymins, cymaxs):    
        # check if there are blocks later on in that row
        samerow = []
        for otherblock in allxblocks:
            if cymin <= otherblock[2] < cymax:
                samerow.append(otherblock)
            elif cymin < otherblock[3] <= cymax:
                samerow.append(otherblock)
            elif otherblock[2] <= cymin < otherblock[3]:
                samerow.append(otherblock)
            elif otherblock[2] < cymax <= otherblock[3]:
                samerow.append(otherblock)
        if samerow:
            xmax = min([block[0] for block in samerow])
        else:
            xmax = imax
            
        xmin = x0
        ymin = cymin
        ymax = cymax

        canyon = [xmin, xmax, ymin, ymax]
        canyons.append(canyon)   
        
    return canyons


def generate_testversion(blocks, limits, showsteps=False):
    
    testblocks = copy.deepcopy(blocks)
    x0 = limits[0]
    imax = limits[1]
    y0 = limits[2]
    jtot = limits[3]
    canyons = []
    
    if showsteps is True:
        # setup
        n = 3*len(blocks)
        col = 4
        row = math.ceil(n/col)
        i = 0
        fig = plt.figure(figsize=(4*col, 3*row))    

    for block in testblocks:

        if showsteps is True:
            i += 1
            ax = fig.add_subplot(row, col, i)
            cgen.plot.layout(blocks, ax=ax, limits=limits, facecolor='xkcd:powder blue')
            cgen.plot.layout(canyons, ax=ax, limits=limits, facecolor='xkcd:light grey')

        # 1. compare to other blocks and find all in same row
        samerow = []
        for otherblock in blocks:
            # show which blocks are at same y-heights:
            if block[2] <= otherblock[2] < block[3]:
                samerow.append(otherblock)
            # block[2] truely smaller than otherblock[3] to 
            # not catch the ones that end where my block begins
            elif block[2] < otherblock[3] <= block[3]:
                samerow.append(otherblock)
            elif otherblock[2] <= block[2] < otherblock[3]:
                samerow.append(otherblock)
            elif otherblock[2] < block[3] <= otherblock[3]:
                samerow.append(otherblock)

        # 2. find closest block in y: sort first by y then by x
        samerow = sorted(samerow, key=operator.itemgetter(2,0))
        for otherblock in samerow:
        # show only blocks with larger x start. because we sorted,
        # the first hit should always be the next block in y-line
            if block[1] <= otherblock[0]:
                nextblocky = copy.deepcopy(otherblock)
                # when first block in same row found, break and go to next
                break
            # no block with larger x, we are at end of line
            else:
                # imaginative block with same y coordinates as original block
                # and xcoordinates at domain end
                nextblocky = [imax, imax, block[2], block[3]] 

        # 3. find closest block in x: sort first by x then by y
        samerow = sorted(samerow, key=operator.itemgetter(0,2))
        for otherblock in samerow:
        # show only blocks with larger x start. because we sorted,
        # the first hit should always be the next block in x-line
        # less or equal to also get adjecent blocks
            if block[1] <= otherblock[0]:
                nextblockx = copy.deepcopy(otherblock)
                # when first block in same row found, break and go to next
                break
            # no block with larger x, we are at end of line
            else:
                # imaginative block with same y coordinates as original block
                # and xcoordinates at domain end
                nextblockx = [imax, imax, block[2], block[3]]

        # 4. choose the right next block
        # compare x and y next blocks:
        if nextblockx == nextblocky:
            nextblock = copy.deepcopy(nextblocky)

        # if xblock is same shape as block just shifted then use it
        elif block[2:4] == nextblockx[2:4]:
            nextblock = copy.deepcopy(nextblockx)

        # if x block is adjecent to block or some block overlap
        # choose y block and make it smaller by x block
        elif block[2] < nextblockx[2] and nextblockx[2] < nextblocky[3]:
            nextblock = copy.deepcopy(nextblocky)
            nextblock[3] = nextblockx[2]

        else:
            print("Canyon case that has not been defined!")
            nextx1 = min(nextblockx[0], nextblocky[0])
            nextx2 = min(nextblockx[1], nextblocky[1])
            nexty1 = min(nextblockx[2], nextblocky[2])
            nexty2 = min(nextblockx[3], nextblocky[3])
            nextblock = [nextx1, nextx2, nexty1, nexty2]

        # 5. if ymax of first block is larger define leftover block
        if nextblock[3] < block[3]:
            # adjecent
            if block[1] == nextblockx[0]:
                # and in corner
                if nextblock[3] == nextblockx[2]:
                    leftblock = [block[0], nextblockx[0], nextblockx[3], block[3]]
                else:
                    leftblock = [block[0], nextblockx[0], nextblockx[2], block[3]]
            else:
                leftblock = [block[0], nextblock[0], nextblock[3], block[3]]
                nextblock[3] = block[3]

            # if not just a line:
            if leftblock[3] > leftblock[2]:
#                 leftblock[2] += 1
#                 leftblock[1] -= 1
                testblocks.append(leftblock)   
        # set nextblock ymax to first block ymax
        elif nextblock[3] > block[3]:
            nextblock[3] = block[3]

        # 6. check if there is a street canyon with no other blocks
        if block[2] < nextblockx[2] and block[2] < nextblocky[2]:
            nextblock = [imax, imax, block[2], nextblock[2]]


        # 7. define canyon in between
        # shift such that canyon center is defined one off of from block centre
        # canyon x coordinates: xmin of first block, xmax of next block
        cxmin = block[1]
        cxmax = nextblock[0]
        # canyon y coordinates: ymin of first block, ymax of next block
        cymin = block[2]
        cymax = nextblock[3]
#            # canyon x coordinates: xmin of first block, xmax of next block
#            cxmin = block[1]
#            cxmax = nextblock[0]
#            # canyon y coordinates: ymin of first block, ymax of next block
#            cymin = block[2]
#            cymax = nextblock[3]
        canyon = [cxmin, cxmax, cymin, cymax]
        canyons.append(canyon)

        if showsteps is True:
            cgen.plot.layout(samerow, ax=ax, limits=limits)
            cgen.plot.layout([nextblocky], ax=ax, limits=limits, facecolor='purple')
            cgen.plot.layout([nextblockx], ax=ax, limits=limits, facecolor='green')
            cgen.plot.layout([block], ax=ax, limits=limits, facecolor=(0,0,0,0), edgecolor='red')
            cgen.plot.layout([nextblock], ax=ax, limits=limits, facecolor=(0,0,0,0), edgecolor='blue')
            # cgen.plot.layout([canyon], ax=ax, limits=[0, imax, 0, jtot], facecolor='grey')

    if showsteps is True:
        i += 1
        ax = fig.add_subplot(row, col, i)
        cgen.plot.layout(blocks, ax=ax, limits=limits, facecolor='xkcd:powder blue')
        cgen.plot.layout(canyons, ax=ax, limits=limits, facecolor='xkcd:light grey')

    # 8. find canyon onlys
    # now sort first x then y
    allxblocks = sorted(blocks, key=operator.itemgetter(0,2))
    # find all blocks in first x column
    x1col = []
    for block in allxblocks:
        if block[0] == x0 and not all(b == 0 for b in block):
            x1col.append(block)

    cymins = [block[3] for block in x1col]
    ymaxs = [block[2] for block in x1col]
    cymaxs = [*ymaxs[1:], jtot] # discard first ymax and use jtot as final value

    for cymin, cymax in zip(cymins, cymaxs):    
        # check if there are blocks later on in that row
        samerow = []
        for otherblock in allxblocks:
            if cymin <= otherblock[2] < cymax:
                samerow.append(otherblock)
            elif cymin < otherblock[3] <= cymax:
                samerow.append(otherblock)
            elif otherblock[2] <= cymin < otherblock[3]:
                samerow.append(otherblock)
            elif otherblock[2] < cymax <= otherblock[3]:
                samerow.append(otherblock)
        if samerow:
            xmax = min([block[0] for block in samerow])
        else:
            xmax = imax
            
        xmin = x0  # Dales indices
        ymin = cymin
        ymax = cymax

        canyon = [xmin, xmax, ymin, ymax]
        canyons.append(canyon)   
        
        if showsteps is True:
            cgen.plot.layout([canyon], ax=ax, limits=limits, facecolor='grey')

    if showsteps is True:
        i += 1
        ax = fig.add_subplot(row, col, i)
        colors = sns.color_palette("cubehelix", len(canyons))
        for canyon, color in zip(canyons, colors):
            cgen.plot.layout([canyon], ax=ax, limits=limits, facecolor=color)

        plt.tight_layout()
        plt.show()
        
    return canyons
