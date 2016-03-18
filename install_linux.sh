#!/bin/sh

# A-Track installer for GNU/Linux System
# Authors: Yücel Kılıç, Murat Kaplan, Nurdan Karapınar, Tolga Atay.
# This is an open-source software licensed under GPLv3.

# Variables to use

DEPS_deb="python3 python3-dev python3-pip python3-numpy 
python3-scipy python3-pil imagemagick libxt-dev git sextractor 
build-essential
"

DEPS_rpm="python3 python3-devel python3-pip python3-numpy 
python3-scipy python3-pillow ImageMagick libXt-devel git 
sextractor make automake gcc gcc-c++ 
kernel-devel
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
atrack_dep_deb(){
   echo ''
   echo '      Installing dependencies for A-Track.' 
   echo '      (Be patient...)'
   echo ''
   apt-get update
   apt-get install --no-install-recommends -y $DEPS_deb
}

atrack_dep_rpm(){
   echo ''
   echo '      Installing dependencies (Be patient...)'
   echo ''
   yum -y install $DEPS_rpm
}

atrack_dep_pip(){
   echo ''
   echo '      Installing dependencies via pip3.'
   echo ''
   echo ''
   echo '      Installing pandas, numpy, pyfits, pyds9' 
   echo '      (Be patient...)'
   echo ''
   pip3 install --upgrade pandas pyfits
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

install_atrack_deb(){
    atrack_dep_deb
    atrack_dep_pip
    atrack_post
}

install_atrack_rpm(){
    atrack_dep_rpm
    atrack_dep_pip
    atrack_post
}

fail_install(){
   echo ''
   echo 'Do you have the required GNU/Linux Distro?'
   echo '(Fedora, Ubuntu, Debian, LinuxMint, CentOS, RedHat)'
   echo 'You need to install A-Track manually :('
   echo ''
}

# Check which distro we are using and run the appropriate script.

distro=$(cat /etc/issue| head -n1| awk '{print $1}')
# LinuxMint => Linux

if [ $distro = "Debian" -o $distro = "Ubuntu" -o $distro = "Linux" ]; then
    echo ''
    echo 'The following extra packages will be installed for A-Track;'
    echo 'pandas, numpy, pyfits, alipy, astroasciidata, pyds9'
    echo $DEPS_deb
    echo ''
    read -r -p "Do you want to proceed? [y/N] " response
    case $response in
	[yY][eE][sS]|[yY])
	    rm -rf atrack_tmp/;
	    install_atrack_deb;
	    ;;
	*)
	    exit 1
	    ;;
    esac
elif [ $distro = "Fedora" -o $distro = "CentOS" ]; then
    echo ''
    echo 'The following extra packages will be installed for A-Track;'
    echo 'pandas, numpy, pyfits, alipy, astroasciidata, pyds9'
    echo $DEPS_rpm
    echo ''
    read -r -p "Do you want to proceed? [y/N] " response
    case $response in
	[yY][eE][sS]|[yY])
	    rm -rf atrack_tmp/;
	    install_atrack_rpm;
	    ;;
	*)
	    exit 1
	    ;;
    esac
else  fail_install;
fi

exit
