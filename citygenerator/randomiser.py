import random
import math
import numpy as np


def mid(interval, randomness=0.):
    """Function that returns a random point from a given set. 
    If randomness is zero, it returns the midpoint point of set.
    :param interval: given set of points
    Optional parameter:
    :param randomness: degree of randomisation, 0 <= randomness <= 1. 
    For example if degree = 0.4, then the probability of a random point is 0.4, 
    the probability of the midpoint is 0.6.
    Default is randomness = 0."""
    
    nvalues = len(interval)
    midpoint = interval[math.floor(nvalues/2)]  # returns lower value in case of odd number of values
    
    if 0. <= randomness <= 1.:
        p = int(randomness * 100)
        q = int((1 - randomness) * 100)
        randomlist = [random.choice(interval) for _ in range(p)]
        intlist = [midpoint] * q + randomlist
        randomnr = random.choice(intlist)
    else:
        raise ValueError("Degree of randomness must be between 0 and 1.")

    return randomnr


def low(interval, randomness=0.):    
    """Function that returns a random point from a given set. 
    If randomness is zero, it returns the lowest point of the set.
    :param interval: given set
    Optional parameter:
    :param randomness: degree of randomisation, 0 <= degree <= 1. 
    For example if degree = 0.4, then the probability of a random point is 0.4, 
    the probability of the lowest point is 0.6.
    Default is randomness = 1."""

    lowpoint = interval[0]

    if 0. <= randomness <= 1.:
        p = int(randomness * 100)
        q = int((1 - randomness) * 100)
        randomlist = [random.choice(interval) for _ in range(p)]
        intlist = [lowpoint] * q + randomlist
        randomnr = random.choice(intlist)
    else:
        raise ValueError("Degree of randomness must be between 0 and 1.")

    return randomnr
