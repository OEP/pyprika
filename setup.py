import os
from setuptools import setup

# run setup from all directories
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# get __version__ and __author__
exec(open(os.path.join('pyprika', 'version.py')).read())

# fetch readme contents
README = open('README.rst').read()

setup(
    name='pyprika',
    version=__version__,  # noqa
    packages=['pyprika', 'pyprika.kit', 'pyprika.tests'],
    description='A recipe management library',
    long_description=README,
    url='https://github.com/OEP/pyprika',
    author=__author__,  # noqa
    author_email='paulkilgo@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
        'kit = pyprika.kit.main:main',
        ],
    },
    install_requires=[
        'PyYAML',
    ],
    test_suite='pyprika.tests',
)
