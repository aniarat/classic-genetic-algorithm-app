import math

import numpy as np


def rastrigin(x):
    a = 5
    return a + (x ** 2 - a * np.cos(2 * math.pi * x))
