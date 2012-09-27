import os
from setuptools import setup, find_packages

README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = 'Command line client for making API calls.'

import bsdapi

setup(
    name='bsdapi',
    version=bsdapi.__version__,
    description=long_description,
    author='Scott Frazer',
    author_email='sfrazer@bluestatedigital.com',
    packages=['bsdapi'],
    package_dir={'bsdapi': 'bsdapi'},
    entry_points={
      'console_scripts': [
            'bsdapi = bsdapi.Main:Cli'
        ]
      },
    license = "GPL",
    keywords = "API, Client, HTTP",
    url = "http://bluestatedigital.com/",
    classifiers=[
          "Programming Language :: Python",
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Natural Language :: English",
      ]
    )
