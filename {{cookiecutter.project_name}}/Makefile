# Comments: single '#' for ordinary comments, 
#           '## ' indicates text for 'help' target 
#
# Use only one statement per line and do not mix statements and comments on a
# single line in order to allow for automatic editing.

# ATTENTION: Running `make <target>` is only supported from the project directory
#

# --- Common ---
#
# Obtain paths based on MAKEFILE_LIST variable, since variable contents can
# change while reading the Makefile (depending on include etc.) perform 
# immediate evaluation with ':='
# Note that a single '=' is only evaluated when accessing the variable 
#
# Current working directory
CWD := "${CURDIR}"
# Relative path to Makefile (from current working directory)
MKFILE_PATH := $(lastword $(MAKEFILE_LIST))


# --- Python ---
#
# Define names of executables used in make targets (and variables)
PYTHON = python
PIP = pip
# Files required by setuptools (python setup.py, pip)
# Note that setuptools can only supports running from the project root
# --> SETUPTOOLSFILES must be present in the working directory
# Adjust the list when your configuration changes, e.g., you use additional
# files one of the files is not used anymore.
SETUPTOOLSFILES = setup.py requirements.txt
#
# Obtain Python package path, name and version
# Lazy variable evualtion (with a single '=') is used in order to evaluate
# variables only from inside make targets. This allows to check if SETUPTOOLSFILES
# are present *before* executing the shell commands. 
#
# Name of the application defined in setup.py
NAME=$(shell $(PYTHON) setup.py --name)
# Version of the application defined in setup.py
VERSION=$(shell $(PYTHON) setup.py --version)
# Name of the directory where application sources are located
PACKAGE=./$(NAME)
# Directory where unittests are located
TESTS=./tests


# --- Linting/Testing configuration ---
#
# Executables
PYTEST = pytest
COVERAGE = coverage
PYLINT = pylint
BANDIT = bandit
# Directory where to save linting and testing reports
REPDIR=./.codereports
# Report result files
PYTESTREP=$(REPDIR)/pytest.xml
COVERAGEREP=$(REPDIR)/coverage.xml
PYLINTREP=$(REPDIR)/pylint.txt
BANDITREP=$(REPDIR)/bandit.json


# --- Docker configuration ---
#
# Docker executable
DOCKER = docker
# Name of the executable that is to be run in the Docker entry point script
# (entrypoint.sh). It is expected that there exists an executable
# called $DOCKERENTRYPOINTEXEC in the PATH of the Docker container. 
DOCKERENTRYPOINTEXEC=$(NAME)
# Files required to build a docker image for the Python project
DOCKERFILES = Dockerfile entrypoint.sh


# --- SonarQube client configuration ---
#
# Authentication token variable
SONARTOKEN=
# Authentication token file
# (will be read if file exists and SONARTOKEN variable is not defined)
SONARTOKENFILE=.sonartoken
ifndef SONARTOKEN
ifneq (,$(wildcard $(SONARTOKENFILE)))
SONARTOKEN=$(strip $(shell cat $(SONARTOKENFILE)))
endif
endif
# Report to sonar URL
SONARURL=http://sonarqube:9000
# DISABLE/enable whether to include SCM (git) meta info in sonarqube report
SONARNOSCM=False
# Connect sonar-scanner Docker container to Docker network
DOCKERNET=sonarqube_net
# Docker command for running sonar-scanner container
# make sure to allocate at least 4GB RAM in the Docker resource config
# if SonarQube server and SonarScanner are running simultaneously
SONARSCANNER=$(DOCKER) run \
    --network=$(DOCKERNET) \
    --rm -v $(CWD):/usr/src \
    sonarsource/sonar-scanner-cli:4.6
#
# Local sonar-scanner installation
#
# Report to sonar URL
# SONARURL=http://localhost:9000
# Path to executable or name of executable if on PATH
# SONARSCANNER=sonar-scanner


# --- Common targets ---

.PHONY: help clean clean-all dist install-dev test lint sonar docker-build docker-tag

## 
## MAKEFILE for building and testing Python package including
## code analysis and reporting to SonarQube in a dockerized build environment
## 
## ATTENTION: Running `make <target>` is only supported from the project directory
## 
## Targets:
## 

## help:         Print this comment-generated help message
# reads contents of this file and expects that this file is called 'Makefile'
help: $(MKFILE_PATH)
	@sed -n 's/^## //p' $(MKFILE_PATH)

## clean:        Clean up auto-generated files
clean:
	@rm -f $(PYTESTREP) $(COVERAGEREP)
	@rm -f $(PYLINTREP) $(BANDITREP)

## clean-all:    Clean up auto-generated files and directories
##               (WARNING: do not store user data in auto-generated directories)
clean-all: clean
	@rm -rf .coverage .scannerwork
	@rm -rf .pytest_cache
	@rm -rf ./$(REPDIR)
	@rm -rf ./$(NAME).egg-info
	@rm -rf ./$(PACKAGE)/$(NAME).egg-info
	@rm -rf build
	@rm -rf dist


# --- Python targets ---

# Check if project files exist in current working directory, otherwise stop.
$(PACKAGE):
	$(error "Python project files missing in working directory ($@)")
