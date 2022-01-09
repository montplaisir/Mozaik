
import sys

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

        # Parameters - Undocumented
        self._colorThreshold = 30
        self._numColorMax = 8
        self._pctCoverage = 95
        if len(sys.argv) > 3:
            self._colorThreshold = int(sys.argv[3])
        if len(sys.argv) > 4:
            self._numColorMax = int(sys.argv[4])
        if len(sys.argv) > 5:
            self._pctCoverage = int(sys.argv[5])
        
        

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


    def colorDistance(self, color1, color2):
        return max(abs(color1[0]-color2[0]), abs(color1[1]-color2[1]), abs(color1[2]-color2[2]))


    def isNeighbouringColor(self, color1, color2):
        return self.colorDistance(color1,color2) <= self._colorThreshold


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
                    print("warning: missing pixel in",i,",",j)
                pixnewij = (r, g, b)
                self._picnew.putpixel((i,j),pixnewij)


    def clearStats(self, mostFrequentColor):
        newStats = {}
        for color in self._stats.keys():
            if not self.isNeighbouringColor(color, mostFrequentColor):
                newStats[color] = self._stats[color]
        self._stats = newStats


    def computeRemainingPixels(self, checkIsSet):
        numPixelColor = 0
        for i in range(self._width):
            for j in range(self._height):
                refcolor = self._pixref[i,j]
                if not self._pixnew[i][j]:
                    minDist = 1000
                    if i > 0:
                        ii = i-1
                        jj = j
                        dist = self.colorDistance(self._pixref[ii,jj], refcolor)
                        if dist < minDist:
                            minDist = dist
                            if not checkIsSet or self._pixnew[ii][jj]:
                                self._pixnew[i][j] = self._pixnew[ii][jj]
                    if j > 0:
                        ii = i
                        jj = j-1
                        dist = self.colorDistance(self._pixref[ii,jj], refcolor)
                        if dist < minDist:
                            minDist = dist
                            if not checkIsSet or self._pixnew[ii][jj]:
                                self._pixnew[i][j] = self._pixnew[ii][jj]
                    if i < self._width-1:
                        ii = i+1
                        jj = j
                        dist = self.colorDistance(self._pixref[ii,jj], refcolor)
                        if dist < minDist:
                            minDist = dist
                            if not checkIsSet or self._pixnew[ii][jj]:
                                self._pixnew[i][j] = self._pixnew[ii][jj]
                    if j < self._height-1:
                        ii = i
                        jj = j+1
                        dist = self.colorDistance(self._pixref[ii,jj], refcolor)
                        if dist < minDist:
                            minDist = dist
                            if not checkIsSet or self._pixnew[ii][jj]:
                                self._pixnew[i][j] = self._pixnew[ii][jj]

                    if self._pixnew[i][j]:
                        numPixelColor += 1

        return numPixelColor


        
    def computePalette(self):
        numPixelColored = 0
        numColors = 0
        totalPixel = self._width * self._height
        pctCovered = 0.0

        print("compute palette using values:")
        print("    threshold:",self._colorThreshold)
        print("    max number of color:",self._numColorMax)
        print("    percentage of coverage before computing remaining pixels:",self._pctCoverage)

        self.computeStats()
        
        while pctCovered < self._pctCoverage and numColors < self._numColorMax:
            mostFrequentColor = self.getMostFrequentColor()
            print("computing pixels with color:",mostFrequentColor)
            numPixelColored += self.computePixels(mostFrequentColor)
            self.clearStats(mostFrequentColor)
            pctCovered = numPixelColored * 100.0 / totalPixel
            numColors += 1

        numNewPixels = 1
        while numPixelColored < totalPixel:
            checkIfColorSet = (numNewPixels == 0)
            numNewPixels = self.computeRemainingPixels(checkIfColorSet)
            if checkIfColorSet:
                print("last pass...")
            else:
                print("computing remaining pixels...")
            numPixelColored += numNewPixels

        self.paintPixels()

        return self._picnew


### BrightColors on whole image given by picref. ###
def apply(picref):
    bc = BrightColors(picref)
    return bc.computePalette()
    

