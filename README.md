# Moving Object Detection

### Dependencies:

* [Python](https://www.python.org/) 3.4.x or later.
* [Numpy](http://www.numpy.org/) 1.8.x or later.
* [Pandas](http://pandas.pydata.org/) 0.16.x or later.
* [AliPy](http://obswww.unige.ch/~tewes/alipy/) 2.0.x or later.
* [PyFITS](http://www.stsci.edu/institute/software_hardware/pyfits) 3.3.x or later.
* [f2n](https://github.com/akdeniz-uzay/mod/tree/master/f2n) for Python 3.
* [docopt] (https://github.com/docopt/docopt) for Python3.

### Usage:

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
  --skip-cats           Skip creating catalogue files if catalogue.
                        files had been created by user.
  --skip-pngs           Skip create PNGs and animation.
  --skip-gif            Skip create animation file.
```