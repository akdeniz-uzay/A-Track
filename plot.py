# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 18:33:56 2015

@author: ykilic
"""

import pandas as pd
import matplotlib.pyplot as plt
import os, glob
from pandas.lib import cache_readonly


class Plot:
    """
    MOD's plotting class.
        		
    """
    
    def catalogue(self, star_cat, target_folder):
        """
        Reads given ordered (corrected) coordinate file plot stars.
        :param star_cat: Ordered (corrected) star catalogue.
        :type star_cat: Text file object..
            		
        """
        catxy = pd.read_csv(star_cat, sep=",", names=["ref_x", "ref_y"], header=0)
        if not catxy.empty:
            catxy.plot(kind="scatter", x = "ref_x", y = "ref_y", xlim=(0, 2048), ylim=(0, 2048), fontsize=12, figsize=(10, 10))

        starcatfile = os.path.basename(star_cat)
        h_starcatfile, e_starcatfile = starcatfile.split(".")
    
        if os.path.exists(target_folder):
            pass
        else:
            os.mkdir(target_folder)
        if not catxy.empty:
            plt.title("Detected %s stray objects on %s" % (len(catxy), h_starcatfile))
            ax = plt.gca()
            ax.set_aspect('equal', 'datalim')
            plt.savefig("%s/%s.png" %(target_folder, h_starcatfile))
            plt.close()
        else:
            print "No objects detected on %s." %(starcatfile)


    def plotallcat(self, ordered_cats, target_folder):
        """
        Reads and plots all ordered (corrected) coordinate files under given directory.
        
        :param ordered_cats: Ordered coordinate folder.
        :type stray_cats: Directory object.
            		
        """      
        for catfile in sorted(glob.glob("%s/*affineremap.txt" %(ordered_cats))):
            self.catalogue(catfile, target_folder)
            print "Ploted all detected objects on: %s." %(os.path.basename(catfile))        

    def plotallobjects(self, ordered_cats, target_folder):
        """
        Reads all catalogue files under given ordered catalogue folder to draw all objects in one figure.
        
        :param ordered_cats: Ordered coordinate folder.
        :type stray_cats: Directory object.
            		
        """      
        starcat = sorted(glob.glob("%s/*affineremap.txt" %(ordered_cats)))
        onecatlist = pd.DataFrame(columns=["ref_x", "ref_y"])
        
        for objctlist in starcat:
            objtcat = pd.read_csv(objctlist, sep=",", names=["ref_x", "ref_y"], header=0)
            onecatlist = onecatlist.append(objtcat)
        onecatlist.plot(kind="scatter", x = "ref_x", y = "ref_y", xlim=(0, 2048), ylim=(0, 2048), fontsize=12, figsize=(10, 10))          

   
        if os.path.exists(target_folder):
            pass
        else:
            os.mkdir(target_folder)
        plt.title("Detected %s objects." % (len(onecatlist)))
        ax = plt.gca()
        ax.set_aspect('equal', 'datalim')    
        plt.savefig("%s/allobjects.png" %(target_folder))
        plt.close()