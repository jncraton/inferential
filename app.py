from flask import *
import yaml
from ctransformers import AutoModelForCausalLM


app = Flask(__name__)

# Opens the config file and assigns it to config_index
with open("config.yml", "r") as f:
    config_index = yaml.safe_load(f)

# Uses the chosen model in the config file and sets it to selected_model
selected_model = config_index["models"][2]

# Dynamically load the appropriate model based on the selected backend
if selected_model["backend"] == "ctransformers":
    llm = AutoModelForCausalLM.from_pretrained(selected_model["name"], gpu_layers=50)
else:
    pass


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

    # Generate a reply using the selected model
    reply = llm(query)
    return {"data": reply}, 200  # returns with a response code of 200 OK
