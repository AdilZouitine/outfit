import io
import os
from setuptools import find_packages, setup

# metadata
NAME = 'outfit'
VERSION = '0.0.2'
DESCRIPTION = 'Tidy up your machine learning experiments'
URL = 'https://github.com/AdilZouitine/Outfit'
AUTHOR = 'Adil Zouitine'
AUTHOR_MAIL = 'adilzouitine@gmail.com'
LICENSE = 'BSD-3'
REQUIRES_PYTHON = '>=3.5.0'

base_packages = ['peewee>=3.9.6', 'pandas>=0.24.2', 'tabulate>=0.8.3']

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_MAIL,
    license=LICENSE,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    install_requires=base_packages,
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    include_package_data=True,
    zip_safe=False)
