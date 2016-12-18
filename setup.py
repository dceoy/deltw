#!/usr/bin/env python

from setuptools import setup, find_packages
from deltw import __version__, __description__


setup(
    name='deltw',
    version=__version__,
    description=__description__,
    packages=find_packages(),
    author='Daichi Narushima',
    author_email='d.narsil@gmail.com',
    url='https://github.com/dceoy/deltw',
    install_requires=[
        'requests_oauthlib',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': ['deltw=deltw.cli:main'],
    }
)
