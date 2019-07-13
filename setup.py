#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Adil Zouitine <adilzouitinegm@gmail.com
"""

from setuptools import setup, find_packages
import outfit

setup(name='outfit',
      version=outfit.__version__,
      description='Tidy up your machine learning experiments',
      url='https://github.com/AdilZouitine/Outfit',
      author='Adil Zouitine',
      author_email='adilzouitine@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)