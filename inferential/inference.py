""" This module provides functions for downloading and generating responses using pre-trained language models for the "Inferential" web app."""

import threading
from os.path import join
from tokenizers import Tokenizer
import ctranslate2
from ctransformers import AutoModelForCausalLM
from huggingface_hub import snapshot_download, hf_hub_download
import requests
import json
from inferential.stats import log
from inferential.stats import config

models = {m["name"]: m for m in config["models"]}


def download_llms():
    for name, model in models.items():
        print(f"Loading model {name}")

        if model["backend"] == "ctransformers":
            model["model"] = AutoModelForCausalLM.from_pretrained(model["hf_path"])
        elif model["backend"] == "ctranslate2":
            path = snapshot_download(repo_id=model["hf_path"])

            try:
                model["model"] = ctranslate2.Translator(path, compute_type="int8")
            except RuntimeError:
                model["model"] = ctranslate2.Generator(path, compute_type="int8")
            model["tokenizer"] = Tokenizer.from_file(join(path, "tokenizer.json"))
        elif model["backend"] == "vllm":
            path = hf_hub_download(repo_id=model["hf_path"], filename="tokenizer.json")
            model["model"] = True
            model["tokenizer"] = Tokenizer.from_file(path)
        else:
            raise ValueError(f"Invalid backend for {name}")

    print("All models loaded")


threading.Thread(target=download_llms).start()


def generate(prompt, model_name, gen_params):
    model_data = models[model_name]
    max_tokens = int(gen_params.get("max_tokens", 128))

    if not model_data["model"]:
        return

    if model_data["backend"] == "ctransformers":
        num_tokens_generated = 0
        for text in model_data["model"](prompt, stream=True, top_k=1):
            num_tokens_generated += 1
            yield text
            if num_tokens_generated >= max_tokens:
                break
        log(model_name, None, num_tokens_generated)
    elif model_data["backend"] == "ctranslate2":
        # Tokenize the input
        input_tokens = model_data["tokenizer"].encode(prompt).tokens

        # Translate the tokens
        results = model_data["model"].generate_tokens(input_tokens, disable_unk=True)

        output_tokens = []
        bytes_sent = 0
        for item in results:
            output_tokens.append(item.token_id)
            decoded_string = model_data["tokenizer"].decode(output_tokens)
            new_text = decoded_string[bytes_sent:]
            bytes_sent = len(decoded_string)
            yield new_text
            if len(output_tokens) >= max_tokens:
                break

        log(model_name, len(input_tokens), len(output_tokens))

    elif model_data["backend"] == "vllm":
        headers = {"User-Agent": "Test Client"}
        pload = {
            "prompt": prompt,
            "temperature": 0.0,
            "max_tokens": 2048,
            "stream": True,
        }
        response = requests.post(
            model_data["url"], headers=headers, json=pload, stream=True
        )

        last = prompt
        for chunk in response.iter_lines(
            chunk_size=8192, decode_unicode=False, delimiter=b"\0"
        ):
            if chunk:
                data = json.loads(chunk.decode("utf-8"))
                output = data["text"]
                yield output[-1][len(last) :]
                last = output[-1]

        input_toks = model_data["tokenizer"].encode(prompt).tokens
        output_toks = model_data["tokenizer"].encode(output[-1][len(prompt) :]).tokens
        log(model_name, len(input_toks), len(output_toks))
    else:
        raise ValueError(f"Invalid backend for {model_name}")
