from flask import *

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        # For now, the output is just the input
        output = escape(request.form["input"])
        return render_template("index.html", output=output, outputDisplay="block")
    else:
        return render_template("index.html", output="", outputDisplay="none")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.root_path, "static/favicon.ico", mimetype="image/vnd.microsoft.icon"
    )
