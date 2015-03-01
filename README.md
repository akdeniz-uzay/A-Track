# Moving Object Detection Pipeline on FITS Images

### Dependencies:
* [Python](http://python.org) 2.7.x or later.
* [AliPy](http://obswww.unige.ch/~tewes/alipy/) 2.0.
* [Pandas](http://pandas.pydata.org/) 0.15 or later.

### Usage:

**Step 1:** Align your scientific images with reference FITS image.

```bash
$ python asterotrek.py -ra reference.fits
```

**Step 2:** Run the star identification algorithm for aligned images.

```bash
$ python asterotrek.py -ri reference.fits
```

**Step 3:** Read the sextractor's result files for extracting ordered (x, y) coordinates to specified directory.

```bash
$ python asterotrek.py -moc alipy_cats ordered_cats
```
* **-moc**: make ordered catalogue

**Step 4:** Make one object catalogue from all ordered object cats (starcat.txt).

```bash
$ python asterotrek.py -msc ordered_cats
```
* **-msc**: make star catalogue

**Step 5:** Search (check with starcat.txt) stray objects for each catalogue file and make candidate moving object catalogues under specified directory.

```bash
$ python asterotrek.py -mods ordered_cats stray_cats
```
* **-mods**: make moving object catalogues

**Step 6:** Plot objects in ordered catalogue files to virtual CCD image (figure) and save specified directory. 

```bash
$ python asterotrek.py -plts stray_cats stray_png
```
* **-plts**: plot catalogues to specified directory

**Step 7:** Plot objects in all ordered catalogue files to ONE virtual CCD image (figure) and save specified directory. 

```bash
$ python asterotrek.py -pltone stray_cats ./
```
* **-pltone**: plot catalogues under specified directory to ONE figure with name "allobject.png".

**Step 8:** Plot detected lines save/nosave mode.

```bash
$ python asterotrek.py -dl stray_cats/ -nosave
```
* **-dl**: detect lines
* **stray_cats/**: Candidate MO cats.
* **-nosave**: Do not save figure.

**Step 9:** Convert FITS images into PNG files. This command draw all detected MOs on PNGs. 

```bash
$ python asterotrek.py -fits2png ./stray_cats/ ./ png/
```
* **./stray_cats/**: Detected stray object catalogue files directory.
* **./**: FITS image directory.
* **png/**: PNG files will be saved in the directory.

**Step 10:** Convert PNG images to animated GIF file.

```bash
$ python asterotrek.py -makegif png/ animated
```
* **png/**: PNG files directory to be converted.
* **animated**: Animated GIF file (output).

