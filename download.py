from ctransformers import AutoModelForCausalLM
from huggingface_hub import hf_hub_download, snapshot_download
from ctransformers import AutoModelForCausalLM
import yaml


with open("config.yml", "r") as f:
    config_root = yaml.safe_load(f)
    config_models = config_root["models"]


def download_llms():
    for model in config_models: #For each model in the config index 
        if model["backend"] == "ctransformers":
            AutoModelForCausalLM.from_pretrained(model["name"]) #These all download to the hub
        elif model["backend"] == "ctranslate2":
            #Download the model (ctranslate2)
            snapshot_download(repo_id=model["name"]) #These all download to the hub
            hf_hub_download(model["name"], "tokenizer.json") #These all download to the hub
        else:
            raise ValueError("Download failed! Invalid backend for model " + model["name"])
