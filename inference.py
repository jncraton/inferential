import threading
import os
from tokenizers import Tokenizer
import ctranslate2
from ctransformers import AutoModelForCausalLM
from huggingface_hub import snapshot_download
import yaml


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

models = {m["name"]: {} for m in config["models"]}
models_status = {
    "models": [{"name": m["name"], "loaded": False} for m in config["models"]],
    "loadedAll": False,
}


def download_llms():
    for model_config in config["models"]:
        name = model_config["name"]
        print(f"Loading model {name}")

        models[name]["backend"] = model_config["backend"]
        if model_config["backend"] == "ctransformers":
            models[name]["model"] = AutoModelForCausalLM.from_pretrained(name)
        elif model_config["backend"] == "ctranslate2":
            path = snapshot_download(repo_id=name)

            models[name]["model"] = ctranslate2.Translator(path, compute_type="int8")
            models[name]["tokenizer"] = Tokenizer.from_file(
                os.path.join(path, "tokenizer.json")
            )
        else:
            raise ValueError(
                "Invalid backend in config file for model named '" + name + "'"
            )
        for entry in models_status["models"]:
            if entry["name"] == name:
                entry["loaded"] = True
                break
    models_status["loadedAll"] = True
    print("All models loaded")


threading.Thread(target=download_llms).start()


def generate(prompt, model_name):
    print(models)
    model_data = models[model_name]

    if not model_data["model"]:
        return

    if model_data["backend"] == "ctransformers":
        for text in model_data["model"](prompt, stream=True):
            yield text
    elif model_data["backend"] == "ctranslate2":
        # Tokenize the input
        input_tokens = model_data["tokenizer"].encode(prompt).tokens

        # Translate the tokens
        results = model_data["model"].generate_tokens(input_tokens, disable_unk=True)

        accumlated_results = []
        bytes_sent = 0
        for item in results:
            accumlated_results.append(item.token_id)
            decoded_string = model_data["tokenizer"].decode(accumlated_results)
            new_text = decoded_string[bytes_sent:]
            bytes_sent = len(decoded_string)
            yield new_text
    else:
        raise ValueError(f"Invalid backend for {model_name}")
