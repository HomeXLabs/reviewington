import datetime
import os
import subprocess

from flask import Flask, render_template, request

from reviewington.diff2html import diff2html
from reviewington.repository import Repository
from reviewington.search import search_discussions
from reviewington.tags import TAGS, TAG_IDS

# TODO: replace with fetched input
out = subprocess.check_output(
    ["git", "ls-tree", "--full-tree", "-r", "--name-only", "HEAD"]
)


def recurse_setdefault(res, array, currentPath):
    if len(array) == 0:
        return
    elif len(array) == 1:
        res[(array[0], os.path.join(currentPath, array[0]))] = {}
    else:
        recurse_setdefault(
            res.setdefault((array[0], os.path.join(currentPath, array[0])), {}),
            array[1:],
            os.path.join(currentPath, array[0]),
        )


res = {}
for f in out.decode("utf-8").splitlines():
    recurse_setdefault(res, f.split("/"), "/")

app = Flask(__name__, template_folder="templates")
global session
session = {}
if "repo" not in session:
    session["repo"] = Repository(os.environ["GITHUB_ORG_REPO"])
if "discussions" not in session:
    session["discussions"] = session["repo"].pr_discussions


def getHtml(diffData, path):
    return diff2html(diffData, path)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", files=res)


@app.route("/reviews", methods=["GET"])
def reviews():
    selected_tags = list(set(request.args.keys()) & set(TAG_IDS))

    return render_template(
        "reviews.html",
        tags=TAGS,
        discussions=search_discussions(
            session["discussions"],
            request.args.get("filepath", ""),
            request.args.get("search", ""),
            selected_tags,
        ),
    )


if __name__ == "__main__":
    app.run()
