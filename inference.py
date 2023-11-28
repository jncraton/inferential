import threading
import os
from tokenizers import Tokenizer
import ctranslate2
from ctransformers import AutoModelForCausalLM
from huggingface_hub import hf_hub_download, snapshot_download
import yaml

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

models = {m["name"]: m for m in config["models"]}

for model in models:
    models[model]["loaded"] = False


def download_llms():
    for name, model in models.items():
        if model["backend"] == "ctransformers":
            models[name]["model"] = AutoModelForCausalLM.from_pretrained(name)
            models[name]["loaded"] = True
        elif model["backend"] == "ctranslate2":
            path = snapshot_download(repo_id=name)

            models[name]["model"] = ctranslate2.Translator(path, compute_type="int8")
            models[name]["tokenizer"] = Tokenizer.from_file(
                os.path.join(path, "tokenizer.json")
            )
            models[name]["loaded"] = True
        else:
            raise ValueError(
                "Invalid backend in config file for model named '" + name + "'"
            )


threading.Thread(target=download_llms).start()


def generate(prompt, model_name):
    model = models[model_name]

    if not model["loaded"]:
        return

    if model["backend"] == "ctransformers":
        reply = generate_response_ctransformers(prompt, model)
    elif model["backend"] == "ctranslate2":
        reply = generate_response_ctranslate2(prompt, model)
    else:
        raise ValueError(
            "Invalid backend in loaded models list for model named '" + model_name + "'"
        )

    return reply


def generate_response_ctranslate2(prompt, model):
    # Tokenize the input
    input_tokens = model["tokenizer"].encode(prompt).tokens

    # Translate the tokens
    results = model["model"].generate_tokens(input_tokens, disable_unk=True)

    accumlated_results = []
    current_length = 0
    for item in results:
        if item.is_last:
            break
        accumlated_results.append(item.token_id)
        decoded_string = model["tokenizer"].decode(accumlated_results)
        new_text = decoded_string[current_length - len(decoded_string) :]
        current_length = len(decoded_string)
        yield new_text


def generate_response_ctransformers(prompt, model):
    for text in model["model"](prompt, stream=True):
        yield text
