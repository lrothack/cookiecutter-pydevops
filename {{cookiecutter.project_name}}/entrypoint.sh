#!/bin/bash
#
# Docker ENTRYPOINT for starting your Python application
# 
# This script is used in Dockerfile
#  - script is copied to defined location in deployment container (2nd stage)
#  - script is registered as an ENTRYPOINT
#  - the ENTRYPOINT environment variable (used below) is defined in Dockerfile
#  - the value of the ENTRYPOINT environment variable is obtained in Makefile
#    and passed to Dockerfile as build-arg
#
# You can just use this script if
#  - your executable has the same name as your Python package, i.e., the 'name'
#    defined in setup.cfg/setup.py
#  - your executable is available on the PATH (standard if you define/register
#    your executable in setup.cfg/setup.py as 'entry_point' or 'script')
#
# ENTRYPOINT environment variable contains the name of the executable
# and is expected to be on the PATH
#
# $@ forwards all command-line arguments from this script to the 
# entry point executable

$ENTRYPOINT $@

# Feel free to replace the execution of the Python application above 
# (executed within the Docker container) 
# with your own code that matches your requirements.
#
# If you want to use your own entry point script, modify Dockerfile such that
#  - all references to this entrypoint.sh script are removed
#    (COPY, chown, ENTRYPOINT)
#  - you replace ENTRYPOINT (and CMD) with your own definitions 
# Afterwards, you can safely remove this script