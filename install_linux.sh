#!/bin/sh

# A-Track installer for GNU/Linux System
# Authors: Yücel Kılıç, Murat Kaplan, Nurdan Karapınar, Tolga Atay.
# This is an open-source software licensed under GPLv3.

# Variables to use

DEPS_deb="python3 python3-dev python3-pip python3-numpy
python3-matplotlib python3-scipy python3-pyfits python3-pil 
wget imagemagick libxt-dev git-all sextractor build-essential
"

DEPS_rpm="python3 python3-devel python3-pip python3-numpy
python3-matplotlib python3-scipy python3-pyfits python3-pillow 
wget ImageMagick libXt-devel git-all sextractor make automake 
gcc gcc-c++ kernel-devel
"

ROOT_UID=0
#E_NOTROOT=67

# Stop if there are any errors.
set -e

# Check if we are root.
if [ ! "`whoami`" = "root" ]
then
    echo '     Please run the script as root or sudo.'
    echo '     If you are in Ubuntu, you can'
    echo '     become root with'
    echo '         sudo -s'
    echo '           or        '
    echo '         sudo ./install.sh'
    exit 1
fi


# Functions to use.
#
atrack_dep_deb()   {
   echo ''
   echo '      Installing dependencies for A-Track.' 
   echo '      (Be patient...)'
   echo ''
   apt-get install --no-install-recommends -y $DEPS_deb
}

atrack_dep_rpm()   {
   echo ''
   echo '      Installing dependencies (Be patient...)'
   echo ''
   yum -y install $DEPS_rpm
}

atrack_dep_pip()   {
   echo ''
   echo '      Installing dependencies via pip3.'
   echo ''
   echo ''
   echo '      Installing pandas, docopt, pyds9' 
   echo '      (Be patient...)'
   echo ''
   pip3 install docopt pandas
   pip3 install git+https://github.com/ericmandel/pyds9.git#egg=pyds9
   mkdir atrack_tmp/
   cd atrack_tmp/
   echo ''
   echo '      Installing alipy.'
   echo ''
   wget https://dl.dropboxusercontent.com/u/3985402/alipy.tar.gz
   tar -xvf alipy.tar.gz
   cd alipy
   python3 setup.py install
   cd ..
   echo ''
   echo '      Installing astroasciidata.'
   echo ''
   git clone https://github.com/japs/astroasciidata
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

atrack_post()    {
   echo ''
   echo '      A-Track has been installed.'
   echo ''
   echo '      Now, copy your FITS files into' 
   echo '      a folder under A-Track/ then run it!'
   echo '      Example: python3 atrack.py folder/'
   echo ''
}

install_atrack_deb()   {
    atrack_dep_deb
    atrack_dep_pip
    atrack_post
}

install_atrack_rpm()   {
    atrack_dep_rpm
    atrack_dep_pip
    atrack_post
}

fail_install()  {
   echo ''
   echo 'Do not you have required GNU/Linux Distro?'
   echo '(Fedora, Ubuntu, Debian, LinuxMint, CentOS, RedHat)'
   echo 'You need to install A-Track manually:('
   echo ''
}

# Check which distro are we running and run the apropiate script.

distro=$(cat /etc/issue| head -n1| awk '{print $1}')

if [ $distro = "Debian" -o $distro = "Ubuntu" -o $distro = "LinuxMint" ]; then
    rm -rf atrack_tmp/;
    install_atrack_deb;
elif [ $distro = "Fedora" -o $distro = "CentOS" ]; then
    rm -rf atrack_tmp/;
    install_atrack_rpm
else  fail_install;
fi

exit
