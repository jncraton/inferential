from html import escape
from flask import *
import languagemodels as lm
from markupsafe import escape
import requests

app = Flask(__name__)


# Front end
@app.route("/")
def root():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.root_path, "static/favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


# Backend
@app.route("/api")
def api():
    query = request.args.get("input", "")
    if len(query) >= 250 or query == "":
        return {"data": "Enter a valid query!"}

    reply = lm.do(query)
    return {"data": reply}, 200  # Returns the dictionary and a 200 response code
