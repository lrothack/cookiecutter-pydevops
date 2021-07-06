# SonarQube Code Quality Monitoring

SonarQube server as well as SonarScanner run within Docker containers by default. Make sure to allocate at least 4GB RAM in the Docker resource configuration.
Start SonarQube server in a Docker container and report Python code analyses:

1. Start SonarQube server:

    ```bash
    docker-compose -p sonarqube -f sonarqube/docker-compose.yml up -d
    ```

2. Login at `http://localhost:9000`, set a new password and generate/copy an authentication token (*Administration - Users*).

3. Update `SONARTOKEN` variable in [`Makefile`](../Makefile) with the token generated before.

4. Generate and send report:

   ```bash
   make clean && make sonar
   ```

Below you will find a detailed description on how to use [SonarQube with Docker](https://hub.docker.com/_/sonarqube/) and report Python code quality with `sonar-scanner`.

## Setting up SonarQube server with PostgreSQL

1. Multiple docker containers can be run with `docker-compose` (current working directory: `./sonarqube`):

   ```bash
   docker-compose up -d
   ```

   Notes:
    - `-d` run in background
    - [docker-compose.yml (see comments)](docker-compose.yml) defines services, networks and volumes
    - `docker-compose` auto-generates names for containers (based on services), networks and volumes by prefixing each name from the [docker-compose.yml](docker-compose.yml) with `projectname_` where `projectname` defaults to the name of the current directory. The project name can be specified with command-line parameter `-p`, e.g., `docker-compose -p project up -d` or with environment variable `COMPOSE_PROJECT_NAME`, [see docker reference](https://docs.docker.com/compose/reference/envvars/#compose_project_name).
    - Since we are only interested in preserving analysis data for projects, it is sufficient to use a single docker volume for postgresql data (`db_data`). The contents of all other directories, which might be worth preserving according to the [SonarQube documentation on Docker Hub](https://hub.docker.com/_/sonarqube/), are not modified.
    - **Attention:** database credentials are specified over the command-line. This is insecure. For example, the credentials will be visible to any user by calling `top`, try `docker-compose top`.
2. Access SonarQube at `http://localhost:9000` and login as *admin*/*admin*
3. Generate a new password for the *admin* user. Go to *Administration - Security - Users* in order to create additional users as needed.
4. Go to *Administration - Security - Users* and click *Update Tokens* in the *Tokens* column for a chosen user in order to generate an **authentication token**. Copy the token and update the variable `SONARTOKEN` in [`Makefile`](../Makefile) for automatic code quality reporting with `sonar-scanner` (see below).
5. There is no need to manually create a project in the web interface as it can be created automatically by publishing analysis reports (see below).
6. Stop and remove the containers with

   ```bash
   docker-compose -p sonarqube stop
   ```

## Generating reports with SonarScanner

SonarScanner is run within the [SonarScanner CLI Docker image](https://github.com/SonarSource/sonar-scanner-cli-docker) by default.

1. Setup a virtual environment and install the requirements:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Configure the SonarQube project with SonarScanner command-line arguments in the [Makefile](../Makefile) (see make target `sonar`). **Important:** Generate an authentication token in the Sonarqube web interface (log in as *admin* user and go to *Administration - Security - Users*). Copy the token and update the variable `SONARTOKEN` in [`Makefile`](../Makefile) (also see above).

3. Generate and send report:

   ```bash
   make clean && make sonar
   ```

   `make sonar` generates external reports (pytest, coverage, pylint, bandit) and runs `sonar-scanner` in a Docker container in order to transmit all reports to the SonarQube server at [http://localhost:9000](http://localhost:9000) (default).
   Notes:
    - SonarScanner reaches SonarQube at `http://sonarqube:9000` because it is running in the same Docker network (`sonarqube_net`) as the SonarQube server with hostname `sonarqube` (see [docker-compose.yml](docker-compose.yml)).
    - You can configure the SonarQube URL through the `Makefile` variable `SONARURL`.
    - [`pytest`](https://docs.pytest.org/en/stable/) runs unit tests, see `pytest -h`
    - [`coverage`](https://coverage.readthedocs.io/en/coverage-5.1/) analyzes test coverage, see `coverage -h`
    - [`pylint`](https://www.pylint.org) creates code analysis report with respect to [PEP8](https://www.python.org/dev/peps/pep-0008/) compliance.
      Messages have to follow a defined format, see [SonarQube documentation](https://docs.sonarqube.org/latest/analysis/languages/python/) (section Pylint) and `pylint -h`
    - [`bandit`](https://pypi.org/project/bandit/) analyses security issues in Python, SonarQube expects json report, also see `bandit -h`
    - [sonar-scanner](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/) is configured with command line flags according to:

      ```bash
      # Authentication
      sonar.login=<auth_token>
      # SonarQube URL
      sonar.host.url=http://sonarqube:9000
      # unique project identifier
      sonar.projectKey=sampleproject
      # project display name in web interface
      #sonar.projectName=sampleproject
      sonar.projectVersion=0.1
      # encoding
      sonar.sourceEncoding=UTF-8

      # source directory/package (must contain __init__.py)
      sonar.sources=sampleproject

      # unittests directory/package (must contain __init__.py)
      sonar.tests=tests
      # report for unittest results
      sonar.python.xunit.reportPath=.codereports/pytest.xml
      # report for unittest coverage
      sonar.python.coverage.reportPaths=.codereports/coverage.xml
      # linting
      sonar.python.pylint.reportPath=.codereports/pylint.txt
      sonar.python.bandit.reportPaths=.codereports/bandit.json
       ```

      The full documentation can be found [here](https://docs.sonarqube.org/latest/analysis/analysis-parameters/) and Python related settings can be found [here](https://docs.sonarqube.org/latest/analysis/coverage/).

4. Go to `http://localhost:9000`. The project has been created with default quality profiles, see *Project Settings*.
5. In the web interface, login as administrator and create a custom Python quality profile that inherits from the default Python profile. Add all rules available (except the rules tagged as deprecated) which results in 468 active rules and 34 inactive rules (the default Python profile has 101 active rules). Note that rules are updated in the SonarQube repositories, thus, the exact numbers will change.
6. Repeat step 4 and re-run `make sonar`. The project statistic in the web interface should have updated and report one bug for the failed unittest and 8 code smells for PEP8 violations.

You might want to have a look at the *Quality Gates* in the web interface that define conditions for determining whether your code meets the minimum quality standards. Note that SonarQube follows the [*clean as you code*](https://docs.sonarqube.org/latest/user-guide/clean-as-you-code/) principle, thus, quality gates are only applied on new code by default (there are settings for *overall code*).

Further configurations are described in the SonarQube [documentation](https://docs.sonarqube.org/latest/).

To deactivate the `venv` after testing the container run: `deactivate`.

## Generating reports with locally installed SonarScanner

1. Setup a virtual environment and install the requirements:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Install SonarScanner used for generating and sending reports:

    ```bash
    brew install sonar-scanner
    ```

3. Edit `Makefile` and uncomment `SONARURL` and `SONARSCANNER` below *Local sonar-scanner installation*. Set `SONARSCANNER=sonar-scanner` in order to use the SonarScanner installation that can be found on the `PATH`. Set `SONARURL=http://localhost:9000` such that `sonar-scanner` running locally (not within a Docker network) is able to reach SonarQube.

4. Continue from step 3 in [Generating reports with SonarScanner](#generating-reports-with-sonarscanner).

## Setting up SonarQube server with embedded database

1. Run the SonarQube Docker image (latest version):

   ```bash
   docker run -d --name sonarqube --stop-timeout 3600 -p 9000:9000 sonarqube
   ```

   Notes:
    - `-d` run in background
    - `--name` identifier of the container
    - `--stop-timeout` wait for 3600 seconds until forcing container to stop (see [SonarQube container documentation](https://hub.docker.com/_/sonarqube/), section *Avoid hard termination of SonarQube*)
    - `-p` port forwarding from container to Docker host

2. Access SonarQube at `http://localhost:9000` and login as *admin*.
3. Note the warning at the bottom of the page informing you that you are using an embedded database which is not suitable for production (only evaluation).
4. There is no need to manually create a project in the web interface as it can be created automatically by publishing analysis reports (see below).
5. Stop the container with

    ```bash
    docker stop sonarqube
    ```


