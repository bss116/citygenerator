import random
import numpy as np
import copy
from citygenerator import utils
from citygenerator import randomiser


def uniform(blocks, height):
    blocks3d = []
    for block in blocks:
        xy = [b for b in block[0:4]]
        z = [0, height]
        blocks3d.append(xy + z)

    return blocks3d


def heightlist(blocks, heights):
    blocks3d = []
    for block, height in zip(blocks, heights):
        xy = [b for b in block[0:4]]
        z = [0, height]
        blocks3d.append(xy + z)

    return blocks3d


def generate(blocks, target, randomness=0., maxheight=50, minvolume=None, delta=1, savesteps=False):
    # minvolume is dimensional parameter
    
    generationsteps = []
    # to save intermediate layouts
    if savesteps is True:
        generationsteps.append(copy.deepcopy(blocks))

    if target is 0:
        blocks3d = uniform(blocks, 1*delta)
    else:
        # make a volume check to avoid too small blocks
        if minvolume is not None:
            zmins = []
            for block in blocks:
                zmin = round(minvolume**3/((block[1] - block[0])*(block[3] - block[2])))
                zmins.append(zmin)

            if randomness == 0.:
                # set minimum volume same for all blocks
                minheight = max(zmins)
                blocks3d = uniform(blocks, minheight)
            else:
                blocks3d = heightlist(blocks, zmins)
                
        hblocks = utils.blockfront(blocks3d)
        
        # to save intermediate layouts
        if savesteps is True:
            generationsteps.append(copy.deepcopy(blocks3d))

        n = len(blocks)
        j = 0
        #  add height for as long as blocks are below lf
        while hblocks < target:
            # adjust maximum height
            currentheight = blocks3d[j][5]
            cap = maxheight - currentheight
            # if block has not reached maximum height
            if cap > 1:
                interval = np.arange(delta, cap + delta, delta)
                blocks3d[j][5] += randomiser.low(interval, randomness)
            hblocks = utils.blockfront(blocks3d)
            
            # to save intermediate layouts
            if savesteps is True:
                generationsteps.append(copy.deepcopy(blocks3d))


            j += 1
            j %= n
            
    # to save intermediate layouts
    if savesteps is True:
        generationsteps.append(copy.deepcopy(blocks3d))

    return blocks3d, generationsteps
