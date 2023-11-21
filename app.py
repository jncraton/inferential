from flask import *
from markupsafe import escape
from inference import generate_response_ctranslate2, generate_response_ctransformers
from huggingface_hub import hf_hub_download, snapshot_download
from ctransformers import AutoModelForCausalLM
import yaml

app = Flask(__name__)

# Opens the config file and assigns it to config_index
with open("config.yml", "r") as f:
    config_root = yaml.safe_load(f)
    config_models = config_root["models"]
    config_logos = config_root["logos"]

models = {}

# Dynamically load the appropriate model based on the selected backend
for model in config_models:
    name = model["name"]
    if model["backend"] == "ctransformers":
        models[name] = {
            "backend": "ctransformers",
            "auto-model": AutoModelForCausalLM.from_pretrained(name),
        }
    elif model["backend"] == "ctranslate2":
        # Download the model (ctranslate2)
        model_path = snapshot_download(repo_id=name)
        models[name] = {"backend": "ctranslate2", "model-path": model_path}
    else:
        raise ValueError(
            "Invalid backend in config file for model named '" + name + "'"
        )

selected_logo = config_logos[0]
logo_path = selected_logo["path"]
logo_url = selected_logo.get("web", "")


# Loading page


@app.route("/")
def loading_page():
    return render_template("status.html", selected_logo=selected_logo)


# API Front End
@app.route("/playground")
def playground():
    return render_template(
        "index.html", models=config_models, selected_logo=selected_logo, logo_url=logo_url
    )


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
        model_name = config_models[0]["name"]
    if not model_name in models:
        return "Error: Unknown model name '" + model_name + "'.", 400  # 400 Bad Request
    model_config = models[model_name]

    if query == "":
        return "Error: No prompt was provided.", 400  # 400 Bad Request
    if len(query) >= 250:
        return "Error: The prompt was too long.", 413  # 413 Content Too Large

    if model_config["backend"] == "ctransformers":
        reply = generate_response_ctransformers(query, model_config["auto-model"])
    elif model_config["backend"] == "ctranslate2":
        reply = generate_response_ctranslate2(query, model_config["model-path"])
    else:
        raise ValueError(
            "Invalid backend in loaded models list for model named '" + name + "'"
        )
    return Response(reply, content_type="text/plain")
