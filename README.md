# Reviewington

## Usage

Run the program locally using `Flask` command:

`cd` into `reviewington` (inside `reviewington`) and run below command

```
FLASK_APP=app.py FLASK_DEBUG=1 python3 -m flask run
```

Run locally using `pip` installable pacakge:
1. locate to main directory (on the same level as where `setup.py` is located)

2. Run below command. You will notice `dist` directory being created.
```
python3 setup.py bdist_wheel
```
3. Run below command to install your package locally
```
pip3 install dist/<YOU_PACAKGE_NAME>

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
