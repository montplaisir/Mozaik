
import os
import sys
from PIL import Image
cwd = os.getcwd()
import blur
import palette8

if len(sys.argv) < 3:
	print("Syntax: " + sys.argv[0] + " filename [blur|palette8]")
	exit(0)
	
## File to be read. ##
filename = sys.argv[1]

## Name of the filter. Used for naming output file and to select filter. ## 
filtername = sys.argv[2]

outfilename = filename
outfilename = filename.replace(".","_" + filtername + ".")
fullfilename = cwd + '\\' + filename
fulloutfilename = cwd + '\\' + outfilename 
picref = Image.open(fullfilename)

def applyFilter(filtername, picref):
	if "blur" == filtername:
		return blur.blur(picref)
	elif "palette8" == filtername:
		return palette8.palette8(picref)
	else:
		return "Invalid filter name"
	
	
picnew = applyFilter(filtername, picref)

picnew.show()
picnew.save(fulloutfilename)