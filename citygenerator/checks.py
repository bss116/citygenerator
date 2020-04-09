import numpy as np


def get_heightratios(blocks, domainheight):
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


def get_blockvolumes(blocks):
    """Function that calculates the cube roots of the block volume."""
    roots = []
    for block in blocks:
        volume = (block[1] - block[0])*(block[3] - block[2])*(block[5] - block[4])
        cuberoot = np.cbrt(volume)
        roots.append(cuberoot)
        
    return roots


def check_heightratio(dimblocks, domainheight, heightratio=6):
    # blocks and limits are dimensionalised
    problemblocks = []
    # check for domain height zsize over block height zmax ratio:
    ratios = get_heightratios(dimblocks, domainheight)
    
    for r, block in zip(ratios, dimblocks):
        if r < heightratio:
            problemblocks.append(block)
            print("Smaller height ratio zsize/zmax = ", r, "with block ", block, ".")
            
    return problemblocks


def check_blockvolume(blocks, blockvolume=10):
    # blocks are in cells, not dimensionalised
    problemblocks = []
    # check for block volume:
    roots = get_blockvolumes(blocks)
    for r, block in zip(roots, blocks):
        if r < blockvolume:
            problemblocks.append(block)
            print("Smaller block volume with cube root = ", r, "for block ", block, ".")
            
    return problemblocks


def run_checks(blocks, limits, resolution, heightratio=6, blockvolume=10):
        
    problemblocks = []

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
        
    print("Checks completed.")
    
    return problemblocks
