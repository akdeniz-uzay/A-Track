

# The following two lines are only needed if f2n.py and f2n_fonts
# are not yet copied somewhere into your usual python path !
import sys
sys.path.append("../.") # The directory that contains f2n.py and f2n_fonts !

# Now we can go on as usual :
import f2n

# And show a minimalistic exemple :

myimage = f2n.fromfits("example.fits") # The way to read a FITS file.
myimage.setzscale() # By default, automatic cutoffs will be calculated.
myimage.makepilimage("lin") # By default, a log transformation would be used.
myimage.tonet("1_simple.png") # We write the png.



