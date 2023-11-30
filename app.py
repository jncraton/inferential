import yaml
from flask import Flask, Response, request, render_template, send_from_directory
from inference import generate, models,download_llms
import threading
app = Flask(__name__)


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)


# Opens the config file and sets up config_models
models_status = {"models": [], "loadedAll": False}
with open("config.yml", "r") as f:
    config_root = yaml.safe_load(f)
    config_models = config_root["models"]
    logo = config_root["logo"]
for model in config_models:
    models_status["models"].append({"name": model["name"], "loaded": False})

# Start a new thread to load the models asynchronously
models = {}
threading.Thread(
    target=download_llms, args=(config_models, models, models_status)
).start()



# Loading page
@app.route("/")
def loading_page():
    return render_template("status.html", logo=logo)


# API Front End
@app.route("/playground")
def playground():
    return render_template("index.html", models=config_models, logo=logo)


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

    if not model_name in models:
        return f"Error: Unknown model name '{model_name}'.", 400  # 400 Bad Request

    return Response(generate(query, model_name), content_type="text/plain")


@app.route("/api/status")
def api_status_page():
    return models_status
