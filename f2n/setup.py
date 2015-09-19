#!/usr/bin/env python

from distutils.core import setup

setup(
	name='f2n',
	version='1.2dev',
	packages=['f2n'],
	package_data = {'f2n':['f2n_fonts/*.*']},
	description='f2n',
	long_description=open('README.txt').read(),
	author='Malte Tewes',
	license='GPLv3',
	author_email='malte.tewes[at]epfl.ch',
	url='http://obswww.unige.ch/~tewes/f2n_dot_py/'
)


#data_files=[('f2n_fonts', ['f2n_fonts/courR08.pbm', 'f2n_fonts/courR10.pil', 'f2n_fonts/courR10.pbm', 'f2n_fonts/courR08.pil', 'f2n_fonts/courR12.pbm', 'f2n_fonts/courR12.pil', 'f2n_fonts/courR18.pbm', 'f2n_fonts/courR18.pil', 'f2n_fonts/README.txt'])]  

#package_dir = {'f2n_fonts': 'f2n_fonts'},
#package_data = {'f2n_fonts':['f2n_fonts/*.*']},	

# data_files=[('f2n_fonts', ['f2n_fonts/courR08.pbm', 'f2n_fonts/courR10.pil', 'f2n_fonts/courR10.pbm', 'f2n_fonts/courR08.pil', 'f2n_fonts/courR12.pbm', 'f2n_fonts/courR12.pil', 'f2n_fonts/courR18.pbm', 'f2n_fonts/courR18.pil', 'f2n_fonts/README.txt'])]  


#recursive-include f2n_fonts *.pbm *.pil *.txt
#recursive-include demo_scripts *.py *.fits *.cat
