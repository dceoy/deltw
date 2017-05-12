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
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet'
    ],
    long_description="""\
deltw
-----

Tweet cleaner to delete archived tweets in [Twitter Archive](https://support.twitter.com/articles/20170160) from Twitter

Twitter API: v1.1

This version requires Python 3 or later.
    """
)
