"""Setup file.

 _____     _ _____ _____ _____
|  |  |___| |     |     |   __|
|     | . | | | | |  |  |__   |
|__|__|___|_|_|_|_|_____|_____|

This is the setup file. It allows you to create packages.

"""
from distutils.core import setup
from setuptools import find_packages

setup(name='holoview',
      version='0.0.3',
      description='Holographic Image Viewer',
      author='Christoph Stelz',
      author_email='mail@ch-st.de',
      url='https://github.com/stelzch/holmos',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Education',
          'Environment :: X11 Applications :: GTK',
          'License :: OSI Approved :: MIT License',
          'Topic :: Scientific/Engineering',
          'Programming Language :: Python :: 3'
      ],
      keywords='holography open science',
      packages=find_packages(),
      install_requires=[],
      include_package_data=True,
      package_data={
      },
      data_files=[
          ('share/applications', ['data/holoview.desktop'])
      ],
      entry_points={
          'console_scripts': [
              'holoview=holoview:main'
          ]
      })
