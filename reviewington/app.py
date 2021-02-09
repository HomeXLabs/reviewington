import os
from flask import Flask, render_template


app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET"])
def index():
    repo_name = os.environ["GITHUB_ORG_REPO"]
    return render_template("index.html", example=repo_name)


if __name__ == "__main__":
    app.run()
