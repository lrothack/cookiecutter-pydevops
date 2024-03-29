"""Setuptools package configuration file

The 'Makefile' triggers builds and uses setup.py/requirements.txt
Adapt the Makefile variable SETUPTOOLSFILES if dependencies change, e.g.,
you switch to using only setup.py and/or setup.cfg for defining your package.
"""
import os
import re
from setuptools import setup, find_packages


def parse_version(package_rpath):
    """Parse version number from __init__.py in top-level import package

    It is assumed that the version is defined as a string and the '=' sign
    is surrounded by at most one whitespace character to the left and to the
    right.

    Params:
        package_rpath: String with the relative path to the package
            (with respect to setup.py)
    Returns:
        version: String with the version number
    Raises:
        ValueError: if the parser could not match the version definition
    """
    init_fpath = os.path.join(package_rpath, '__init__.py')
    with open(init_fpath, 'r', encoding='utf-8') as handle:
        init_contents = handle.read()
        ver_re = r"^__version__ ?= ?['\"]([^'\"]*)['\"]"
        match = re.search(ver_re, init_contents, re.M)
        if match:
            version = match.group(1)
            return version
        raise ValueError('Could not parse version string')


def read_file(filepath):
    """Read file as text

    Params:
        filename: relative/absolute path to the file
    Returns:
        contents as str
    """
    with open(filepath, 'r', encoding='utf-8') as handle:
        return handle.read()


# Name of the top-level import package (directory)
PKG_NAME = '{{cookiecutter.project_slug}}'

# Parse version
VERSION = parse_version(PKG_NAME)

# Read Readme that will be used as long package description
DESCRIPTION_LONG = read_file('README.md')

# Read list of Python package dependencies
INSTALL_REQUIRES = read_file('requirements.txt').splitlines()

# ATTENTION: the name must match the name of the top-level import package
# see Makefile variable PACKAGE.
# Naming the project as the top-level import package is also consistent with
# conventions.
setup(name=PKG_NAME,
      # The version string will be included in your Python package
      # https://setuptools.readthedocs.io/en/latest/setuptools.html#specifying-your-project-s-version
      version=VERSION,
      python_requires='>= 3.8',
      # Define the package sources.
      packages=find_packages(include=[PKG_NAME, f'{PKG_NAME}.*']),
      # Package dependencies
      install_requires=INSTALL_REQUIRES,
      # Defines dev environment containing development dependencies
      # (for linting, testing, etc.)
      extras_require={'dev': ['pip >= 20.1.1',
                              'wheel',
                              'pytest',
                              'pytest-mock',
                              'coverage',
                              'bandit',
                              'pylint',
                              'autopep8',
                              'flake8']
                      },
      # Include scripts/executables for application from 'scripts' directory
      # Executables will be included in the PATH search directory of the Python
      # environment, e.g., a virtual environment or /usr/local/bin
      # scripts=['scripts/samplescript'],
      # Generate entry points (executables) automatically from Python functions
      #     executable = package.module:function
      # Executables will be included in the PATH search directory of the Python
      # environment, e.g., a virtual environment or /usr/local/bin
      entry_points={
          'console_scripts': [
              f'{PKG_NAME}={PKG_NAME}.main:main',
          ],
      },
      # Data files should always be part of the package and you should avoid
      # dependencies to data files outside of the package.
      # find_packages (see above) searches Python packages and includes source
      # files. In order to include data files, too, you can use
      # include_package_data OR package_data
      # Note that package_data will not work when include_package_data=True
      # With include_package_data you must manage your data file includes in
      # MANIFEST.in. With package_data you manage data file includes relative
      # to package key provided in the dictionary.
      # https://setuptools.readthedocs.io/en/latest/setuptools.html#including-data-files
      # include_package_data = True,
      # package_data={
      #     # If any package contains *.txt or *.rst files, include them:
      #     '': ['*.txt', '*.rst'],
      #     # And include any *.msg files found in the 'hello' package, too:
      #     'hello': '*.msg'
      # },
      # Generally do not assume that the package can safely be run as a zip
      # archive
      zip_safe=False,
      # Package meta information
      author='{{cookiecutter.author_name}}',
      author_email='{{cookiecutter.author_email}}',
      description='{{cookiecutter.project_description}}',
      long_description=DESCRIPTION_LONG,
      long_description_content_type='text/markdown',
      # keywords = 'keyword1, keyword2, keyword3'
      url='{{cookiecutter.project_url}}',
      # project_urls={
      #     'Bug Tracker': 'https://bugs.example.com/HelloWorld/',
      #     'Documentation': 'https://docs.example.com/HelloWorld/',
      #     'Source Code': 'https://code.example.com/HelloWorld/'
      # },
      platforms='any',
      # license='MIT',
      # Define the intended audience of your Python package
      # For a full list of classifiers see: https://pypi.org/classifiers/
      classifiers=[
          'Intended Audience :: Developers',
          #   'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
      ]
      )