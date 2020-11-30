from math import sqrt, radians, degrees

def distance(x, y):
    a = (x[1] - x[0])**2
    b = (y[1] - y[0])**2
    c = sqrt(a+b)
    return c

def convert(x):

    if x < 0:
        num = 360 + x
    elif x > 360:
        num = x - 360
    else:
        num = x

    return num
