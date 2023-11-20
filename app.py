from flask import *
from markupsafe import escape
from inference import generate_response_ctranslate2, generate_response_ctransformers
from huggingface_hub import hf_hub_download, snapshot_download
from ctransformers import AutoModelForCausalLM
import yaml

app = Flask(__name__)

with open("config.yml", "r") as f:
    config_index = yaml.safe_load(f)

flag = False #Flag to only call this once 
def download_llms():
    global flag
    for model in config_index["models"]: #For each model in the config index 
        if flag == False: #If this function hasn't been called install each model
            if model["backend"] == "ctransformers":
                global llm
                llm = AutoModelForCausalLM.from_pretrained(model["name"]) #These all download to the hub
                api_model_status(True, model["name"]) #Return true to api_model_status to confirm the model is done installing
            else:
                #Download the model (ctranslate2)
                global model_folder
                global tok_config
                model_folder = snapshot_download(repo_id=model["name"]) #These all download to the hub
                tok_config = hf_hub_download(model["name"], "tokenizer.json") #These all download to the hub
                api_model_status(True, model["name"]) #Return true to api_model_status to confirm the model is done installing

#Before the request, will call function and check if the models are downloaded
@app.before_request  
def intialized():
    global flag
    if not flag:
        download_llms()
        flag = True

global selected_model
selected_model = config_index["models"][5]


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
        return "Error: No prompt was provided.", 400  # 400 Bad Request
    if len(query) >= 250:
        return "Error: The prompt was too long.", 413  # 413 Content Too Large
    # Dynamically generate reposnse based on the selected backend
    if selected_model["backend"] == "ctransformers":
        reply = generate_response_ctransformers(query, llm)
        return Response(reply, content_type="text/plain")
    else:
        tokens = generate_response_ctranslate2(query, model_folder)
        return Response(tokens, content_type="text/plain")

#@app.route("/api/model-status")
def api_model_status(flag, model_name): #needs to keep track of 
    if flag:
        print(model_name, " is done downloading")
