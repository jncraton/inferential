import threading
import os
from tokenizers import Tokenizer
import ctranslate2
from ctransformers import AutoModelForCausalLM
from huggingface_hub import snapshot_download
import yaml
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)


models = {m["name"]: m for m in config["models"]}

def download_llms(config_models, models, models_status):
    for model in config_models:
        name = model["name"]
        print(f"Loading model {name}")

        if model["backend"] == "ctransformers":
            model["model"] = AutoModelForCausalLM.from_pretrained(name)
        elif model["backend"] == "ctranslate2":
            path = snapshot_download(repo_id=name)

            model["model"] = ctranslate2.Translator(path, compute_type="int8")
            model["tokenizer"] = Tokenizer.from_file(
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
    return models



threading.Thread(target=download_llms).start()


def generate(prompt, model_name):
    model = models[model_name]

    if not model["model"]:
        return

    if model["backend"] == "ctransformers":
        for text in model["model"](prompt, stream=True):
            yield text
    elif model["backend"] == "ctranslate2":
        # Tokenize the input
        input_tokens = model["tokenizer"].encode(prompt).tokens

        # Translate the tokens
        results = model["model"].generate_tokens(input_tokens, disable_unk=True)

        accumlated_results = []
        bytes_sent = 0
        for item in results:
            accumlated_results.append(item.token_id)
            decoded_string = model["tokenizer"].decode(accumlated_results)
            new_text = decoded_string[bytes_sent:]
            bytes_sent = len(decoded_string)
            yield new_text
    else:
        raise ValueError(
            "Invalid backend in loaded models list for model named '" + model_name + "'"
        )
