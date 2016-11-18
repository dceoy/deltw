#!/usr/bin/env python

from setuptools import setup, find_packages
from deltw import __version__


setup(
    name='deltw',
    version=__version__,
    packages=find_packages(),
    description='Tweet Cleaner using Twitter Archive',
    author='Daichi Narushima',
    author_email='d.narsil@gmail.com',
    url='https://github.com/dceoy/deltw',
    install_requires=[
        'pyyaml',
        'requests_oauthlib'
    ],
    entry_points={
        'console_scripts': ['deltw=deltw.cli:main'],
    }
)
