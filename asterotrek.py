# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 13:26:22 2015

@author: ykilic
"""


from asteractor import *
import sys, os
import glob
import pandas as pd
import matplotlib.pyplot as plt

def catRead(cat_path):
    """
    Reads sextractor's irregular result file and extract just (x, y) coordinate to specified file.
    
    :param cat_path: The target .pysexcat file
    :type cat_path: Text object
        		
    """    
    readcat = os.popen("cat %s| grep -v '#'| awk '{print $1,$2}'" %(cat_path))
    catname = os.path.basename(cat_path)
    h_catname, e_catname = catname.split(".")
    
    if os.path.exists("./ordered_cats/"):
        pass
    else:
        os.mkdir("./ordered_cats")
        
    f = open("./ordered_cats/%s.txt" %(h_catname),'w')
    for satir in readcat.readlines():
        f.write(satir)
    f.close()
    
def catReadAll(catdir):
    """
    Reads under given all sextractor's irregular result file directory's and extract just (x, y) coordinate to specified file.
    
    :param catdir: The target directory which contains all .pysexcat files
    :type catdir: Directory object
        		
    """    
    for catfile in sorted(glob.glob("%s/*.pysexcat" %(catdir))):
        catRead(catfile)

def makeStarCat(ordered_cats):
    """
    Reads all ordered coordinate file under ordered_cats directory and extract just (x, y) coordinate to "one catalogue file" named as "starcat.txt".
    
    :param ordered_cats: The target directory which contains all corrected(readeble) coordinate files.
    :type ordered_cats: Directory object.
        		
    """      
    if os.path.exists(ordered_cats):
        catfiles = glob.glob("%s/*.txt" %(ordered_cats))
                         
        with open("%s/starcat.txt" %(ordered_cats), "wb") as outfile:
            for f in catfiles:
                with open(f, "rb") as infile:
                    outfile.write(infile.read())

def plotStray(reference_cat, star_cat):
    """
    Reads ordered (corrected) coordinate file under ordered_cats directory and plot stars which does not match in "starcat.txt".
    
    :param reference_cat: Ordered (corrected) star catalogue file for one image.
    :type reference_cat: Text file object.
    :param star_cat: Ordered (corrected) star catalogue file for all image.
    :type star_cat: Text file object..
        		
    """    
    refcat = pd.read_csv(reference_cat, sep=" ", names=["ref_x", "ref_y"], header=None)
    starcat = pd.read_csv(star_cat, sep=" ", names=["ref_x", "ref_y"], header=None)
    
    lastlist = pd.DataFrame(columns=["ref_x", "ref_y"])
    for i in range(len(refcat.ref_x)):
        if len(starcat[(abs(starcat.ref_x - refcat.ref_x[i]) < 1) & (abs(starcat.ref_y - refcat.ref_y[i]) < 1)]) < 2:
            lastlist = lastlist.append(starcat[(abs(starcat.ref_x - refcat.ref_x[i]) < 1) & (abs(starcat.ref_y - refcat.ref_y[i]) < 1)])
    lastlist.plot(kind="scatter", x = "ref_x", y = "ref_y", xlim=(0, 2048), ylim=(0, 2048), fontsize=12, figsize=(10, 10))
    
    refcat_file = os.path.basename(reference_cat)
    h_refcat_file, e_refcat_file = refcat_file.split(".")

    if os.path.exists("./stray_png/"):
        pass
    else:
        os.mkdir("./stray_png/")
    plt.title("Detected %s stray objects on %s" % (len(lastlist), h_refcat_file))
    ax = plt.gca()
    ax.set_aspect('equal', 'datalim')    
    plt.savefig("./stray_png/%s.png" %(h_refcat_file))
    plt.close()
     
def plotStrayAll(ordered_cats):
    """
    Reads all ordered (corrected) coordinate file under ordered_cats directory and plot stars which does not match in "starcat.txt".
    
    :param ordered_cats: Ordered (corrected) star catalogue folder.
    :type ordered_cats: Directory object.
        		
    """      
    for catfile in sorted(glob.glob("%s/*affineremap.txt" %(ordered_cats))):
        plotStray(catfile, "./ordered_cats/starcat.txt")
        print "Ploted all detected objects on: %s." %(os.path.basename(catfile))



if sys.argv[1] == "-ri":
    """
    Ident stars on all FITS images according to reference image.
    Use this option for you have already aligned images.
    Usage: python asterotrek.py -ri <reference_img.fits>  
        		
    """
    
    runFilteroid = Filteroid(sys.argv[2])
    runFilteroid.ident()
    
elif sys.argv[1] == "-ra":
    """
    Align stars on all FITS images according to reference image.
    Usage: python asterotrek.py -ra <reference_img.fits>
        		
    """   
    
    runFilteroid = Filteroid(sys.argv[2])
    runFilteroid.ident()
    runFilteroid.align()
    
elif sys.argv[1] == "-moc":
    """
    Makes ordered stars cats.
    Usage: python asterotrek.py -moc alipy_cats    
    		
    """      
    
    catReadAll(sys.argv[2])
    
elif sys.argv[1] == "-msc":
    """
    Makes stars cats as one file.
    Usage: python asterotrek.py -moc ordered_cats
        		
    """     
    
    makeStarCat(sys.argv[2])
    
elif sys.argv[1] == "-plt":
    """
    Plot detected moving objects.
    Usage: python asterotrek.py -plt ordered_cats        		
    """   
    
    plotStrayAll(sys.argv[2])

