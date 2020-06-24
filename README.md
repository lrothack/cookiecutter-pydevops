# Cookiecutter PyDevops

[Cookiecutter template](https://github.com/audreyr/cookiecutter) for a dockerized dev-ops pipeline with SonarQube code-quality monitoring.

- [Sample project](https://github.com/lrothack/dev-ops) for this cookiecutter (including
	detailed documentation)
- This cookiecutter has been generated with the command-line client [devopstemplate](https://github.com/lrothack/dev-ops-admin)
- Also check out [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) for additional Python package templates

## Features

The template provides a minimal dev-ops pipeline that supports:

- testing and deployment in a multi-stage [Docker](https://www.docker.com) environment
- packaging with [setuptools](https://setuptools.readthedocs.io/en/latest/)
- code analysis with [pylint](https://www.pylint.org/), [bandit](https://bandit.readthedocs.io/en/latest/), [pytest](https://docs.pytest.org/en/stable/) and [coverage](https://coverage.readthedocs.io/en/latest/)
- code quality monitoring with [SonarQube](https://www.sonarqube.org)

The dev-ops pipeline is mostly implemented in a `Makefile` and a `Dockerfile` which are
independent of your Python code.

## Quickstart

Install the latest cookiecutter:

```bash
pip install -U cookiecutter
```

Generate an instance of the template:

```bash
cookiecutter https://github.com/lrothack/cookiecutter-pydevops.git
```

Then switch to the project directory and:

- Set up a virtual environment for your project and activate it (requires Python >= 3.6).
- Run `make help` in order to get an overview of the targets provided by `Makefile`.
- Run `make install-dev` in order to install the package (and all dependencies) in development
	mode.
- Run `make lint` in order to run code analysis with pylint and bandit.
- Run `make test` in order to run unit tests with pytest and coverage.
- Run `make dist` in order to build a Python package (binary and source).
- Run `docker-compose -p sonarqube -f sonarqube/docker-compose.yml up -d` in order to start a SonarQube server.
- Run `make sonar` in order to locally run `sonar-scanner` and report results to your local
	SonarQube server. Requires a local installation of [sonar-scanner](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/).
- Run `make docker-build` in order to analyze, test, package, report to SonarQube and deploy in a multi-stage Docker
	build. Test your docker image with `docker run`.

Advanced configurations can be made in the *configuration* sections of `Makefile`. See [lrothack/dev-ops](https://github.com/lrothack/dev-ops) for more information.
