import yaml
from flask import Flask, Response, request, render_template, send_from_directory
from inference import generate

app = Flask(__name__)

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)


# Loading page
@app.route("/")
def loading_page():
    return render_template("status.html")


# API Front End
@app.route("/playground")
def playground():
    return render_template("index.html", models=config["models"])


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.root_path, "static/favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


# Backend
@app.route("/api")
def api():
    query = request.args.get("input", "")
    if request.args.get("model", ""):
        model_name = request.args.get("model", "")
    else:
        model_name = config["models"][0]["name"]

    if query == "":
        return "Error: No prompt was provided.", 400  # 400 Bad Request
    if len(query) >= 250:
        return "Error: The prompt was too long.", 413  # 413 Content Too Large

    reply = generate(query, model_name)

    return Response(reply, content_type="text/plain")


@app.route("/api/status")
def api_status_page():
    return str(len(models))
