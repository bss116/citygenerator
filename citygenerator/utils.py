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


def blockstats(dimblocks, a0=None):
    blockstatistics = {}
    precision = 2

    # number of blocks
    nblocks = len(dimblocks)
    blockstatistics['nblocks'] = nblocks

    # blocks plan area
    afinal = blockplan(dimblocks)
    blockstatistics['blocksarea'] = afinal

    # blocks frontal area
    hfinal = blockfront(dimblocks)
    blockstatistics['blocksarea_f'] = hfinal

    # blockheights
    blockheights = [b[5] for b in dimblocks]
    blockstatistics['blockheights'] = blockheights

    # block maximum zmax
    if blockheights:  # if not empty
        zmax = np.max(blockheights)
    else:
        zmax = 0
    blockstatistics['zmax'] = round(zmax, precision)

    # block average height unweighted
    if blockheights:
        zmean = np.mean(blockheights)
    else:
        zmean = 0
    blockstatistics['zmean'] = round(zmean, precision)

    # blockfronts
    blockfronts = [blockfront([f]) for f in dimblocks]
    blockstatistics['blockfronts'] = blockfronts

    # blockplans
    blockplans = [blockplan([p]) for p in dimblocks]
    blockstatistics['blockplans'] = blockplans

    # block weighted average height zh
    if hfinal > 0:
        # weights from blockfronts
        weights = [b/hfinal for b in blockfronts]
        weightedheights = [f * b for f, b in zip(weights, blockheights)]
        zh = np.sum(weightedheights)
    else: # sets weighted heights to zero in case of no blocks
        zh = 0
    blockstatistics['zh'] = round(zh, precision)

    # block weighted average height zh_alt weighted by block area
    # not block fronts
    if afinal > 0:
        # weights from blockplan areas
        weights2 = [b/afinal for b in blockplans]
        weightedheights2 = [f * b for f, b in zip(weights2, blockheights)]
        zh_alt = np.sum(weightedheights2)
    else: # sets weighted heights to zero in case of no blocks
        zh_alt = 0
    blockstatistics['zh_alt'] = round(zh_alt, precision)

    # if a0 defined
    try:
        # building area density
        lp = afinal / a0
        blockstatistics['lp'] = round(lp, precision)
        
        # building frontal aspect ratio
        lf = hfinal / a0
        blockstatistics['lf'] = round(lf, precision)
        
    except Exception:
        print("No a0 defined.")
        pass
        
    return blockstatistics


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
