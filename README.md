# Premier Geek

### An AI-powered Premier League squad intelligence.

Unlock instant access to Premier League talent insights through natural language queries. The technology delivers precise player profiles, including names, positions, and birthdays, boosting team analysis and scouting processes.


## Getting Started
These instructions will get you a ready-to-use development environment.

### Backend

#### Prerequisites
- Install the latest version of [Python 3.12](https://www.python.org/downloads/).
- Install the latest version of [poetry 1.8](https://python-poetry.org/docs/#installation).
- set backend environment variables specified in [.env.template](.env.template).

#### Set up a Python environment
You can set up the environment and install the required dependencies by running the command below:
```shell
poetry install
```

#### Run tests
The tests are based on [pytest](https://docs.pytest.org/) so running them boils down to executing a single command:
```shell
poetry run pytest
```

#### Run the Local Server
After setting up the environment, you can run the API. The project uses Uvicorn, an ASGI server, to run the application in the development mode. To start the server on your localhost at port 8000, use the following command:

```shell
poetry run uvicorn premier_geek.api.runtime.main:app --reload
```

When you have the server running, you can access swagger documentation under http://localhost:8000/docs

### Frontend

#### Prerequisites
- Install the latest version of [Node 18](https://nodejs.org/en/download/).
- set frontend environment variables specified in [.env.template](.env.template).

#### Set up node environment
You can set up the environment and install the required dependencies by running the commands below:
```shell
cd premier_geek/website/runtime
npm install
```

#### Run the Local Server
After setting up the environment, you can run the Website at localhost port 3000 by executing:

```shell
npm start
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

## Deployment
These instructions will allow you to deploy the app to AWS.

### Prerequisites
- Install the latest version of [aws-cli v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and [set up credentials](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html). If you don't have the keys, follow [the documentation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html).
- Install the latest version of [aws cdk v2](https://www.npmjs.com/package/aws-cdk) using [node](https://nodejs.org/en/download/):
```shell
npm install -g aws-cdk
```

### Deploy
Deployment is as simple as running `cdk deploy pocPremierGeek`.
