"""Top-level import package for {{cookiecutter.project_slug}}"""
from {{cookiecutter.project_slug}}.log import LoggerConfig


# Package meta information
__version__ = '{{cookiecutter.project_version}}'
# Logger configuration can be accessed through global variable LOGCONFIG
LOGCONFIG = LoggerConfig()