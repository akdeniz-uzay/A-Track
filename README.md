# Moving Object Detection Pipeline on FITS Images

### Dependencies:
* [Python](http://python.org) 2.7.x or later.
* [SExtractor] (http://www.astromatic.net/software/sextractor) 2.19.x or later.
* [AliPy](http://obswww.unige.ch/~tewes/alipy/) 2.0.
* [Pandas](http://pandas.pydata.org/) 0.15 or later.

### Usage:

**Step 1:** Align your scientific images with reference FITS image.

```bash
$ python asterotrek.py -align "path/*.fits" path/reference.fits path/aligned
```

**Step 2:** Run the object identification algorithm (SExtractor) for aligned images.

```bash
$ python asterotrek.py -sextractor "fitsdir/*.fits" path/cats/
```

**Step 3:** Make one object catalogue file from all catalogue files (mastercat.txt).

```bash
$ python asterotrek.py -makemaster path/catdir
```
* **-makemaster**: make master catalogue

**Step 4:** Search (check with mastercat.txt and save eligible objects to candidate objects file) candidate objects for each catalogue file and make candidate moving object catalogues under specified directory.

```bash
$ python asterotrek.py -xcan path/catdir path/candidatedir
```
* **-xcan**: Extract candidate objects from catalogue files.

**Step 5:** Detect lines with multi-processing from the candidate cats.

```bash
$ python asterotrek.py -mdl path/candidatedir path/
```
* **-mdl**: detect lines with multi-processing
* **path/candidatedir**: Candidate MO catalogue directory.
* **path/fitsdir/**: Aligned FITS images directory.

**Step 6:** Converts FITS images into PNG files with detected objects (with-multi-processing). 

```bash
$ python asterotrek.py -dlwpng path/candidatedir path/fitsdir path/png/
```
* **path/candidatedir**: Directory of candidate object catalogue files.
* **path/fitsdir**: FITS image directory.
* **path/png/**: PNG files will be saved in the directory.

Note: You can use directly f2n for converting FITS images to PNG images with following command.

```bash
$ python asterotrek.py -fits2png fitsdir/ path/png/
```

**Step 7:** Plot catalogue file into DS9.

```bash
$ python asterotrek.py -plot2ds9 <fitsimage> <catfile>
```
* **fitsimage/**: FITS image.
* **catfile**: Catalogue file to be ploted into DS9.

**Step 8:** Convert PNG images to animated GIF file.

```bash
$ python asterotrek.py -makegif png/ animated
```
* **png/**: PNG files directory to be converted.
* **animated**: Animated GIF file (output).

