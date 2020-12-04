import scipy.stats as ss
import numpy as np


def normal_int(n):
    x = np.arange(-n, n+1)
    xU, xL = x + 0.5, x - 0.5
    prob = ss.norm.cdf(xU, scale=n/3) - ss.norm.cdf(xL, scale=n/3)
    prob = prob / prob.sum()
    nums = np.random.choice(x, size=1, p=prob)
    return nums[0]
