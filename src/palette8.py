
#Divide in 8 colors: mean of r < 128, mean of r >= 128, idem for g and b.
# This will be probably grayish, but it's a start.
def palette8(picnew):
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
	for i in range(width):
		for j in range(height):
			(r,g,b) = pixref[i,j]
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
	print(meanr1,meang1,meanb1)
	print(meanr2,meang2,meanb2)
	
	for i in range(width):
		for j in range(height):
			(r,g,b) = pixref[i,j]
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
			#print(r,g,b)
			#print (pixnewij)
			picnew.putpixel((i,j),pixnewij)




