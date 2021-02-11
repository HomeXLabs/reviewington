import datetime
import os
import subprocess

from flask import Flask, render_template, request

from reviewington.diff2html import diff2html
from reviewington.repository import Repository
from reviewington.tags import TAGS

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
        recurse_setdefault(res.setdefault((array[0], os.path.join(currentPath, array[0])), {}), array[1:], os.path.join(currentPath, array[0]))


res = {}
for f in out.decode("utf-8").splitlines():
    recurse_setdefault(res, f.split("/"), "/")

app = Flask(__name__, template_folder="templates")
global session
session = {}
if "repo" not in session:
    session["repo"] = Repository("HomeXLabs/reviewington")
if "discussions" not in session:
    session["discussions"] = session["repo"].pr_discussions


def getHtml(diffData, path):
    return diff2html(diffData, path)


def searchMatch(params):
    filepath = params.get("filepath", "")
    search_query = params.get("search", "")
    missing_tag_allowed = False
    valid_tags = []
    for tag in TAGS:
        tag_id = tag["id"]
        tag_val = params.get(tag_id)
        if tag_val:
            if tag_id == "none":
                missing_tag_allowed = True
            else:
                valid_tags.append(tag_id)

    def filterComments(comment):
        return search_query.lower() in comment["body"].lower()

    return lambda discussion: (
        (
            len(valid_tags) == 0
            or discussion.tag in valid_tags
            or (missing_tag_allowed and len(discussion.tag) == 0)
        )
        and (discussion.path.startswith(filepath))
        and (
            search_query.lower() in discussion.diffHunk.lower()
            or len(list(filter(filterComments, discussion.comments))) > 0
        )
    )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", files=res)

@app.route("/reviews", methods=["GET"])
def reviews():
    return render_template(
        "reviews.html",
        tags=TAGS,
        discussions=session["discussions"] #filter(searchMatch(request.args), session["discussions"]),
    )


if __name__ == "__main__":
    app.run()
