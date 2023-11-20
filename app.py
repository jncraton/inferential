from flask import *
from markupsafe import escape
from inference import generate_response_ctranslate2, generate_response_ctransformers
from huggingface_hub import hf_hub_download, snapshot_download
from ctransformers import AutoModelForCausalLM
import yaml

app = Flask(__name__)

# Opens the config file and assigns it to config_index
with open("config.yml", "r") as f:
    config_index = yaml.safe_load(f)

# # Uses the chosen model in the config file and sets it to selected_model


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
    model = int(request.args.get("model", ""))

    if query == "":
        return "Error: No prompt was provided.", 400  # 400 Bad Request
    if len(query) >= 250:
        return "Error: The prompt was too long.", 413  # 413 Content Too Large

    if model == -1:  # If no model is picked change to default
        selected_model = config_index["models"][0]

    selected_model = config_index["models"][model]
    # Dynamically load the appropriate model based on the selected backend
    if selected_model["backend"] == "ctransformers":
        llm = AutoModelForCausalLM.from_pretrained(selected_model["name"])
    else:
        # Download the model (ctranslate2)
        model_folder = snapshot_download(repo_id=selected_model["name"])
        tok_config = hf_hub_download(selected_model["name"], "tokenizer.json")

    if selected_model["backend"] == "ctransformers":
        reply = generate_response_ctransformers(query, llm)
        return Response(reply, content_type="text/plain")
    else:
        # Download the model (ctranslate2)
        tokens = generate_response_ctranslate2(query, model_folder)
        return Response(tokens, content_type="text/plain")
