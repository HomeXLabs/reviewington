import datetime
from flask import Flask, render_template


app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        discussions=[
            {
                "url": "https://api.github.com/repos/octocat/Hello-World/pulls/comments/1",
                "path": "file1.txt",
                "diffHunk": "@@ -16,33 +16,40 @@ public class Connection : IConnection...",
                "comments": [
                    {
                        "user": {
                            "login": "octocat",
                            "url": "https://api.github.com/users/octocat",
                        },
                        "body": "Great stuff!",
                        "created_at": datetime.datetime.strptime(
                            "2011-04-14T16:00:49Z", "%Y-%m-%dT%H:%M:%SZ"
                        ),
                    },
                    {
                        "user": {
                            "login": "octodog",
                            "url": "https://api.github.com/users/octocat",
                        },
                        "body": "Thanks!",
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
    app.run(passthrough_errors=False)
