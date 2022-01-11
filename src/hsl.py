
def computeSaturation(color):
    maxrgb = max(color[0], color[1], color[2]);
    minrgb = min(color[0], color[1], color[2]);
    if minrgb == maxrgb:
        return 0;
    return (maxrgb-minrgb) / (1 - abs((maxrgb-minrgb)/255-1))


def computeHue(color):
    (r,g,b) = color
    minrgb = min(r,g,b)
    maxrgb = max(r,g,b)
    if minrgb == maxrgb:
        return 0

    if (r == minrgb and g == maxrgb) or (g == minrgb and r == maxrgb):
        midrgb = b
    elif (r == minrgb and b == maxrgb) or (b == minrgb and r == maxrgb):
        midrgb = g
    elif (g == minrgb and b == maxrgb) or (b == minrgb and g == maxrgb):
        midrgb = r
    else:
        printf("Error in computeHue with",color)

    return (midrgb - minrgb) / (maxrgb - minrgb)


def computeGreyscale(color):
    (r,g,b) = color
    grey = int((r+g+b)/3)
    return grey

