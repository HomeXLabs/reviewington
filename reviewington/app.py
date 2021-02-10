import datetime

from reviewington.diff2html import diff2html
from flask import Flask, render_template

import markdown
from markdown.extensions.fenced_code import FencedCodeExtension


app = Flask(__name__, template_folder="templates")


def getHtml(diffData, path):
    return diff2html(diffData, path)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/reviews", methods=["GET"])
def reviews():
    return render_template(
        "reviews.html",
        tags=[
            {"id": "change", "name": "Change"},
            {"id": "question", "name": "Question"},
            {"id": "concern", "name": "Concern"},
            {"id": "discussion", "name": "Discussion"},
            {"id": "praise", "name": "Praise"},
            {"id": "suggestion", "name": "Suggestion"},
            {"id": "nitpick", "name": "Nitpick"},
            {"id": "guide", "name": "Guide"},
        ],
        discussions=[
            {
                "url": "https://api.github.com/repos/octocat/Hello-World/pulls/comments/1",
                "path": "file1.txt",
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
                            extensions=[FencedCodeExtension()],
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
    )


if __name__ == "__main__":
    app.run()

