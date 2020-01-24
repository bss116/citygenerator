from . import utils


def convert(blocks, target):
    """Function to convert target surface of blocks into green space."""

    greenspace = []

    if target is 0:
        return blocks, greenspace

    else:
        area = [utils.blockplan([b]) for b in blocks]

        agreen = 0
        n = len(blocks)

        # check if any of the blocks is the size of greenery
        i = 0
        while (i < n) and (agreen == 0):
            if target * 0.9 <= area[i] <= target * 1.1:
                agreen = area[i]
                greenspace.extend([blocks[i]])
                del blocks[i]
                print("One block transformed to green space")
            i += 1

        # check if any two of the blocks add up to the required size of greenery
        i = 0
        while (i < n) and (agreen == 0):
            for j in range(n):
                if target * 0.9 <= area[i] + area[j] <= target * 1.1:
                    if i is not j:
                        agreen = area[i] + area[j]
                        greenspace.extend([blocks[i], blocks[j]])
                        # trick to delete both indices: sort and delete higher first
                        indices = [i, j]
                        for index in sorted(indices, reverse=True):
                            del blocks[index]
                        print("Two blocks transformed to green space")
                        # get out of for loop
                        break
            i += 1

        # check if any three of the blocks add up to the required size of greenery
        i = 0
        while (i < n) and (agreen == 0):
            for j in range(n):
                if agreen == 0:
                    for k in range(n):
                        if target * 0.9 <= area[i] + area[j] + area[k] <= target * 1.1:
                            indices = [i, j, k]
                            indices.sort()
                            # test that the indices are all different by checking strict order
                            if indices[0] < indices[1] < indices[2]:
                                agreen = area[i] + area[j] + area[k]
                                greenspace.extend([blocks[i], blocks[j], blocks[k]])
                                # trick to delete both indices: sort and delete highest first
                                for index in sorted(indices, reverse=True):
                                    del blocks[index]
                                print("Three blocks transformed to green space")
                                # get out of inner for loop
                                break
                else:
                    # get out of outer for loop
                    break
            i += 1

        if i == n and agreen == 0:
            print("Could not find suitable blocks for green space")

        return blocks, greenspace
