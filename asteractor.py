# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 23:16:29 2015

@author: ykilic
"""

# -*- coding: utf-8 -*-
#
# Copyleft, Yücel Kılıç (yucelkilic@myrafproject.org).
# This is open-source software licensed under a GPLv3 license.

import alipy
import glob

class Filteroid:
    def __init__(self, ref_image):
        """
        Filteroid's init function.
        
        :param ref_image: Reference image file
        :type ref_image: Image file object
            		
        """          
        self.ref_image = ref_image
        self.images_to_align = sorted(glob.glob("*.fits"))  
        self.identifications = alipy.ident.run(self.ref_image, self.images_to_align, visu=False, sexkeepcat=True)
        # That's it !
        # Put visu=True to get visualizations in form of png files (nice but much slower)
        # On multi-extension data, you will want to specify the hdu (see API doc).
        
        # The output is a list of Identification objects, which contain the transforms :        
        
    def ident(self):        
        """
        Stars find function for selected FITS image.
            		
        """  
        for id in self.identifications: # list of the same length as images_to_align.
                if id.ok == True: # i.e., if it worked
        
                        print "%20s : %20s, flux ratio %.2f" % (id.ukn.name, id.trans, id.medfluxratio)
                        # id.trans is a alipy.star.SimpleTransform object. Instead of printing it out as a string,
                        # you can directly access its parameters :
                        #print id.trans.v # the raw data, [r*cos(theta)  r*sin(theta)  r*shift_x  r*shift_y]
                        #print id.trans.matrixform()
                        #print id.trans.inverse() # this returns a new SimpleTransform object
        
                else:
                        print "%20s : no transformation found !" % (id.ukn.name)
    
    def align(self):
        """
        FITS fike align for alipy.
            		
        """   
        # Minimal example of how to align images :
        
        outputshape = alipy.align.shape(self.ref_image)
        # This is simply a tuple (width, height)... you could specify any other shape.
        
        for id in self.identifications:
                if id.ok == True:
        
                        # Variant 1, using only scipy and the simple affine transorm :
                        alipy.align.affineremap(id.ukn.filepath, id.trans, shape=outputshape, makepng=False)
                        # By default, the aligned images are written into a directory "alipy_out".
        
        # To be continued ...

        
        