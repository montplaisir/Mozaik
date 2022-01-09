
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


    def computePixels(self, mostFrequentColor):
        mfcr = mostFrequentColor[0]
        mfcg = mostFrequentColor[1]
        mfcb = mostFrequentColor[2]
        colorThreshold = 20

        for i in range(self._width):
            for j in range(self._height):
                (r,g,b) = self._pixref[i,j]
                if abs(r-mfcr) <= colorThreshold and abs(g-mfcg) <= colorThreshold and abs(b-mfcb) <= colorThreshold:
                    if self._pixnew[i][j] is None:
                        self._pixnew[i][j] = mostFrequentColor


    def paintPixels(self):
        for i in range(self._width):
            for j in range(self._height):
                if self._pixnew[i][j]:
                    (r,g,b) = self._pixnew[i][j]
                else:
                    (r,g,b) = (0,0,0)
                pixnewij = (r, g, b)
                self._picnew.putpixel((i,j),pixnewij)

        
    def computePalette(self):
        self._picnew = self._picref
        numColored = 0

        self.computeStats()

        mostFrequentColor = self.getMostFrequentColor()

        self.computePixels(mostFrequentColor)

        self.paintPixels()


        '''
        for color in allcolors:
            if (self._stats[color] > 1):
                print(color, self._stats[color])
        '''
        

        '''
        for i in range(self._width):
            for j in range(self._height):
                (r,g,b) = self._pixref[i,j]
        
        for i in range(self._width):
            for j in range(self._height):
                (r,g,b) = self._pixref[i,j]
                (rnew, gnew, bnew) = (r,g,b)
                pixnewij = (rnew, gnew, bnew)
                picnew.putpixel((i,j),pixnewij)
        '''
                
        return self._picnew


### BrightColors on whole image given by picref. ###
def apply(picref):
    bc = BrightColors(picref)
    return bc.computePalette()
    

