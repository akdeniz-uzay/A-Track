#!/bin/sh

# A-Track installer for GNU/Linux System
# Authors: Yücel Kılıç, Murat Kaplan, Nurdan Karapınar, Tolga Atay.
# This is an open-source software licensed under GPLv3.

# Variables to use

# Stop if there are any errors.
set -e

# Functions to use.
#

atrack_install_dep(){
   echo ''
   echo '      Installing dependencies for A-Track.' 
   echo '      (Be patient...)'
   echo ''
   echo ''
   echo '      imagemagick, pandas, numpy, sextractor, pyfits'
   echo '      pyfits, scipy, matplotlib, pyds9, alipy'
   echo '      astroasciidata, f2n, pillow;'
   echo '      will be installed. (Be patient...)'
   echo ''
   brew update
   for pkg in imagemagick git python3 sextractor wget; do
       if brew list -1 | grep -q "^${pkg}\$"; then
	   echo "Package '$pkg' is already installed!"
       else
	   brew install $pkg
       fi
   done
   pip3 install --upgrade numpy pandas pyfits scipy matplotlib pillow
   pip3 install git+https://github.com/ericmandel/pyds9.git#egg=pyds9
   mkdir atrack_tmp/
   cd atrack_tmp/
   echo ''
   echo '      Installing alipy.'
   echo ''
   git clone https://github.com/akdeniz-uzay/alipy.git
   cd alipy
   python3 setup.py install
   cd ..
   echo ''
   echo '      Installing astroasciidata.'
   echo ''
   git clone https://github.com/japs/astroasciidata.git
   cd astroasciidata
   python3 setup.py install
   cd ../..
   echo ''
   echo '      Installing f2n.'
   echo ''
   cd f2n
   python3 setup.py install
   cd ..
   if [ -x "/usr/bin/sextractor" ] ; then
       ln -s /usr/bin/sextractor /usr/bin/sex
   fi
   rm -rf atrack_tmp/
}

atrack_post(){
   echo ''
   echo '      A-Track has been installed.'
   echo ''
   echo '      You can open a command-line interface' 
   echo '      in the A-Track directory and run A-Track.'
   echo '      Example: python3 atrack.py fits_dir/'
   echo ''
}

install_atrack(){
    atrack_install_dep
    atrack_post
}

fail_install(){
   echo ''
   echo 'Do you have the required OS?'
   echo 'If you have GNU/Linux, use install_linux.sh instead.'
   echo 'Otherwise, install A-Track manually :('
   echo ''
}

fail_brew(){
   echo ''
   echo 'Do you have brew?'
   echo 'Please install brew: http://brew.sh'
   echo ''
}

# Check which distro are we running and run the apropiate script.

if [ "$(uname -s)" == "Darwin" ]; then
    if [ -x "/usr/local/bin/brew" ] ; then
	echo ''
	echo 'The following extra packages will be installed for A-Track;'
	echo 'imagemagick, pandas, numpy, sextractor, pyfits'
	echo 'pyfits, scipy, matplotlib, pyds9, alipy'
	echo 'astroasciidata, f2n, pillow.'
	read -r -p "Do you want to proceed? [y/N] " response
	case $response in
	    [yY][eE][sS]|[yY])
		rm -rf atrack_tmp/;
		install_atrack;
		;;
	    *)
		exit 1
		;;
	esac
    else
	fail_brew
    fi
elif [ "$(uname -s)" == "Linux" ]; then
    fail_install;
fi
