from flask import *
from markupsafe import escape
from inference import generate_response_ctranslate2
from huggingface_hub import hf_hub_download, snapshot_download

app = Flask(__name__)

# Download the model (ctranslate2)
model_folder = snapshot_download(repo_id="jncraton/LaMini-Flan-T5-248M-ct2-int8")
tok_config = hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "tokenizer.json")


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

    tokens = generate_response_ctranslate2(query, model_folder)
    return Response(tokens, content_type="text/plain")
