<img src="https://user-images.githubusercontent.com/70149795/107785177-45a5c080-6d1a-11eb-9daa-31b405e706b1.png" style="width: 150px" />

# [Reviewington](https://homexlabs.github.io/reviewington/)

## Usage

Run the program locally using following `Flask` command in the root of the repo:

```
FLASK_APP=reviewington.app FLASK_DEBUG=1 python3 -m flask run
```

Run locally using `pip` installable pacakge:

1. Locate the root of the repo (on the same level as where `setup.py` is located).

2. Run below command. You will notice `dist` directory being created.

```
python3 setup.py bdist_wheel
```

3. Run below command to install your package locally

```
pip3 install dist/<YOU_PACKAGE_NAME>

e.g.
pip3 install dist/reviewington-0.0.1-py3-none-any.whl
```

4. You can run any `rton` commands

Examples:

```
rton run HomeXLabs/reviewington
rton configure
rton about
```

### Writing PRs

To get the most out of Reviewington you should write PR's that follow our recommended [PR Comment Etiquette](/docs/pr_etiquette.md).

If you want a PR comment to be ignored by Reviewington you can prepend it with the custom tag `NA:`, this ensures that the PR comment will not be picked up while processing.
This is different from having a non-existent tag, which will still be picked up by Reviewington but with the default PR tag of `null`.

## Development Environment

```
python -m virtualenv venv
venv/bin/pip install pip-tools
venv/bin/python -m piptools compile
venv/bin/python -m piptools sync
```

## Contributing

Development on the latest version of Python is preferred. As of this writing we are using `python 3.9`.
You can use any operating system, however the development team uses MacOS so there might be some slight differences to get setup.

Make sure you do all the development work in a virtual environment setup using:

```console
python -m virtualenv venv
venv/bin/pip install -r requirements.txt
```

Before submitting pull requests, run lints and tests with the following commands from the root of the reviewington repo:

```console
# Linting using black
black .

# Unit tests
venv/bin/python -m unittest
```

## Reviewington on Private Repo

Get an Github Personal Access Token from https://github.com/settings/tokens/new
and make sure that it has "repo" scope selected.

Make sure you copy the token so that you can use it when you configure reviewington with `rton configure`.

## PyPi deployment

To deploy run the following commands to upload a build distribution to pypi. Use `__token__` for a username and use your own PyPi API token as a password.

```
python3 -m pip install --user --upgrade twine
python3 setup.py bdist_wheel
python3 -m twine upload --repository testpypi dist/*
```
