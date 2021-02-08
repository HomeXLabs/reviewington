from flask import Flask, render_template


app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", example="example variable")


if __name__ == "__main__":
    app.run()
