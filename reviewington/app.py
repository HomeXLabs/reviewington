import datetime
import os
import subprocess
import threading

from flask import Flask, render_template, request
from reviewington.repository import Repository
from reviewington.search import search_discussions
from reviewington.tags import TAGS, TAG_IDS

# Initialize Flask App
app = Flask(__name__, template_folder="templates")


# Initialize global session data
def get_github_data():
    """On startup this function will query all github data in background thread."""
    global session
    if "repo" not in session:
        session["repo"] = Repository(os.environ["GITHUB_ORG_REPO"])
    if "filenames" not in session:
        session["filenames"] = session["repo"].get_repo_filenames()
    if "discussions" not in session:
        session["discussions"] = session["repo"].get_pr_discussions()


global session
session = {}
threading.Thread(target=get_github_data).start()

# Routes
@app.route("/files", methods=["GET"])
def files():
    if "filenames" not in session:
        return render_template("loading.html")
    return render_template(
        "files.html", reponame=session["repo"].name, files=session["filenames"]
    )


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/reviews", methods=["GET"])
def reviews():
    selected_tags = list(set(request.args.keys()) & set(TAG_IDS))

    if "discussions" not in session:
        return render_template("loading.html")
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
