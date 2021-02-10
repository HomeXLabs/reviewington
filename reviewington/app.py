import datetime
from diff2html import diff2html
from flask import Flask, render_template, request
import markdown
import subprocess

# TODO: replace with fetched input
out = subprocess.check_output(['git', 'ls-tree', '--full-tree', '-r', '--name-only', 'HEAD'])

def recurse_setdefault(res, array):
    if len(array) == 0:
        return
    elif len(array) == 1:
        res[array[0]] = {}
    else:
        recurse_setdefault(res.setdefault(array[0], {}), array[1:])

res = {}
for f in out.decode("utf-8").splitlines():
    recurse_setdefault(res, f.split("/"))

app = Flask(__name__, template_folder="templates")


TAGS = [
    {"id": "change", "name": "Change"},
    {"id": "question", "name": "Question"},
    {"id": "concern", "name": "Concern"},
    {"id": "discussion", "name": "Discussion"},
    {"id": "praise", "name": "Praise"},
    {"id": "suggestion", "name": "Suggestion"},
    {"id": "nitpick", "name": "Nitpick"},
    {"id": "guide", "name": "Guide"},
]


def getHtml(diffData, path):
    return diff2html(diffData, path)


def searchMatch(params):
    filename = params.get("filename")
    search_query = params.get("search")
    valid_tags = []
    for tag in TAGS:
        tag_val = params.get(tag["id"])
        if tag_val:
            valid_tags.append(tag["id"])

    return lambda comment: (
        (len(valid_tags) == 0 or comment["tag"] in valid_tags)
        and (comment["path"] == filename)
        and (True)  # TODO: Check that the comment matches search_query.
    )

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", files = res)


@app.route("/reviews", methods=["GET"])
def reviews():
    return render_template(
        "reviews.html",
        tags=TAGS,
        discussions=filter(
            searchMatch(request.args),
            [
                {
                    "url": "https://api.github.com/repos/octocat/Hello-World/pulls/comments/1",
                    "path": "file1.txt",
                    "tag": "Suggestion",
                    "diffHunk": getHtml(
                        "@@ -219,24 +239,77 @@\n     ```\n \n ## Ordering\n-  - Always follow the following order for methods in a React component:\n+\n+  - Ordering for class extends React.Component:\n+  \n+  1. constructor\n+  1. optional static methods\n+  1. getChildContext\n+  1. componentWillMount\n+  1. componentDidMount\n+  1. componentWillReceiveProps\n+  1. shouldComponentUpdate\n+  1. componentWillUpdate\n+  1. componentDidUpdate\n+  1. componentWillUnmount\n+  1. *clickHandlers or eventHandlers* like onClickSubmit() or onChangeDescription()\n+  1. *getter methods for render* like getSelectReason() or getFooterContent()\n+  1. *Optional render methods* like renderNavigation() or renderProfilePicture()\n+  1. render\n+\n+  - How to define propTypes, defaultProps, contextTypes, etc...  \n+\n+  ```javascript\n+  import React, { Component, PropTypes } from 'react';\n+  \n+  const propTypes = {\n+    id: PropTypes.number.isRequired,\n+    url: PropTypes.string.isRequired,\n+    text: PropTypes.string,\n+  };\n+  \n+  const defaultProps = {\n+    text: 'Hello World',\n+  };\n+  \n+  class Link extends Component {",
                        "file1.txt",
                    ),
                    "comments": [
                        {
                            "user": {
                                "login": "octocat",
                                "url": "https://api.github.com/users/octocat",
                            },
                            "body": markdown.markdown(
                                "Great *stuff*!\n Have you tried ```print('Hello, world')```? ",
                                extensions=['fenced_code'],
                            ).replace("\n", "<br/>"),
                            "created_at": datetime.datetime.strptime(
                                "2011-04-14T16:00:49Z", "%Y-%m-%dT%H:%M:%SZ"
                            ),
                        },
                        {
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
