from flask import *
from markupsafe import escape
from inference import generate_response_ctranslate2, generate_response_ctransformers
from download import download_llms
import yaml
import threading

app = Flask(__name__)
# Opens the config file and assigns it to config_index
with open("config.yml", "r") as f:
    config_root = yaml.safe_load(f)
    config_models = config_root["models"]

#On load
threading.Thread(target = download_llms).start()

# Loading page
@app.route("/")
def loading_page():
    return render_template("status.html")


# API Front End
@app.route("/playground")
def playground():
    return render_template("index.html", models=config_models)


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
    if not model_name in model_config:
        return "Error: Unknown model name '" + model_name + "'.", 400  # 400 Bad Request
    model_config = config_models[model_name]

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
            "Invalid backend in loaded models list for model named '" + model_config["name"] + "'"
        )
    return Response(reply, content_type="text/plain")

@app.route("/api-status-page")
def api_status_page():
    flag = download_llms()
    if flag:
        print("Model is downloaded")