# SEA

Software Engineering Agile Assignment

# SETTING UP THE APPLICATION

## Pre-requisites for local deployment

Have python installed
Have docker installed

## Setting up venv

```
python -m venv venv
```

after this step you will need to select the venv as your python interpreter (cmd + shift + p -> select python interpreter -> venv)

```
source venv/Scripts/activate
pip install -r requirements.txt
```

## Creating docker image

```
docker build -t sea-flask-app-local:latest .
docker run -p 5000:5000 sea-flask-app-local
```

# TO RUN TESTS

```
cd backend
```

## Logic tests -

```
python -m tests.test_logic
```

## Route tests -

```
pytest
```

