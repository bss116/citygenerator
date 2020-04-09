import numpy as np


def area(x, y):
    """Calculates the area of two given intervals x = [xmin xmax] and y = [ymin ymax]"""
    a = (x[1] - x[0]) * (y[1] - y[0])
    return a


def blockplan(blocks):
    """Returns sum of all block plan areas.
    Block entries stored as block = [xmin, xmax, ymin, ymax]"""
    areas = 0
    for block in blocks:
        x = block[0:2]
        y = block[2:4]
        areas += area(x, y)
    return areas


def blockfront(blocks):
    """Returns sum of all block frontal areas facing the wind.
    Wind is U wind only, the front is the y-z surface of blocks.
    Block entries stored as block = [xmin, xmax, ymin, ymax, zmin, zmax]"""
    areas = 0
    for block in blocks:
        y = block[2:4]
        z = block[4:6]
        areas += area(y, z)
    return areas


def length(interval):
    """Calculates the length of a given interval."""
    l = interval[1] - interval[0]
    return l


def areas(xarray, yarray):
    """Calculates the areas of two given arrays"""
    areas = [x * y for x, y in zip(xarray, yarray)]
    return areas


def normed_sum(array, norm):
    normsum = np.sum(array) / norm
    return normsum


def calculate_blockstats(blocks, a0=None):
    precision=4
    
    # number of blocks
    nblocks = len(blocks)

    # block length in z
    blockheights = [length(b[4:6]) for b in blocks]
    # block length in y
    blockwidths = [length(b[2:4]) for b in blocks]
    # block length in x
    blocklengths = [length(b[0:2]) for b in blocks]

    # block maximum height
    heightmax = np.max(blockheights)
    # block mean height
    heightmean = np.mean(blockheights)
    # block height standard deviation
    heightstd = np.std(blockheights)

    # block plan areas
    blockplans = areas(blocklengths, blockwidths)
    # block frontal areas for wind from x direction
    blockfronts = areas(blockwidths, blockheights)
    # block frontal areas for wind from y direction
    # blocksides = areas(blocklengths, blockheights)
    
    # add statistics to dictionary
    blockstats = {}
    blockstats['nblocks'] = nblocks
    blockstats['blockheights'] = blockheights
    blockstats['blockwidths'] = blockwidths
    blockstats['blocklengths'] = blocklengths
    blockstats['heightmax'] = heightmax
    blockstats['heightmean'] = heightmean
    blockstats['heightstd'] = heightstd
    blockstats['blockplans'] = blockplans
    blockstats['blockfronts'] = blockfronts
    # blockstats['blocksides'] = blocksides
    
    if a0 is not None:
        # building area density
        planindex = normed_sum(blockplans, a0)
        # building frontal aspect ratio
        frontindex = normed_sum(blockfronts, a0)
        # add statistics to dictionary
        blockstats['planindex'] = planindex
        blockstats['frontindex'] = frontindex        
    
    for key, val in blockstats.items():
        # convert numpy types to generic python types
        if isinstance(val, np.float32):
            val = val.item()
        # round values to precision
        if isinstance(val, float):
            blockstats[key] = round(val, precision)
    
    return blockstats


def blockshift(blocks, limits, xshift, yshift):
    # shift the whole block layout
    
    xmin = limits[0]
    xmax = limits[1]
    ymin = limits[2]
    ymax = limits[3]

    shiftblocks = []
    for block in blocks:
        newx = [(b - xshift) % xmax for b in block[0:2]]
        newy = [(a - yshift) % ymax for a in block[2:4]]
        z = block[4:6]
        shiftblocks.append(newx + newy + z)

    # split up blocks that go over boundaries
    tmpblocks = []
    for block in shiftblocks:
        # if imax < imin
        if block[1] <= block[0]:
            # create new block coordinates
            x1 = [block[0], xmax]
            x2 = [xmin, block[1]]
            y = block[2:4]
            z = block[4:6]
            newblock1 = x1 + y + z
            newblock2 = x2 + y + z
            tmpblocks.extend([newblock1, newblock2])
        else:
            tmpblocks.extend([block])

    newblocks = []
    for block in tmpblocks:
        # if jmax < jmin
        if block[3] <= block[2]:
            # create new block coordinates
            x = block[0:2]
            y1 = [block[2], ymax]
            y2 = [ymin, block[3]]
            z = block[4:6]
            newblock3 = x + y1 + z
            newblock4 = x + y2 + z
            newblocks.extend([newblock3, newblock4])
        else:
            newblocks.extend([block])

    return newblocks


def convert(blocks, dx, dy, dz, rounding=True):
    """Changes the resolution of a given block list. 
    If rounding=True, it returns the list rounded to the nearest integer.
    Block entries stored as block = [xmin, xmax, ymin, ymax, zmin, zmax]"""

    resolution = np.array([dx, dx, dy, dy, dz, dz])
    newblocks = blocks * resolution
    newblocks = newblocks.tolist()
    if rounding is True:  # rounds new blocks to integers!
        newblocks = [[round(x) for x in block] for block in newblocks]

    return newblocks


def write(blocks, filename):

    for block in blocks:
        # Checks that blocks are the right length. 
        # If you have only one block, store as blocks = [[block]].
        if len(block) == 6:
            pass
        else:
            raise IndexError("Blocks not the right length.")

    file = open(filename, 'w')
    file.write("{:12}".format('# Block location') + '\n')
    file.write("{:100}".format('#  il  iu  jl  ju  kl  ku') + '\n')

    for block in blocks:
        for val in block[0:6]:
            file.write('{:<3.0f} '.format(val))
        file.write('\n')

    file.close()
