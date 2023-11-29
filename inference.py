import os
from tokenizers import Tokenizer
import ctranslate2
from ctransformers import AutoModelForCausalLM
from huggingface_hub import snapshot_download


def download_llms(config_models, models, models_status):
    for model in config_models:
        name = model["name"]
        print(f"Loading model {name}")
        if model["backend"] == "ctransformers":
            models[name] = {
                "backend": "ctransformers",
                "auto-model": AutoModelForCausalLM.from_pretrained(name),
            }
        elif model["backend"] == "ctranslate2":
            # Download the model (ctranslate2)
            model_path = snapshot_download(repo_id=name)
            models[name] = {"backend": "ctranslate2", "model-path": model_path}
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


def generate_response_ctranslate2(prompt, model_folder):
    # Tokenize the input
    tokenizer = Tokenizer.from_file(os.path.join(model_folder, "tokenizer.json"))
    input_tokens = tokenizer.encode(prompt).tokens

    model_base_path = model_folder

    # Initialize the translator
    model = ctranslate2.Translator(model_base_path, compute_type="int8")

    # Translate the tokens
    results = model.generate_tokens(input_tokens, disable_unk=True)

    accumlated_results = []
    current_length = 0
    for item in results:
        if item.is_last:
            break
        accumlated_results.append(item.token_id)
        decoded_string = tokenizer.decode(accumlated_results)
        new_text = decoded_string[current_length - len(decoded_string) :]
        current_length = len(decoded_string)
        yield new_text


def generate_response_ctransformers(prompt, model):
    for text in model(prompt, stream=True):
        yield text
