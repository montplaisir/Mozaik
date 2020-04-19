
#Divide in 8 colors: mean of r < 128, mean of r >= 128, idem for g and b.
# This will be probably grayish, but it's a start.

class Palette8:
	def __init__(self, picref):
		self._width = picref.size[0]
		self._height = picref.size[1]
		self._picref = picref
		self._pixref = picref.load()
		
	def getWidth(self):
		return self._width

	def getHeight(self):
		return self._height
		
	def computePalette(self):
		picnew = self._picref
		meanr1 = 0
		meanr2 = 0
		meang1 = 0
		meang2 = 0
		meanb1 = 0
		meanb2 = 0
		nr1 = 0
		nr2 = 0
		ng1 = 0
		ng2 = 0
		nb1 = 0
		nb2 = 0
		for i in range(self._width):
			for j in range(self._height):
				(r,g,b) = self._pixref[i,j]
				if (r < 128):
					meanr1 += r
					nr1 += 1
				else:
					meanr2 += r
					nr2 += 1
				if (g < 128):
					meang1 += g
					ng1 += 1
				else:
					meang2 += g
					ng2 += 1
				if (b < 128):
					meanb1 += b
					nb1 += 1
				else:
					meanb2 += b
					nb2 += 1
		if (nr1 > 0):
			meanr1 = int(meanr1/nr1)
		if (ng1 > 0):
			meang1 = int(meang1/ng1)
		if (nb1 > 0):
			meanb1 = int(meanb1/nb1)
		if (nr2 > 0):
			meanr2 = int(meanr2/nr2)
		if (ng2 > 0):
			meang2 = int(meang2/ng2)
		if (nb2 > 0):
			meanb2 = int(meanb2/nb2)
		
		for i in range(self._width):
			for j in range(self._height):
				(r,g,b) = self._pixref[i,j]
				(rnew, gnew, bnew) = (r,g,b)
				if (r < 128):
					rnew = meanr1
				else:
					rnew = meanr2
				if (g < 128):
					gnew = meang1
				else:
					gnew = meang2
				if (b < 128):
					bnew = meanb1
				else:
					bnew = meang2
				pixnewij = (rnew, gnew, bnew)
				picnew.putpixel((i,j),pixnewij)
				
		return picnew


### Palette8 on whole image given by picref. ###
def palette8(picref):
	pal8 = Palette8(picref)
	return pal8.computePalette()
	

