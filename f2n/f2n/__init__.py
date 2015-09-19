"""
f2n.py, the successor of f2n !
==============================

About
-----

f2n.py is a tiny python module to make a well-scaled PNG file out of a FITS image.
It's mainly a wrapper around pyfits + PIL. Aside of these two, we use only numpy.

PIL : http://www.pythonware.com/products/pil/
pyfits : http://www.stsci.edu/resources/software_hardware/pyfits


Usage
-----
You can use this python script both as a module or as an executable with command line options.
See the website and the examples provided in the tarball ! To learn about the methods of the f2nimage class, click on 
I{f2n.f2nimage} in the left menu.

Features
--------

f2n.py let's you crop the input image, rebin it, choose cutoffs and log or lin scales, draw masks, "upsample" the pixels without interpolation, circle and annotate objects, write titles or longer strings, and even compose several of such images side by side into one single png file.

For the location of pixels for drawing + labels, we work in "image" pixels, like ds9 and sextractor. This is true even when you have choosen to crop/rebin/upsample the image : you still specify all coordinates as pixels of the original input image !

By default we produce graylevel 8-bit pngs, for minimum file size. But you are free to use colours as well (thus writing 24 bit pngs).

Order of operations that should be respected for maximum performance (and to avoid "features" ... ) :

	- fromfits (or call to constructor)
	- crop
	- setzscale (auto, ex, flat, or your own choice)
	- rebin
	- makepilimage (lin, log, clin, or clog) (the c stands for colours... "rainbow")
	- drawmask, showcutoffs
	- upsample
	- drawcircle, drawrectangle, writelabel, writeinfo, writetitle, drawstarsfile, drawstarslist
	- tonet (or compose)

Ideas for future versions
-------------------------

	- variant of rebin() that rebins/upscales to approach a given size, like maxsize(500).
	- make vector graphics version, using pysvg


License
-------

Malte Tewes, December 2009

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
http://www.gnu.org/licenses/gpl.html

Note: Python 3 conversion contributed by Yucel Kilic on 29 Sep. 2015.
e-mail = yucelkilic@myrafproject.org
"""

__author__ = "Malte Tewes"
__copyright__ = "2010, Malte Tewes"
__version__ = "1.2.1"
__maintainer__ = "Yucel Kilic"

from f2n.f2n import f2nimage, fromfits, compose


