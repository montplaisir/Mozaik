
import os
import sys
from PIL import Image
cwd = os.getcwd()
import blur
import palette8
import brightcolors
import saturation
import zones

if len(sys.argv) < 3:
    print("Syntax: " + sys.argv[0] + " filename [blur|palette8|brightcolors|saturation|zones]")
    exit(0)
    
## File to be read. ##
filename = sys.argv[1]

## Name of the filter. Used for naming output file and to select filter. ## 
filtername = sys.argv[2]

outfilename = filename
outfilename = filename.replace(".","_" + filtername + ".")
blurfilename = filename.replace(".","_blur.")
fullfilename = os.path.join(cwd, filename)
fulloutfilename = os.path.join(cwd, outfilename)
fullblurfilename = os.path.join(cwd, blurfilename)
picref = Image.open(fullfilename);



def applyBlur(picref):
    width = picref.size[0]
    height = picref.size[1]
    numSmooth = int((width + height) / 1000)
    print("smoothing image...")
    picnew = blur.blur(picref)
    for s in range(1,numSmooth):
        print("smoothing some more...")
        picnew = blur.blur(picnew)

    picnew.save(fullblurfilename)
    return picnew


def applyFilter(filtername, picref):
    # preprocessing
    if not "blur" == filtername:
        if os.path.isfile(fullblurfilename):
            picref = Image.open(fullblurfilename)
        else:
            picref = applyBlur(picref)


    if "blur" == filtername:
        return blur.blur(picref)
    elif "palette8" == filtername:
        return palette8.palette8(picref)
    elif "brightcolors" == filtername:
        return brightcolors.apply(picref)
    elif "saturation" == filtername:
        return saturation.apply(picref)
    elif "zones" == filtername:
        return zones.apply(picref)
    else:
        return "Invalid filter name"
    
    
picnew = applyFilter(filtername, picref)

picnew.show()
picnew.save(fulloutfilename)
