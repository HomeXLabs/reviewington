import datetime
import os
import subprocess

from flask import Flask, render_template, request

from reviewington.repository import Repository
from reviewington.search import search_discussions
from reviewington.tags import TAGS, TAG_IDS


app = Flask(__name__, template_folder="templates")
global session
session = {}
if "repo" not in session:
    session["repo"] = Repository(os.environ["GITHUB_ORG_REPO"])
if "discussions" not in session:
    session["discussions"] = session["repo"].get_pr_discussions()
if "filenames" not in session:
    session["filenames"] = session["repo"].get_repo_filenames()


@app.route("/files", methods=["GET"])
def files():
    return render_template("files.html", reponame=session["repo"].name, files=session["filenames"])


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


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
