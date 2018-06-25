#!/usr/bin/env python

from setuptools import setup, find_packages
from deltw import __version__


setup(
    name='deltw',
    version=__version__,
    description='Twitter Cleaner to delete archived tweets',
    packages=find_packages(),
    author='Daichi Narushima',
    author_email='dnarsil+github@gmail.com',
    url='https://github.com/dceoy/deltw',
    install_requires=[
        'requests_oauthlib',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': ['deltw=deltw.main:main'],
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

Twitter cleaner to delete archived tweets on Twitter using
a [Twitter Archive](https://support.twitter.com/articles/20170160) file

Twitter API: v1.1
    """
)