# Check if test files exist in current working directory, otherwise stop.
$(TESTS):
	$(error "Python test files missing in working directory ($@)")
# Check if setuptools files exist in current working directory, otherwise stop.
$(SETUPTOOLSFILES):
	$(error "Python packaging files missing in working directory ($@)")

## dist:         Build a Python wheel with setuptools (based on setup.py)
dist: $(SETUPTOOLSFILES)
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel

## install-dev:  Install development dependencies (based on setup.py)
##               (installation within a Python virtual environment is
##                recommended)
##               (application sources will be symlinked to PYTHONPATH)
install-dev: $(SETUPTOOLSFILES)
	$(PIP) install wheel
	$(PIP) install -e .[dev]

## test:         Run Python unit tests with pytest and analyse coverage
# check SETUPTOOLSFILES since setuptools is used to generate the PACKAGE name
test: $(SETUPTOOLSFILES) $(PACKAGE) $(TESTS)
	@echo "\n\nUnit Tests\n----------\n"
	$(COVERAGE) run --source $(PACKAGE) -m $(PYTEST) $(TESTS)
	@echo "\n\nUnit Test Code Coverage\n-----------------------\n"
	$(COVERAGE) report -m

## lint:         Run Python linter (bandit, pylint) and print output to terminal
# check SETUPTOOLSFILES since setuptools is used to generate the PACKAGE name
lint: $(SETUPTOOLSFILES) $(PACKAGE)
	@echo "\n\nBandit Vulnerabilities\n----------------------\n"
	-$(BANDIT) -r $(PACKAGE)
	@echo "\n\nPylint Code Analysis\n--------------------\n"
	$(PYLINT) --output-format=colorized --reports=n --exit-zero $(PACKAGE)


# --- SonarQube targets ---

## sonar:        Report code analysis and test coverage results to SonarQube
##               (requires SonarQube server, to run server in Docker:
##                `docker-compose -p sonarqube \
##                                -f sonarqube/docker-compose.yml up -d`)
#                (requires code analysis dependencies, 
#                 intall with `make install-dev`
#                 ATTENTION: make sure to allocate at least 4GB RAM in the 
#                 Docker resource configuration when running sonar server 
#                 and sonar scanner containers simulataneously)
# leading dash (in front of commands, not parameters) ignores error codes,
# `make` would fail if test case fails or linter reports infos/warnings/errors.
# check SETUPTOOLSFILES since setuptools is used to generate PACKAGE / NAME
sonar: $(SETUPTOOLSFILES) $(PACKAGE) $(TESTS)
	@mkdir -p $(REPDIR)
	-$(BANDIT) -r $(PACKAGE) --format json >$(BANDITREP)
	$(PYLINT) $(PACKAGE) --exit-zero --reports=n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > $(PYLINTREP)
	-$(COVERAGE) run --source $(PACKAGE) -m $(PYTEST) --junit-xml=$(PYTESTREP) -o junit_family=xunit2 $(TESTS)
	$(COVERAGE) xml -o $(COVERAGEREP)
	$(SONARSCANNER) -Dsonar.host.url=$(SONARURL) \
              -Dsonar.login=$(SONARTOKEN) \
              -Dsonar.projectKey=$(NAME) \
              -Dsonar.projectVersion=$(VERSION) \
              -Dsonar.sourceEncoding=UTF-8 \
              -Dsonar.sources=$(PACKAGE) \
              -Dsonar.tests=$(TESTS) \
              -Dsonar.scm.disabled=$(SONARNOSCM) \
              -Dsonar.python.xunit.reportPath=$(PYTESTREP) \
              -Dsonar.python.coverage.reportPaths=$(COVERAGEREP) \
              -Dsonar.python.pylint.reportPaths=$(PYLINTREP) \
              -Dsonar.python.bandit.reportPaths=$(BANDITREP)


# --- Docker targets ---

## docker-build: Build docker image for Python application with code analysis
# Note: info is parsed and immediately printed by make, echo is executed in a
# shell as are the other commands in the recipe.
# check SETUPTOOLSFILES since setuptools is used to generate the package NAME
docker-build: $(SETUPTOOLSFILES) $(DOCKERFILES)
	$(info Running Docker build in context: ./ )
	$(info ENTRYPOINT executable: $(DOCKERENTRYPOINTEXEC))
	$(eval REPORTFILE:=code-analyses.txt)
	$(DOCKER) build --rm -t $(NAME) ./ \
		--build-arg REPORTFILE=$(REPORTFILE) \
		--build-arg ENTRYPOINT=$(DOCKERENTRYPOINTEXEC)
	@echo "\n### CODE ANALYSIS REPORT ###\n"
	$(DOCKER) run -it --entrypoint="more" --rm $(NAME) $(REPORTFILE)
	@echo "\n\nbuild finished, run the container with \`docker run --rm $(NAME)\`"

## docker-tag:   Tag the 'latest' image created with `make docker-build` with
##               the current version that is defined in setup.cfg/setup.py
# check SETUPTOOLSFILES since setuptools is used to generate NAME and VERSION
docker-tag: $(SETUPTOOLSFILES)
	$(DOCKER) tag $(NAME) $(NAME):$(VERSION)