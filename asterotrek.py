# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 13:26:22 2015

@author: ykilic
"""

try:
    from asteractor import *
except:
    print "Can not load asteractor. Do you have asteractor.py?"
    raise SystemExit

import sys, os
try:
    import glob
except:
    print "Did you install glob?"
    raise SystemExit

try:
    import pandas as pd
except:
    print "Did you install pandas?"
    raise SystemExit

try:
    from plot import *
except:
    print "Can not load plot. Do you have plot.py?"
    raise SystemExit

def catread(cat_path, target_folder):
    """
    Reads "sextractor\'s" irregular result file and extract just (x, y) coordinate to specified file.
    
    :param cat_path: The target .pysexcat file
    :type cat_path: Text object
        		
    """    
    readcat = os.popen("cat %s| grep -v '#'| awk '{print $1,$2}'" %(cat_path))
    catname = os.path.basename(cat_path)
    h_catname, e_catname = catname.split(".")
    
    if os.path.exists("./%s/" %(target_folder)):
        pass
    else:
        os.mkdir("./%s" %(target_folder))
        
    f = open("%s/%s.txt" %(target_folder, h_catname),'w')
    for satir in readcat.readlines():
        f.write(satir)
    f.close()
    
def catreadall(catdir, target_folder):
    """
    Reads under given all sextractor's irregular result file directory's and extract just (x, y) coordinate to specified file.
    
    :param catdir: The target directory which contains all .pysexcat files
    :type catdir: Directory object
        		
    """    
    for catfile in sorted(glob.glob("%s/*.pysexcat" %(catdir))):
        catread(catfile, target_folder)

def makestarcat(ordered_cats):
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

def detectmovingobject(reference_cat, star_cat, target_folder):
        """
        Reads given ordered (corrected) coordinate file and detect moving object candidate in "starcat.txt".
        
        :param reference_cat: Ordered (corrected) star catalogue file for one image.
        :type reference_cat: Text file object.
        :param star_cat: Ordered (corrected) star catalogue file for all image.
        :type star_cat: Text file object..
            		
        """ 
        refcat = pd.read_csv(reference_cat, sep=" ", names=["ref_x", "ref_y"], header=None)
        starcat = pd.read_csv(star_cat, sep=" ", names=["ref_x", "ref_y"], header=None)
        
        strayobjectlist = pd.DataFrame(columns=["ref_x", "ref_y"])
        for i in range(len(refcat.ref_x)):
            if len(starcat[(abs(starcat.ref_x - refcat.ref_x[i]) < 1) & (abs(starcat.ref_y - refcat.ref_y[i]) < 1)]) < 2:
                strayobjectlist = strayobjectlist.append(starcat[(abs(starcat.ref_x - refcat.ref_x[i]) < 1) & (abs(starcat.ref_y - refcat.ref_y[i]) < 1)])

        starcatfile = os.path.basename(reference_cat)
        h_starcatfile, e_starcatfile = starcatfile.split(".")

        if os.path.exists(target_folder):
            pass
        else:
            os.mkdir(target_folder)        

        strayobjectlist.to_csv("%s/stray_%s.txt" %(target_folder, h_starcatfile))
        return strayobjectlist

def astromods(ordered_cats, target_folder):
    """
    Reads under given all sextractor's irregular result file directory's and extract just (x, y) coordinate to specified file.
    
    :param catdir: The target directory which contains all .pysexcat files
    :type catdir: Directory object
        		
    """
    for catfile in sorted(glob.glob("%s/*affineremap.txt" %(ordered_cats))):
        detectmovingobject(catfile, "%s/starcat.txt" %(ordered_cats), target_folder)
        print "Saved all detected stray objects to: %s/%s." %(ordered_cats, os.path.basename(catfile))

# Reads FITS file and ident/align stars
if sys.argv[1] == "-ri":
    """
    Ident stars on all FITS images according to reference image.
    Use this option for you have already aligned images.
    Usage: python asterotrek.py -ri <reference_img.fits>  
        		
    """
    try:
        runFilteroid = Filteroid(sys.argv[2])
        runFilteroid.ident()
    except:
        print "Usage error!"
        print "Usage: python asterotrek.py -ri <reference_img.fits>"
        raise SystemExit
    
elif sys.argv[1] == "-ra":
    """
    Align stars on all FITS images according to reference image.
    Usage: python asterotrek.py -ra <reference_img.fits>
        		
    """   
    try:    
        runFilteroid = Filteroid(sys.argv[2])
        runFilteroid.ident()
        runFilteroid.align()
    except:
        print "Usage error!"
        print "Usage: python asterotrek.py -ra <reference_img.fits>"
        raise SystemExit
# Reads sextractor's output and makes readable catalogue files 
elif sys.argv[1] == "-moc":
    """
    Makes ordered stars cats.
    Usage: python asterotrek.py -moc <alipy_cats_folder> <ordered_cats_folder>    
    		
    """
    try:
        catreadall(sys.argv[2], sys.argv[3])
    except:
        print "Usage error!"
        print "Usage: python asterotrek.py -moc <alipy_cats_folder> <ordered_cats_folder>"
        raise SystemExit
# Create readable catalogue file for comparison and check stars    
elif sys.argv[1] == "-msc":
    """
    Makes stars cats as one file.
    Usage: python asterotrek.py -moc <ordered_cats_folder>
        		
    """
    try:
        makestarcat(sys.argv[2])
    except:
        print "Usage error!"
        print "Usage: python asterotrek.py -moc <ordered_cats_folder>"
        raise SystemExit
# Detect stray objects on given cat file
elif sys.argv[1] == "-mod":
    """
    Detects stray stars in given catalogue file.
    Usage: python asterotrek.py -mod <reference_cat> <star_cat> <stray_cat_folder>
        		
    """
    try:
        detectmovingobject(sys.argv[2], sys.argv[3], sys.argv[4])
    except:
        print "Usage error!"
        print "Usage: python asterotrek.py -mod <reference_cat> <star_cat> <stray_cat_folder>"
        raise SystemExit
# Detect stray objects in given catalogue folder
elif sys.argv[1] == "-mods":
    """
    Detects all stray stars in given catalogue folder.
    Usage: python asterotrek.py -mods <ordered_cats_folder> <target_folder>
        		
    """
    try:
        astromods(sys.argv[2], sys.argv[3])
    except:
        print "Usage error!"
        print "Usage: python asterotrek.py -mods <ordered_cats_folder> <target_folder>"
        raise SystemExit    
# Plot objects in catalogue file    
elif sys.argv[1] == "-plt":
    """
    Plot objects in given catalogue (ordered) file.
    Usage: python asterotrek.py -plt <catalogue_file> <target_folder>      		
    """
    try:
        plotCat = Plot()
        plotCat.catalogue(sys.argv[2], sys.argv[3])
    except:
        print "Usage error!"
        print "Usage: python asterotrek.py -plt <catalogue_file> <target_folder>"
        raise SystemExit 
        
# Plot objects in catalogue folder 
elif sys.argv[1] == "-plts":
    """
    Plot each catalogue files in given catalogue (ordered) folder.
    Usage: python asterotrek.py -plts <ordered_cat_folder> <target_folder>    		
    """
    try:
        plotCat = Plot()
        plotCat.plotallcat(sys.argv[2], sys.argv[3])
    except:
        print "Usage error!"
        print "Usage: python asterotrek.py -plts <ordered_cat_folder> <target_folder>"
        raise SystemExit
        
# Plot all objects to one matplotlib figure
elif sys.argv[1] == "-pltone":
    """
    Plot all objects in given catalogue (ordered) folder to one figure.
    Usage: python asterotrek.py -pltone <ordered_cat_folder> <target_folder>    		
    """
    try:
        plotCat = Plot()
        plotCat.plotallobjects(sys.argv[2], sys.argv[3])
    except:
        print "Usage error!"
        print "Usage: python asterotrek.py -pltone <ordered_cat_folder> <target_folder>"
        raise SystemExit 