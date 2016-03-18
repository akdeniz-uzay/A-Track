# Moving Object Detection

### Dependencies:

* [Python](https://www.python.org/) 3.4.x or later.
* [Numpy](http://www.numpy.org/) 1.8.x or later.
* [Pandas](http://pandas.pydata.org/) 0.16.x or later.
* [AliPy](http://obswww.unige.ch/~tewes/alipy/) 2.0.x or later.
* [PyFITS](http://www.stsci.edu/institute/software_hardware/pyfits) 3.3.x or later.
* [f2n](https://github.com/akdeniz-uzay/mod/tree/master/f2n) for Python 3

### <a name="usage"></a> Usage

```
usage: python3 atrack.py [-h] [--ref ref_image] [--skip-align] [--skip-cats]
                         [--skip-pngs] [--skip-gif] [--version]
                         fits_dir

A-Track.

positional arguments:
  fits_dir         FITS image directory (full path)

optional arguments:
  -h, --help       show this help message and exit
  --ref ref_image  reference FITS image for alignment (full path)
  --skip-align     skip alignment if alignment is already done
  --skip-cats      skip creating catalog files if they are already created
  --skip-pngs      skip creating PNGs
  --skip-gif       skip creating animation file
  --version        show version
```

### Installation

A-Track is tested on Ubuntu 14.04 LTS, Fedora 22 and Mac OS X Yosemite. If you want to use A-Track on Windows, you need to install SExtractor first! This is a bit tricky. Please see the [this thread](http://www.astromatic.net/forum/showthread.php?tid=948).

To install A-Track on Linux or Mac, you can simply download the A-Track package and run the installation scripts install_linux.sh (for Linux: `sudo sh install_linux.sh`) or install_mac.sh (for Mac: `sh install_mac.sh`).

<br>
Alternatively, you can install A-Track manually following these steps:

1. **Install Python3, pip3, imagemagick, git, and SExtractor:**

  **Ubuntu:**  
  `sudo apt-get install python3 python3-dev python3-pip imagemagick sextractor libxt-dev git build-essential`

  **Fedora:**  
  `sudo dnf install python3 python3-devel python3-pip imagemagick sextractor libXt-devel git make automake gcc gcc-c++ kernel-devel`  
  Install the latest SExtractor from [here](http://www.astromatic.net/download/sextractor/) (we recommend v2.19.5 as the older versions detect fewer objects).

  **Mac OS X:**  
  `brew install python3 python3-pip imagemagick git-all sextractor`  
  (You will need [Homebrew](http://brew.sh) to install the dependencies.)  
  ` `
  
2. **Install Numpy, Pandas, Scipy, pyFITS, and pillow using pip3:**

  `sudo pip3 install scipy pandas numpy pyfits pillow`  
  (Mac users do not use `sudo`.)  
  ` `

3. **Download and install astroasciidata:**  

  `git clone https://github.com/japs/astroasciidata.git`  
  `cd astroasciidata`  
  `sudo python3 setup.py install`  
  (Mac users do not use `sudo`.)  
  ` `

4. **Download and install Alipy:**  

  `git clone https://github.com/akdeniz-uzay/alipy.git`  
  `cd alipy`  
  `sudo python3 setup.py install`  
  (Mac users do not use `sudo`.)  
  ` `

5. **Download the A-Track package and install f2n:**  

  `git clone https://github.com/akdeniz-uzay/A-Track.git`  
  `cd A-Track/f2n`  
  `sudo python3 setup.py install`  
  (Mac users do not use `sudo`.)

Now, you have A-Track! You can open a command-line interface in the A-Track directory and [run A-Track](#usage).
