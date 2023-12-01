import yaml
from flask import Flask, Response, request, render_template, send_from_directory
from inference import generate, models

app = Flask(__name__)


# Read the config file
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)


# Loading page
@app.route("/")
def loading_page():
    return render_template("status.html", logo=config["logo"])


# API Front End
@app.route("/playground")
def playground():
    return render_template("index.html", models=config["models"], logo=config["logo"])


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

    for model in config_models:
        if model["name"] == model_name:
            maxPrompt = model["maxPromptToken"]
    if query == "":
        return "Error: No prompt was provided.", 400  # 400 Bad Request
    if len(query) >= maxPrompt:
        return "Error: The prompt was too long.", 413  # 413 Content Too Large

    if not model_name in models:
        return f"Error: Unknown model name '{model_name}'.", 400  # 400 Bad Request

    return Response(generate(query, model_name), content_type="text/plain")


@app.route("/api/status")
def api_status_page():
    status = [{"name": m["name"], "loaded": "model" in m} for m in models.values()]

    return {"models": status, "loadedAll": all(m["loaded"] for m in status)}
