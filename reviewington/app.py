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
        return search_query.lower() in comment["body"].lower() or search_query.lower() in comment["user"]["login"]

    return lambda comment: (
        (
            len(valid_tags) == 0
            or comment["tag"] in valid_tags
            or (missing_tag_allowed and len(comment["tag"]) == 0)
        )
        and (comment["path"].startswith(filepath))
        and (
            search_query.lower() in comment["diffHunk"].lower()
            or len(list(filter(filterComments, comment["comments"]))) > 0
        )
    )


@app.route("/files", methods=["GET"])
def files():
    return render_template("files.html", reponame="Reviewington", files=res)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/reviews", methods=["GET"])
def reviews():
    selected_tags = list(set(request.args.keys()) & set(TAG_IDS))

    return render_template(
        "reviews.html",
        tags=TAGS,
        discussions=filter(
            searchMatch(request.args),
            [
                {
                    "url": "https://api.github.com/repos/octocat/Hello-World/pulls/comments/1",
                    "path": "file1.txt",
                    "urlToPath": "https://github.com/octocat/Hello-World/file1.txt",
                    "tag": "suggestion",
                    "diffHunk": getHtml(
                        "@@ -219,24 +239,77 @@\n     ```\n \n ## Ordering\n-  - Always follow the following order for methods in a React component:\n+\n+  - Ordering for class extends React.Component:\n+  \n+  1. constructor\n+  1. optional static methods\n+  1. getChildContext\n+  1. componentWillMount\n+  1. componentDidMount\n+  1. componentWillReceiveProps\n+  1. shouldComponentUpdate\n+  1. componentWillUpdate\n+  1. componentDidUpdate\n+  1. componentWillUnmount\n+  1. *clickHandlers or eventHandlers* like onClickSubmit() or onChangeDescription()\n+  1. *getter methods for render* like getSelectReason() or getFooterContent()\n+  1. *Optional render methods* like renderNavigation() or renderProfilePicture()\n+  1. render\n+\n+  - How to define propTypes, defaultProps, contextTypes, etc...  \n+\n+  ```javascript\n+  import React, { Component, PropTypes } from 'react';\n+  \n+  const propTypes = {\n+    id: PropTypes.number.isRequired,\n+    url: PropTypes.string.isRequired,\n+    text: PropTypes.string,\n+  };\n+  \n+  const defaultProps = {\n+    text: 'Hello World',\n+  };\n+  \n+  class Link extends Component {",
                        "file1.txt",
                    ),
                    "comments": [
                        {
                            "url": "https://comment-url.com",
                            "user": {
                                "login": "octocat",
                                "url": "https://api.github.com/users/octocat",
                            },
                            "body": markdown.markdown(
                                "Great *stuff*!\n Have you tried ```print('Hello, world')```? ",
                                extensions=["fenced_code"],
                            ).replace("\n", "<br/>"),
                            "created_at": datetime.datetime.strptime(
                                "2011-04-14T16:00:49Z", "%Y-%m-%dT%H:%M:%SZ"
                            ),
                        },
                        {
                            "url": "https://comment-url.com",
                            "user": {
                                "login": "octodog",
                                "url": "https://api.github.com/users/octocat",
                            },
                            "body": markdown.markdown(
                                "Thanks ", extensions=["fenced_code"]
                            ).replace("\n", "<br/>"),
                            "created_at": datetime.datetime.strptime(
                                "2011-04-14T16:32:21Z", "%Y-%m-%dT%H:%M:%SZ"
                            ),
                        },
                    ],
                    "html_url": "https://github.com/octocat/Hello-World/pull/1#discussion-diff-1",
                }
            ],
        ),
    )


if __name__ == "__main__":
    app.run()
