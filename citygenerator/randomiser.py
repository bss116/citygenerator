import random
import math
import numpy as np


def density_function(interval, default, randomness=0.):
    """Defines a probablity density function of a given interval.
    The probability of the default value is (1 - r), and probability of a uniformly
    distributed value from the interval is r.
    pdf = (1 - r) * default + r * u(interval).
    :param interval: given set of points
    :param default: value with probability 1 - r.
    :param randomness: degree of randomisation, 0 <= randomness <= 1."""    

    if 0. <= randomness <= 1.:
        p = int(randomness * 100)
        q = int((1 - randomness) * 100)
        plist = [random.choice(interval) for _ in range(p)]
        qlist = [default] * q
        randomlist = plist + qlist
    else:
        raise ValueError("Degree of randomness must be between 0 and 1.")

    return randomlist


def midpoint(interval):
    """Function that returns the mid point of an interval.
    :param interval: given set of points"""

    nvalues = len(interval)
    mid = interval[math.floor(nvalues/2)]  # returns lower value in case of odd number of values
    
    return mid


def lowpoint(interval):
    """Function that returns the lowest value of an interval.
    :param interval: given set of points"""
    
    lowest = interval[0]
    
    return lowest


def draw_from_interval(interval, randomness=0., weight='mid'):
    """Function that returns a random point from a given set. 
    :param interval: given set of points
    Optional parameter:
    :param randomness: degree of randomisation, 0 <= randomness <= 1.
        Default is randomness = 0.
    :param weight: value that is returned with probabilty (1 - r).
        Options are: 'mid', 'low'.
        Default is 'mid'.
    For example if randomness = 0.4, then the probability of a random point is 0.4, 
    the probability of the weight point is 0.6."""
    
    if weight in ['mid', 'm', 'centre']:
        default = midpoint(interval)
    elif weight in ['low', 'l', 'min']:
        default = lowpoint(interval)
    else:
        raise ValueError("The weight point of interval could not be found."
                         "Options for order are: 'mid', 'low'.")
        
    randomlist = density_function(interval, default, randomness)
    randomnumber = random.choice(randomlist)

    return randomnumber    


def mid(interval, randomness=0.):
    """Function that returns a random point from a given set. 
    If randomness is zero, it returns the midpoint point of set.
    :param interval: given set of points
    Optional parameter:
    :param randomness: degree of randomisation, 0 <= randomness <= 1. 
    For example if degree = 0.4, then the probability of a random point is 0.4, 
    the probability of the midpoint is 0.6.
    Default is randomness = 0."""
    
    default = midpoint(interval)
    randomlist = density_function(interval, default, randomness)
    randomnumber = random.choice(randomlist)

    return randomnumber


def low(interval, randomness=0.):    
    """Function that returns a random point from a given set. 
    If randomness is zero, it returns the lowest point of the set.
    :param interval: given set
    Optional parameter:
    :param randomness: degree of randomisation, 0 <= degree <= 1. 
    For example if degree = 0.4, then the probability of a random point is 0.4, 
    the probability of the lowest point is 0.6.
    Default is randomness = 1."""
    
    default = lowpoint(interval)
    randomlist = density_function(interval, default, randomness)
    randomnumber = random.choice(randomlist)

    return randomnumber
