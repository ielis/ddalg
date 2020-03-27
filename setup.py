import io

from setuptools import setup, find_packages

import ddalg

setup(name='ddalg',
      version=ddalg.__version__,
      packages=find_packages(),
      setup_requires=['coverage>=5.0.4'],
      install_requires=['numpy>=1.18.2'],

      long_description=io.open('README.md', encoding='utf-8').read(),
      long_description_content_type='text/markdown',

      author='Daniel Danis',
      author_email='daniel.gordon.danis@gmail.com',
      url='https://github.com/ielis/ddalg',
      description='Algorithms and data structures for my Python projects',
      license='GPLv3',
      keywords='algorithms python')
