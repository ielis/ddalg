from setuptools import setup, find_packages

import ddalg

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(name='ddalg',
      version=ddalg.__version__,
      author='Daniel Danis',
      author_email='daniel.gordon.danis@gmail.com',
      description='Algorithms and data structures for my Python projects',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ielis/ddalg',
      packages=find_packages(),
      python_requires='>=3.6',
      setup_requires=['coverage>=5.0.4'],
      install_requires=['numpy>=1.18.2'],

      license='GPLv3',
      keywords='algorithms python')
