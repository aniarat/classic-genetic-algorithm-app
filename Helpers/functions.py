import math

import numpy as np


def rastrigin(x, y):
    a = 5
    return a + (x ** 2 - a * np.cos(2 * math.pi * x))+(y ** 2 - a * np.cos(2 * math.pi * y))
def schwefel(x):
    N = 5
    return 418.9829
