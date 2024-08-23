# Premier Geek

### An AI-powered Premier League squad intelligence.

Unlock instant access to Premier League talent insights through natural language queries. The technology delivers precise player profiles, including names, positions, and birthdays, boosting team analysis and scouting processes.


## Getting Started
These instructions will get you a ready-to-use development environment.

### Prerequisites
- Install the latest version of [Python 3.12](https://www.python.org/downloads/).
- Install the latest version of [poetry 1.8](https://python-poetry.org/docs/#installation).

### Set up a Python environment
You can set up the environment and install the required dependencies by running the command below:
```shell
poetry install
```

### Run tests
The tests are based on [pytest](https://docs.pytest.org/) so running them boils down to executing a single command:
```shell
poetry run pytest
```


### Before you commit
We use [pre-commit](https://pre-commit.com) alongside [pyright](https://github.com/microsoft/pyright) to maintain the high quality of our codebase. Pre-commit runs a series of checks when you try to commit, either accepting or denying your changes. It may also automatically fix some obvious issues. Pyright ensure there are no issues related to typing.

#### Setting up Pre-commit
You need to install pre-commit only once per poetry environment using the following command. After that, it will automatically run before every commit.
```shell
poetry run pre-commit install
```

#### Running pyright
Due to its strong relation to the installed dependencies and a relatively long time to execute, pyright is not automatically run after each commit by pre-commit. You may want to run it manually as shown below or incorporate it into a CI/CD pipeline.
```shell
poetry run pyright
```
