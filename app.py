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
    if query == "":
        return {"data": "Error: No prompt was provided."}, 400  # 400 Bad Request
    if len(query) >= 250:
        return {"data": "Error: The prompt was too long."}, 413  # 413 Content Too Large

    reply = lm.do(query)
    return {"data": reply}, 200  # returns with a response code of 200 OK
