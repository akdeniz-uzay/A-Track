# Moving Object Detection

### Dependencies:

* [Python](https://www.python.org/) 3.4.x or later.
* [Numpy](http://www.numpy.org/) 1.8.x or later.
* [Pandas](http://pandas.pydata.org/) 0.16.x or later.
* [AliPy](http://obswww.unige.ch/~tewes/alipy/) 2.0.x or later.
* [PyFITS](http://www.stsci.edu/institute/software_hardware/pyfits) 3.3.x or later.
* [f2n](https://github.com/akdeniz-uzay/mod/tree/master/f2n) for Python 3.0
* [docopt](https://github.com/docopt/docopt) for Python 3.

### <a name="usage"></a> Usage

 ```bash
A-Track.

Usage:
  atrack.py <fits_dir> [-r <ref_image>, --ref=<ref_image>] [--skip-align]
                       [--skip-cats] [--skip-pngs]
                       [--skip-gif]
  atrack.py (-h | --help)
  atrack.py --version

Options:
  -h --help             Show this screen.
  --version             Show version.
  -r --ref=<ref_image>  Reference FITS image for alignment.
  --skip-align          Skip aligment if alignment had already done.
  --skip-cats           Skip creating catalogue files if catalogue
                        files had been created by user.
  --skip-pngs           Skip create PNGs and animation.
  --skip-gif            Skip create animation file.
 ```

### Installation

A-Track tested on (X)Ubuntu 14.04 LTS, Fedora >22 and Mac OS X >Yosemite.

To install A-Track on any OS, run the following commands;


**Ubuntu:** ```sudo apt-get install python3 python3-pip imagemagick git-all sextractor```

**Fedora:** ```sudo dnf install python3-pip imagemagick git-all```

* Select and install latest SExtractor from [here](http://www.astromatic.net/download/sextractor/) (We suggest v2.19.5).

**Mac OS X:** You need [Homebrew](http://brew.sh) for install dependencies.

* ```brew install imagemagick git python3 sextractor```

Now, we can continue with pip3 :) (GNU/Linux users! Don't forget the ```sudo```);

```bash

cd ~
pip3 install numpy pandas pyfits docopt scipy matplotlib```

git clone https://github.com/japs/alipy
cd alipy
python3 setup.py install
cd ..
git clone https://github.com/japs/astroasciidata
cd astroasciidata
python3 setup.py install
cd ..
```

After install Alipy you should fix the problem descirebed as [issue#1](https://github.com/akdeniz-uzay/A-Track/issues/1).

```bash

cd ..
git clone https://github.com/akdeniz-uzay/A-Track
cd f2n
python3 setup.py install
```

Now, you have the A-Track! Copy your FITS images folder under A-Track/ then run the [atrack.py](#usage)!

**P.S.:** If you want to install A-Track on Windows. You need to install SExtractor first! However, it is not very easy :) Please see the [link](http://www.astromatic.net/forum/showthread.php?tid=948).
* Also, you can use older version of SExtractor (v2.0.0), but this version detects considerably less objects than latest version.






