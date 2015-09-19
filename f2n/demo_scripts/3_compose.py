

# The following two lines are only needed if f2n.py and f2n_fonts
# are not yet copied somewhere into your usual python path !
import sys
sys.path.append("../.") # The directory that contains f2n.py and f2n_fonts !

import f2n
import copy


myimage = f2n.fromfits("example.fits")
mylargeimage = copy.deepcopy(myimage)

myimage.crop(70, 170, 60, 160)
myimage.setzscale("auto", "ex")

linimage = copy.deepcopy(myimage)
logimage = copy.deepcopy(myimage)

linimage.makepilimage("lin", negative = False)
logimage.makepilimage("log", negative = False)

linimage.upsample(2)
linimage.writetitle("lin")
linimage.drawcircle(112, 101, r=15)

logimage.upsample(2)
logimage.writetitle("log")

mylargeimage.crop(30, 230, 60, 160)
mylargeimage.setzscale(2000, "auto") # We can set manual cutoffs too.
mylargeimage.rebin(4)
mylargeimage.makepilimage("clin", negative = True)
mylargeimage.upsample(8)
#mylargeimage.drawcircle(112, 101, r=15) # Despite the rebin and upsample, coordinates are the same !
mylargeimage.writetitle("clin")

mylargeimage.writeinfo(["f2n.py can rebin and upsample", "your images ! But doing both for the same", "image doesn't make sense."])

f2n.compose([[linimage, logimage], [mylargeimage]], "3_compose.png") # Instead of the tonet() method, we call the compose() function.


