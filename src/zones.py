
import sys
import hsl
import random
import colorutils as ut
import blur

# New, improved from saturation. Globally similar.

class Zones:
    def __init__(self, picref):
        self._width = picref.size[0]
        self._height = picref.size[1]
        self._picref = picref
        self._pixref = picref.load()
        self._picnew = picref
        self._stats = {}
        self._greyscale = [[0 for j in range(self._height)] for i in range(self._width)]
        self._contour   = [[0 for j in range(self._height)] for i in range(self._width)]
        self._pixnew    = [[None for j in range(self._height)] for i in range(self._width)]
        self._palette   = []

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
        
        

    def computeStats(self):
        self._stats.clear()
        for i in range(self._width):
            for j in range(self._height):
                color = self._pixref[i,j]
                if color in self._stats:
                    self._stats[color] += 1
                else:
                    self._stats[color] = 1


    def computeGreyscale(self):
        for i in range(self._width):
            for j in range(self._height):
                self._greyscale[i][j] = hsl.computeGreyscale(self._pixref[i,j])


    def computeContours(self):
        self.computeGreyscale()
        for i in range(self._width):
            for j in range(self._height):
                if i > 0 and j > 0 and i < self._width-1 and j < self._height-1:
                    c1 = 0 -self._greyscale[i-1][j-1] -2*self._greyscale[i-1][j] -self._greyscale[i-1][j+1];
                    c2 =    self._greyscale[i+1][j-1] +2*self._greyscale[i+1][j] +self._greyscale[i+1][j+1];
                    c3 = 0 -self._greyscale[i-1][j-1] -2*self._greyscale[i][j-1] -self._greyscale[i+1][j-1];
                    c4 =    self._greyscale[i-1][j+1] +2*self._greyscale[i][j+1] +self._greyscale[i+1][j+1];
                    self._contour[i][j] = abs((c1 + c2 + c3 + c4) / 16)


    def getMostFrequentColorSat(self, kickGreys, usePicColors):
        allcolors = self._stats.keys()
        frequency = 0
        for color in allcolors:
            if self._stats[color] > frequency:
                mostFrequentColor = color
                frequency = self._stats[color]
        if usePicColors:
            mostFrequentColorSat = self.getMostSaturatedColorAround(mostFrequentColor)
        else:
            mostFrequentColorSat = self.saturateColor(mostFrequentColor, kickGreys)

        return (mostFrequentColor,mostFrequentColorSat)


    def getMostSaturatedColorAround(self, mostFrequentColor):
        mostFrequentColorSat = mostFrequentColor 
        currentSat = hsl.computeSaturation(mostFrequentColorSat)
        allcolors = self._stats.keys()
        
        for color in allcolors:
            if ut.isNeighbouringColor(mostFrequentColor, color, self._colorThreshold):
                colorSat = hsl.computeSaturation(color)
                if colorSat > currentSat:
                    mostFrequentColorSat = color
                    currentSat = colorSat

        return mostFrequentColorSat
                    

    def saturateColor(self, color, kickGreys):
        # Saturate the given color within threshold limits, without regards to the available colors
        # This is done by adding the threshold to the max rgb, and substracting it from the min rgb,
        # within limits.
        # To ensure the hue remains the same, we also augment the middle value.
        (r,g,b) = color
        maxrgb = max(r, g, b);
        minrgb = min(r, g, b);
        if (r == minrgb and g == maxrgb) or (g == minrgb and r == maxrgb):
            midrgb = b
        elif (r == minrgb and b == maxrgb) or (b == minrgb and r == maxrgb):
            midrgb = g
        elif (g == minrgb and b == maxrgb) or (b == minrgb and g == maxrgb):
            midrgb = r
        else:
            print("Error: Could not compute midrgb for color",color)

        # Compute amount that we can use for saturation adjustment
        amount = self._colorThreshold
        if 255-maxrgb < amount:
            amount = 255-maxrgb
        if minrgb < amount:
            amount = minrgb
        if minrgb < maxrgb:
            midamount = int((2*midrgb-minrgb-maxrgb)*amount / (maxrgb-minrgb))

        if maxrgb - minrgb <= 10: #Grey - greyish
            (r,g,b) = self.computeKickedGrey(minrgb, maxrgb, color, kickGreys)
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

        colorSat = (r,g,b)
        if not ut.isNeighbouringColor(color,colorSat, self._colorThreshold):
            print("Error:",color,"and",colorSat,"are not neighbouring colors")

        return colorSat


    def computeKickedGrey(self, minrgb, maxrgb, color, kickGreys):
        (r,g,b) = color
        # Make pale greys whiter, dark greys blacker
        # When kicking greys, Medium grey get a color chosen arbitrarly. Otherwise they remain grey.
        if minrgb <= 2*self._colorThreshold:
            amount = min(int(minrgb/2),self._colorThreshold)
            r -= amount
            g -= amount
            b -= amount
        elif maxrgb + 2*self._colorThreshold >= 255:
            amount = min(int((255-maxrgb)/2),self._colorThreshold)
            r += amount
            g += amount
            b += amount
        elif kickGreys:
            amount = self._colorThreshold
            halfamount = int(amount/2)  #ensures to keep same luminosity
            randrgb = random.randrange(3)
            if randrgb == 0:
                r += amount
                g -= halfamount
                b -= halfamount
            elif randrgb == 1:
                r -= halfamount
                g += amount
                b -= halfamount
            elif randrgb == 2:
                r -= halfamount
                g -= halfamount
                b += amount
        return (r,g,b)


    def computePixels(self, mostFrequentColor, mostFrequentColorSat):
        numPixelColored = 0
        for i in range(self._width):
            for j in range(self._height):
                if self._pixnew[i][j] is None:
                    color = self._pixref[i,j]
                    if ut.isNeighbouringColor(mostFrequentColor, color, self._colorThreshold):
                        self._pixnew[i][j] = mostFrequentColorSat
                        numPixelColored += 1

        return numPixelColored


    def applyBlur(self):
        self._blur = blur.blur(self._picref)
        self._pixref = self._blur.load()    # Override

        
    def paintPixels(self):
        for i in range(self._width):
            for j in range(self._height):
                if self._pixnew[i][j]:
                    (r,g,b) = self._pixnew[i][j]
                else:
                    (r,g,b) = (0,0,0)
                    #print("warning: missing pixel in",i,",",j)
                pixnewij = (r, g, b)
                self._picnew.putpixel((i,j),pixnewij)


    def clearStats(self, mostFrequentColor):
        newStats = {}
        for color in self._stats.keys():
            if not ut.isNeighbouringColor(color, mostFrequentColor, self._colorThreshold):
                newStats[color] = self._stats[color]
        self._stats = newStats


    def computeRemainingPixels(self):
        numPixelColor = 0
        for i in range(self._width):
            for j in range(self._height):
                numPixelColor += self.computePixel(i, j)

        return numPixelColor


    def computePixel(self, i, j):
        if self._pixnew[i][j]:
            return 0

        minDist = 1000
        refcolor = self._pixref[i,j]
        for paletteColor in self._palette:
            dist = ut.colorDistance(refcolor, paletteColor)
            if dist < minDist:
                minDist = dist
                self._pixnew[i][j] = paletteColor

        return 1


    def computePalette(self, kickGreys, usePicColors):
        numPixelColored = 0
        numColors = 0
        totalPixel = self._width * self._height
        pctCovered = 0.0

        print("compute palette using values:")
        print("    threshold:",self._colorThreshold)
        print("    max number of color:",self._numColorMax)
        print("    percentage of coverage before computing remaining pixels:",self._pctCoverage)

        print("computing color stats...")
        self.computeStats()
        
        while pctCovered < self._pctCoverage and numColors < self._numColorMax:
            (mostFrequentColor,mostFrequentColorSat) = self.getMostFrequentColorSat(kickGreys, usePicColors)
            self._palette.append(mostFrequentColor)
            print("computing pixels with color:",mostFrequentColorSat)
            numPixelColored += self.computePixels(mostFrequentColor,mostFrequentColorSat)
            self.clearStats(mostFrequentColor)
            pctCovered = numPixelColored * 100.0 / totalPixel
            print(pctCovered,"% computed...")
            numColors += 1

        print(numColors,"colors used")
        print("computing remaining pixels...")
        self.computeRemainingPixels()

        self.paintPixels()

        return self._picnew


### Apply on whole image given by picref. ###
def apply(picref, kickGreys, usePicColors):
    image = Zones(picref)
    return image.computePalette(kickGreys, usePicColors)
    

