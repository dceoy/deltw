#!/usr/bin/env python

from setuptools import find_packages, setup

from deltw import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='deltw',
    version=__version__,
    author='Daichi Narushima',
    author_email='dnarsil+github@gmail.com',
    description='Twitter Cleaner to delete archived tweets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dceoy/deltw',
    packages=find_packages(),
    install_requires=['requests_oauthlib', 'pyyaml'],
    entry_points={'console_scripts': ['deltw=deltw.cli:main']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Topic :: Internet'
    ],
    python_requires='>=3.5'
)
