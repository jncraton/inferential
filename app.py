from html import escape
from flask import *
import languagemodels as lm
from markupsafe import escape
import requests
from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer
import ctranslate2

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
@app.route("/api")
def api():
    query = request.args.get("input", "")
    if len(query) >= 250 or query == "":
        return {"data": "Enter a valid query!"}

    reply = tokenize(query)
    return {"data": reply}, 200  # returns the dictionary and a 200 response code

def tokenize(input):
    # Download the tokenizer
    tok_config = hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "tokenizer.json")
    tokenizer = Tokenizer.from_file(tok_config)

    # Tokenize the input
    tokens = tokenizer.encode(input).tokens

    # Download the model configuration and model weights
    hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "config.json")
    model_path = hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "model.bin")
    model_base_path = model_path[:-10]

    # Download shared vocabulary
    hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "shared_vocabulary.txt")

    # Initialize the translator
    model = ctranslate2.Translator(model_base_path, compute_type="int8")

    # Translate the tokens
    results = model.translate_batch([tokens])
    output_tokens = results[0].hypotheses[0]
    output_ids = [tokenizer.token_to_id(t) for t in output_tokens]
    text = tokenizer.decode(output_ids, skip_special_tokens=True)
    return text