import os
from setuptools import setup, find_packages

## run setup from all directories
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

## get package version
from pyprika import __version__

## fetch readme contents
README = open('README.rst').read()

setup(
  name='pyprika',
  version=__version__,
  packages=['pyprika', 'pyprika.tests'],
  description='A recipe management library',
  long_description=README,
  url='https://github.com/OEP/pyprika',
  author='Paul Kilgo',
  author_email='paulkilgo@gmail.com',
  classifiers=[
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
  ],
  entry_points={
    'console_scripts': [
      'kit = pyprika.commands:main',
    ],
  },
  install_requires=[
    'PyYAML >= 3.10',  
  ],
)
