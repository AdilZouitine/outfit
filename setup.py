from setuptools import find_packages, setup

import outfit

# base_packages = ['peewee>=3.9.6', 'pandas>=0.24.2','tabulate>=0.8.3']

setup(name='outfit',
      version=outfit.__version__,
      description='Tidy up your machine learning experiments',
      url='https://github.com/AdilZouitine/Outfit',
      author='Adil Zouitine',
      author_email='adilzouitine@gmail.com',
      license='MIT',
      packages=find_packages(),
      # install_requires=base_packages,
      include_package_data=True,
      zip_safe=False)
