
import os
from PIL import Image
cwd = os.getcwd()
import blur

## File to be read. ##
# Could be generalized as input on command line.
filename = "horacio.bmp"

## Name of the filter. Used for naming output file only. ##
# Could be generalized as input on command line, and to select filter. ## 
filtername = "blur"

outfilename = filename
outfilename = filename.replace(".","_" + filtername + ".")
fullfilename = cwd + '\\' + filename
fulloutfilename = cwd + '\\' + outfilename 
picref = Image.open(fullfilename)

#pixref = picref.load()
picnew = blur.blur(picref)

picnew.show()
picnew.save(fulloutfilename)