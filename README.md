Inferential
===========

Inferential is a web application that houses several large language models to run inference locally

--Example of inference

This project helps those at a beginner programming level understand the fundamentals of large language models, tokenization, and API's. This web application follows an encoder-decoder format where a query is sent to the API where it will encode the query into tokens, generate a response in tokens, and then decode those tokens into readable text. For more information on this model [https://arxiv.org/pdf/1706.03762.pdf]

Introduction to Packages
------------------------

Flask

Flask is a python package that is used to build lightweight web applications using the Python programming language, as well as using HTML, JavaScript, and CSS. In this project, flask is used to host the web application locally on a server. In addition, flask is also used to create the API used for running inference.[https://pypi.org/project/Flask/]

```python
>>> from flask import Flask

>>> app = Flask(__name__)

>>> @app.route("/")
>>> def hello_world():
        return "<p>Hello, World!</p>"
```

Ctranslate2

Ctranslate2 us a C++ and Python Library that helps run efficient inference with transformer models. This package is used for running inference on compatible modles found in the Ctranslate2 Documentation[https://github.com/OpenNMT/CTranslate2]

```python
# Download tokenizer, model config, and vocabulary
>>> hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "config.json")
>>> hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "shared_vocabulary.txt")
>>> tok_config = hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "tokenizer.json")
>>> model_path = hf_hub_download("jncraton/LaMini-Flan-T5-248M-ct2-int8", "model.bin")

#Encode the query(input)
>>> input_tokens = tokenizer.encode(input).tokens
 # Translate the tokens
>>> results = model.generate_tokens(input_tokens,disable_unk=True)

#Stream the tokens
>>> accumlated_results = []
>>> current_length = 0
>>> for item in results:
        if item.is_last:
            break
        accumlated_results.append(item.token_id)
        decoded_string = tokenizer.decode(accumlated_results)
        new_text = decoded_string[current_length - len(decoded_string) :]
        current_length = len(decoded_string)
        yield new_text
```

CTransformers

CTransformers is another Python library used for running inference on supported large language models. The difference between this and Ctranslate2 is CTransformers runs the encoding of tokens and decoding of tokens on the backend. [https://github.com/marella/ctransformers]

```python
>>> from ctransformers import AutoModelForCausalLM

>>> llm = AutoModelForCausalLM.from_pretrained("marella/gpt-2-ggml", model_file="ggml-model.bin")

>>> for text in llm("Ai is going to", stream=True):
       print(text, end="", flush=True)
```

Setup and Installation
----------------------

Requirements for installation:
   * Must have git installed [https://git-scm.com/book/en/v2/Getting-Started-Installing-Git]
   * Must have python version 3.11 installed [https://www.python.org/downloads/]
   * Must have x(This will change depending on the models) RAM available

Install requirements.txt after

```sh
pip install requirements.txt
```

If pip install does not work here is the alternative

```sh
python -m pip install requirements.txt
```

After everything is installed, now you can run the command to turn on the server

```sh
flask run
```

If this does not work here is the alternative

```sh
python -m flask run
```

Ctrl click on the url, should look something like this "https://0.0.0.0"

Now you can start running inference using the different models selected
