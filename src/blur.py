
### Blur pixel: Make color a mean color of values of pixels up, down, left and right.

class Blurpix:
	def __init__(self, picref):
		self._width = picref.size[0]
		self._height = picref.size[1]
		self._pixref = picref.load()

		
	def getWidth(self):
		return self._width

		
	def getHeight(self):
		return self._height

		
	def blurpix(self, i, j):
		meanr = 0
		meang = 0
		meanb = 0
		nm = 0
		if i > 0:
			(r,g,b) = self._pixref[i-1,j]
			meanr += r
			meang += g
			meanb += b
			nm += 1
		if j > 0: 
			(r,g,b) = self._pixref[i,j-1]
			meanr += r
			meang += g
			meanb += b
			nm += 1
		if i < self._width-1:
			(r,g,b) = self._pixref[i+1,j]
			meanr += r
			meang += g
			meanb += b
			nm += 1
		if j < self._height-1:
			(r,g,b) = self._pixref[i,j+1]
			meanr += r
			meang += g
			meanb += b
			nm += 1
		pixnew = (int(meanr/nm), int(meang/nm), int(meanb/nm))

		return pixnew
	

### Blur whole image given by picnew. ###
def blur(picref):
	picnew = picref
	blurpix = Blurpix(picref)
	
	for i in range(blurpix.getWidth()):
		for j in range(blurpix.getHeight()):
			picnew.putpixel((i,j),blurpix.blurpix(i,j))
	return picnew


