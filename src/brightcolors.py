
# Compute stats on the pixel colors.
# Take the most frequent color. Use this color for all pixels of neighbouring colors (within threshold).
# Continue with the next color, greedily, until all pixels in new image are colored.

class BrightColors:
    def __init__(self, picref):
        self._width = picref.size[0]
        self._height = picref.size[1]
        self._picref = picref
        self._pixref = picref.load()
        self._picnew = picref
        self._stats = {}
        self._pixnew = [[None for j in range(self._height)] for i in range(self._width)]

        # Parameters
        self._colorThreshold = 30
        self._numColorMax = 10
        self._pctCoverage = 95
        

    def getWidth(self):
        return self._width


    def getHeight(self):
        return self._height
        

    def computeStats(self):
        self._stats.clear()
        for i in range(self._width):
            for j in range(self._height):
                color = self._pixref[i,j]
                if color in self._stats:
                    self._stats[color] += 1
                else:
                    self._stats[color] = 1


    def getMostFrequentColor(self):
        allcolors = self._stats.keys()
        frequency = 0
        for color in allcolors:
            if self._stats[color] > frequency:
                mostFrequentColor = color
                frequency = self._stats[color]

        return mostFrequentColor


    def isNeighbouringColor(self, color1, color2):
        return abs(color1[0]-color2[0]) <= self._colorThreshold and abs(color1[1]-color2[1]) <= self._colorThreshold and abs(color1[2]-color2[2]) <= self._colorThreshold

    def computePixels(self, mostFrequentColor):
        numPixelColored = 0
        for i in range(self._width):
            for j in range(self._height):
                color = self._pixref[i,j]
                if self.isNeighbouringColor(mostFrequentColor, color):
                    if self._pixnew[i][j] is None:
                        self._pixnew[i][j] = mostFrequentColor
                        numPixelColored += 1

        return numPixelColored


    def paintPixels(self):
        for i in range(self._width):
            for j in range(self._height):
                if self._pixnew[i][j]:
                    (r,g,b) = self._pixnew[i][j]
                else:
                    (r,g,b) = (0,0,0)
                pixnewij = (r, g, b)
                self._picnew.putpixel((i,j),pixnewij)


    def clearStats(self, mostFrequentColor):
        newStats = {}
        for color in self._stats.keys():
            if not self.isNeighbouringColor(color, mostFrequentColor):
                newStats[color] = self._stats[color]
        self._stats = newStats
        
    def computePalette(self):
        numPixelColored = 0
        numColors = 0
        totalPixel = self._width * self._height
        pctCovered = 0.0

        self.computeStats()
        
        while pctCovered < self._pctCoverage and numColors < self._numColorMax:
            mostFrequentColor = self.getMostFrequentColor()
            print(mostFrequentColor)
            numPixelColored += self.computePixels(mostFrequentColor)
            self.clearStats(mostFrequentColor)
            print(numPixelColored)
            pctCovered = numPixelColored * 100.0 / totalPixel
            numColors += 1

        self.paintPixels()

        return self._picnew


### BrightColors on whole image given by picref. ###
def apply(picref):
    bc = BrightColors(picref)
    return bc.computePalette()
    

