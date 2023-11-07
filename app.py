from html import escape
from flask import *
import languagemodels as lm
from markupsafe import escape
import requests
import yaml


app = Flask(__name__)

# Opens the config file and assigns it to configIndex
with open("config.yml", "r") as f:
    configIndex = yaml.safe_load(f)

# Uses the chosen model in the config file and sets it to selected_model
selected_model = configIndex["models"][0]

# Changes the model lm uses to the selected model.
lm.config["instruct_model"] = selected_model
lm.set_max_ram("512mb")


# Loading page
@app.route("/")
def loading_page():
    return render_template("status.html")


# API Front End
@app.route("/playground")
def playground():
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
