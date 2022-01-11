
# Color utility functions

def colorDistance(color1, color2):
    return max(abs(color1[0]-color2[0]), abs(color1[1]-color2[1]), abs(color1[2]-color2[2]))


def isNeighbouringColor(color1, color2, threshold):
    return colorDistance(color1,color2) <= threshold


