#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Setup script for the package. """
from setuptools import find_packages, setup

from strcolors import __author__, __email__, __license__, __package__, __version__

setup(
    name=__package__,
    version=__version__,
    description='Python module to handle terminal capabilities.',
    author=__author__,
    url=f'https://github.com/{__author__}/{__package__}',
    packages=find_packages(),
    license=__license__,
    author_email=__email__,
    include_package_data=True,
    data_files=[('', ['LICENSE', 'README.md'])],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: POSIX',
        'Topic :: Terminals',
        'Environment :: Console'
    ],
    python_requires='>=3.6'
)
