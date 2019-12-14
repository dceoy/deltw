#!/usr/bin/env python

from setuptools import find_packages, setup

from deltw import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='deltw',
    version=__version__,
    description='Twitter Cleaner to delete archived tweets',
    packages=find_packages(),
    author='Daichi Narushima',
    author_email='dnarsil+github@gmail.com',
    url='https://github.com/dceoy/deltw',
    install_requires=[
        'requests_oauthlib', 'pyyaml'
    ],
    entry_points={
        'console_scripts': ['deltw=deltw.main:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet'
    ],
    python_requires='>=3.6',
    long_description=long_description
)
