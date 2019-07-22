from setuptools import find_packages, setup

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
