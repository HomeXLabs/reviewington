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
3. Run below command to install your pacakge locally
```
pip install dist/<YOU_PACAKGE_NAME>
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
