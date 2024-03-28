import math

import numpy as np


def rastrigin(x):
    a = 10
    return a + (x ** 2 - a * np.cos(2 * math.pi * x))
