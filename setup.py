#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages
import alien

setup(
    name='alien',
    version=alien.__version__,
    description='An unofficial Reddit SDK for Python',
    url='https://github.com/labteral/alien',
    author='Rodrigo Martínez Castaño',
    author_email='rodrigo@martinez.gal',
    license='GNU General Public License v3 (GPLv3)',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[''])  # Dependencies
