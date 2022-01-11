
import sys

# Copied from brightcolors
# In addition, take into account contour detection, and aim for saturated colors.

class Saturation:
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
        

    def computeSaturation(self, color):
        maxrgb = max(color[0], color[1], color[2]);
        minrgb = min(color[0], color[1], color[2]);
        if minrgb == maxrgb:
            return 0;
        return (maxrgb-minrgb) / (1 - abs((maxrgb-minrgb)/255-1))


    def computeHue(self, color):
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


    def computeStats(self):
        self._stats.clear()
        for i in range(self._width):
            for j in range(self._height):
                color = self._pixref[i,j]
                if color in self._stats:
                    self._stats[color] += 1
                else:
                    self._stats[color] = 1


    def getMostFrequentColorSat(self):
        allcolors = self._stats.keys()
        frequency = 0
        for color in allcolors:
            if self._stats[color] > frequency:
                mostFrequentColor = color
                frequency = self._stats[color]

        # Test 2
        # Saturate the given color within threshold limits, without regards to the available colors
        # This is done by adding the threshold to the max rgb, and substracting it from the min rgb,
        # within limits.
        # To ensure the hue remains the same, we also augment the middle value.
        (r,g,b) = mostFrequentColor
        maxrgb = max(r, g, b);
        minrgb = min(r, g, b);
        if (r == minrgb and g == maxrgb) or (g == minrgb and r == maxrgb):
            midrgb = b
        elif (r == minrgb and b == maxrgb) or (b == minrgb and r == maxrgb):
            midrgb = g
        elif (g == minrgb and b == maxrgb) or (b == minrgb and g == maxrgb):
            midrgb = r
        else:
            print("Error: Could not compute midrgb for color",mostFrequentColor)

        # Compute amount that we can use for saturation adjustment
        amount = self._colorThreshold
        if 255-maxrgb < amount:
            amount = 255-maxrgb
        if minrgb < amount:
            amount = minrgb
        if minrgb == maxrgb: #greyscale, saturation = 0
            amount = 0
            midamount = 0
        else:
            midamount = int((2*midrgb-minrgb-maxrgb)*amount / (maxrgb-minrgb))

        if minrgb == maxrgb:
            # Make pale greys whiter, dark greys blacker
            if minrgb <= 127:
                amount = min(int(minrgb/2),self._colorThreshold)
                r -= amount
                g -= amount
                b -= amount
            else:
                amount = min(int((255-minrgb)/2),self._colorThreshold)
                r += amount
                g += amount
                b += amount
        elif r == minrgb and g == maxrgb:
            r -= amount
            g += amount
            b += midamount
        elif r == minrgb and b == maxrgb:
            r -= amount
            b += amount
            g += midamount
        elif g == minrgb and r == maxrgb:
            g -= amount
            r += amount
            b += midamount
        elif g == minrgb and b == maxrgb:
            g -= amount
            b += amount
            r += midamount
        elif b == minrgb and r == maxrgb:
            b -= amount
            r += amount
            g += midamount
        elif b == minrgb and g == maxrgb:
            b -= amount
            g += amount
            r += midamount

        mostFrequentColorSat = (r,g,b)
        if not self.isNeighbouringColor(mostFrequentColor,mostFrequentColorSat):
            print("Error:",mostFrequentColor,"and",mostFrequentColorSat,"are not neighbouring colors")


        '''
        # Test 1
        # look at all available colors in the neighbourhood and use the most saturated one.
        currentSaturation = self.computeSaturation(mostFrequentColor)
        for color in allcolors:
            if self.colorDistance(color, mostFrequentColor) < self._colorThreshold:
                newSaturation = self.computeSaturation(color)
                if (newSaturation > currentSaturation):
                    print("using",color,"instead of",mostFrequentColor)
                    currentSaturation = newSaturation
                    mostFrequentColor = color
        '''


        return (mostFrequentColor,mostFrequentColorSat)


    def colorDistance(self, color1, color2):
        return max(abs(color1[0]-color2[0]), abs(color1[1]-color2[1]), abs(color1[2]-color2[2]))


    def isNeighbouringColor(self, color1, color2):
        return self.colorDistance(color1,color2) <= self._colorThreshold


    def computePixels(self, mostFrequentColor, mostFrequentColorSat):
        numPixelColored = 0
        for i in range(self._width):
            for j in range(self._height):
                color = self._pixref[i,j]
                if self.isNeighbouringColor(mostFrequentColor, color):
                    if self._pixnew[i][j] is None:
                        self._pixnew[i][j] = mostFrequentColorSat
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
            (mostFrequentColor,mostFrequentColorSat) = self.getMostFrequentColorSat()
            print("computing pixels with color:",mostFrequentColor)
            numPixelColored += self.computePixels(mostFrequentColor,mostFrequentColorSat)
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


### Saturation on whole image given by picref. ###
def apply(picref):
    sat = Saturation(picref)
    return sat.computePalette()
    

