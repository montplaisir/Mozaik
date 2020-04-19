
import os
import sys
from PIL import Image
cwd = os.getcwd()
import blur

if len(sys.argv) < 3:
	print("Syntax: " + sys.argv[0] + " filename [blur]")
	exit(0)
	
## File to be read. ##
filename = sys.argv[1]

## Name of the filter. Used for naming output file only. ##
# Could be generalized to select filter. ## 
filtername = sys.argv[2]

outfilename = filename
outfilename = filename.replace(".","_" + filtername + ".")
fullfilename = cwd + '\\' + filename
fulloutfilename = cwd + '\\' + outfilename 
picref = Image.open(fullfilename)

picnew = blur.blur(picref)

picnew.show()
picnew.save(fulloutfilename)