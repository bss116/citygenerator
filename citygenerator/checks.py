import numpy as np
import operator
import citygenerator as cgen


def heightratios(blocks, domainheight):
    """Function that calculates building height to domain height ratio. 
    General advice: domain height/building height >= 6."""
    ratios = []
    for block in blocks:
        xy = [b for b in block[0:4]]
        z = block[5]
        if z > 0:
            ratio = domainheight/z
        else:
            ratio = 0
        ratios.append(ratio)

    return ratios


def blockvolumes(blocks):
    """Function that calculates the cube roots of the block volume."""
    roots = []
    for block in blocks:
        volume = (block[1] - block[0])*(block[3] - block[2])*(block[5] - block[4])
        cuberoot = np.cbrt(volume)
        roots.append(cuberoot)
        
    return roots


def canyonwidths(fullcanyons):
    """Function that calculates the canyon widths."""
    xwidths = []
    ywidths = []
    for canyon in fullcanyons:
        width1 = (canyon[1] - canyon[0])
        width2 = (canyon[3] - canyon[2])
        xwidths.append(width1)
        ywidths.append(width2)
    
    return xwidths, ywidths


def check_heightratio(dimblocks, domainheight, heightratio=6):
    # blocks and limits are dimensionalised
    problemblocks = []
    # check for domain height zsize over block height zmax ratio:
    ratios = heightratios(dimblocks, domainheight)
    
    for r, block in zip(ratios, dimblocks):
        if r < heightratio:
            problemblocks.append(block)
            print("Smaller height ratio zsize/zmax = ", r, "with block ", block, ".")
            
    return problemblocks


def check_blockvolume(blocks, blockvolume=10):
    # blocks are in cells, not dimensionalised
    problemblocks = []
    # check for block volume:
    roots = blockvolumes(blocks)
    for r, block in zip(roots, blocks):
        if r < blockvolume:
            problemblocks.append(block)
            print("Smaller block volume with cube root = ", r, "for block ", block, ".")
            
    return problemblocks


def check_canyonwidths(blocks, limits, canyonwidth=5):
    # blocks are dimensionalised, therefore we should set higher width
    problemcanyons = []
    # get canyons
    canyons, fullcanyons = cgen.canyons.getcanyons(blocks, limits)
    # get canyon widths
    xwidths, ywidths = canyonwidths(fullcanyons)

    # get canyon shift
    initblocks = sorted(blocks, key=operator.itemgetter(2,0))
    xshift = initblocks[0][0]  # first block xmin
    yshift = initblocks[0][2]  # first block ymin
    
    # check canyon widths
    for xwid, ywid, fullcanyon in zip(xwidths, ywidths, fullcanyons):
        if xwid < canyonwidth or ywid < canyonwidth:
            # shift back
            canyon = cgen.utils.blockshift([fullcanyon], limits, -xshift, -yshift)
            problemcanyons.extend(canyon)
            print("Smaller canyon width with widths = ", xwid, "and", ywid, "for canyon ", canyon, ".")

    return problemcanyons


def allchecks(blocks, limits, resolution, heightratio=6, blockvolume=10, canyonwidth=5):
        
    problemblocks = []
    problemcanyons = []

    try:
        probblocks1 = check_heightratio(blocks, limits[5], heightratio)
        problemblocks.extend(probblocks1)
    except Exception:
        print("Could not check block to domain height ratio.")
        pass
        
    try:
        # block volume requirement in cells, need to scale from dimensional blocks
        # resolution = [dx, dy, dz]
        dimfactor = resolution[0]*resolution[1]*resolution[2]
        probblocks2 = check_blockvolume(blocks, blockvolume*dimfactor)
        problemblocks.extend(probblocks2)
    except Exception:
        print("Could not check block volume.")
        pass
        
#     try:
#         # CANYONS WILL NOT ALWAYS BE WELL DEFINED
#         probcanyons = check_canyonwidths(blocks, limits[:4], canyonwidth)
#         problemcanyons.extend(probcanyons)
#     except Exception:
#         print("Could not check canyon widths.")
#         pass  
            
    print("Checks completed.")
    
    return problemblocks, problemcanyons
    