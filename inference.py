""" This module provides functions for downloading and generating responses using pre-trained language models for the "Inferential" web app."""

import threading
from os.path import join
from tokenizers import Tokenizer
import ctranslate2
from ctransformers import AutoModelForCausalLM
from huggingface_hub import snapshot_download
import yaml


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

models = {m["name"]: m for m in config["models"]}


def download_llms():
    for name, model in models.items():
        print(f"Loading model {name}")

        if model["backend"] == "ctransformers":
            model["model"] = AutoModelForCausalLM.from_pretrained(name)
        elif model["backend"] == "ctranslate2":
            path = snapshot_download(repo_id=name)

            try:
                model["model"] = ctranslate2.Translator(path, compute_type="int8")
            except RuntimeError:
                model["model"] = ctranslate2.Generator(path, compute_type="int8")
            model["tokenizer"] = Tokenizer.from_file(join(path, "tokenizer.json"))
        else:
            raise ValueError(f"Invalid backend for {name}")

    print("All models loaded")


threading.Thread(target=download_llms).start()


def generate(prompt, model_name):
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
