from html import escape
from flask import *
import languagemodels as lm
from markupsafe import escape
import requests
from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer
import ctranslate2
import json

app = Flask(__name__)


# Front end
@app.route("/")
def root():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.root_path, "static/favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


# Backend
import time  # Import the time module


@app.route("/api")
def api():
    query = request.args.get("input", "")
    if query == "":
        return {"data": "Error: No prompt was provided."}, 400  # 400 Bad Request
    if len(query) >= 250:
        return {"data": "Error: The prompt was too long."}, 413  # 413 Content Too Large

    tokens = tokenize(query)
    return Response(tokens, content_type="text/plain")


def tokenize(input):
    # Download the tokenizer
    tok_config = hf_hub_download(
        "jncraton/LaMini-Flan-T5-248M-ct2-int8", "tokenizer.json"
    )
    tokenizer = Tokenizer.from_file(tok_config)

    # Tokenize the input
    input_tokens = tokenizer.encode(input).tokens  # This is the query
    # Download the model configuration and model weights
   
    model_path = hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "model.bin")
    if model_path is None or model_path == "":
        model_path = hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "model.bin")
    model_base_path = model_path[:-10]
    print("Model path: " + model_path)
    print("Model base path: " + model_base_path)
    # Initialize the translator
    try:
        model = ctranslate2.Translator(str(model_base_path), compute_type="int8")
        print("Model: " + str(model))
   
        
    # Translate the tokens
    
        results = model.generate_tokens(
        input_tokens, disable_unk=True
    )  # This generates the reply of tokens

        for text in results:
            list_of_token_ids = []
            list_of_token_ids.append(text.token_id)
            response = tokenizer.decode(list_of_token_ids)
            yield response
    except RuntimeError as e:
        print("Issue with model: " + str(e))
