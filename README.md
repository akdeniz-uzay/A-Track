# Moving Object Detection

### Dependencies:

* [Python](https://www.python.org/) 3.4.x or later.
* [Numpy](http://www.numpy.org/) 1.8.x or later.
* [Pandas](http://pandas.pydata.org/) 0.16.x or later.
* [AliPy](http://obswww.unige.ch/~tewes/alipy/) 2.0.x or later.
* [PyFITS](http://www.stsci.edu/institute/software_hardware/pyfits) 3.3.x or later.
* [f2n](https://github.com/akdeniz-uzay/mod/tree/master/f2n) for Python 3

### <a name="usage"></a> Usage

```bash
usage: python3 atrack.py [-h] [--ref ref_image] [--skip-align] [--skip-cats]
                         [--skip-pngs] [--skip-gif] [--version]
                         fits_dir

A-Track.

positional arguments:
  fits_dir         FITS image directory.

optional arguments:
  -h, --help       show this help message and exit
  --ref ref_image  Reference FITS image for alignment (with path).
  --skip-align     Skip alignment if alignment is already done.
  --skip-cats      Skip creating catalog files if they are already created.
  --skip-pngs      Skip creating PNGs.
  --skip-gif       Skip creating animation file.
  --version        Show version.
```

### Installation

A-Track is tested on Ubuntu 14.04 LTS, Fedora 22 and Mac OS X Yosemite.

To install A-Track on any OS, run the following commands:


**Ubuntu:** ```sudo apt-get install python3 python3-pip imagemagick git-all sextractor```

**Fedora:** ```sudo dnf install python3-pip imagemagick git-all```

* Install the latest SExtractor from [here](http://www.astromatic.net/download/sextractor/) (we suggest v2.19.5 as the older versions detect fewer objects).

**Mac OS X:** You need [Homebrew](http://brew.sh) to install the dependencies.

* ```brew install imagemagick git python3 sextractor```

Numpy, Pandas, Scipy, pyFITS and pillow can be installed with pip3 (GNU/Linux users! Don't forget the ```sudo```):

```bash

cd ~
pip3 install numpy pandas pyfits pillow scipy matplotlib

git clone https://github.com/japs/alipy
cd alipy
python3 setup.py install

cd ..
git clone https://github.com/japs/astroasciidata
cd astroasciidata
python3 setup.py install
cd ..
```

After installing Alipy, you should locate the built align.py file and change

Line 51:
```
   tofits(alifilepath, data, hdr = None, verbose = verbose)
```
To:
```
   if hdr:
       tofits(alifilepath, data, hdr = hdr, verbose = verbose)
   else:
       tofits(alifilepath, data, hdr = None, verbose = verbose)

```
Finally, you can download the A-Track files and install the f2n package:

```
cd ..
git clone https://github.com/akdeniz-uzay/A-Track
cd f2n
python3 setup.py install
```

Now, you have A-Track! You can open a command-line interface in the A-Track directory and execute the file [atrack.py](#usage)!

**P.S.:** If you want to use A-Track on Windows, you need to install SExtractor first! This is a bit tricky. Please see the [link](http://www.astromatic.net/forum/showthread.php?tid=948).
