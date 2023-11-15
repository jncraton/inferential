# Contributor

## Introduction to Packages

Flask

Flask is a python package that is used to build lightweight web applications using the Python programming language, as well as using HTML, JavaScript, and CSS. In this project, flask is used to host the web application locally on a server. In addition, flask is also used to create the API used for running inference.![Flask Documentation](https://pypi.org/project/Flask/)

```python
>>> from flask import Flask

>>> app = Flask(__name__)

>>> @app.route("/")
>>> def hello_world():
        return "<p>Hello, World!</p>"
```

Ctranslate2

Ctranslate2 us a C++ and Python Library that helps run efficient inference with transformer models. This package is used for running inference on compatible modles found in the ![Ctranslate2](https://github.com/OpenNMT/CTranslate2) Documentation

CTransformers

CTransformers is another Python library used for running inference on supported large language models. The difference between this and Ctranslate2 is CTransformers runs the encoding of tokens and decoding of tokens on the backend. ![Ctransformers](https://github.com/marella/ctransformers)

```python
>>> from ctransformers import AutoModelForCausalLM

>>> llm = AutoModelForCausalLM.from_pretrained("marella/gpt-2-ggml", model_file="ggml-model.bin")

>>> for text in llm("Ai is going to", stream=True):
       print(text, end="", flush=True)
```

## Setup and Installation

Requirements for installation:

- Must have git installed ![Git Install](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Must have python version 3.11 installed ![Python Install](https://www.python.org/downloads/)
- Must have x(This will change depending on the models) RAM available

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

Ctrl click on the url, should look something like this "http://127.0.0.1:5000"

Now you can start running inference using the different models selected

## Running Tests

If you are interested in changing and creating a PR, here is how you can run tests locally

```sh
pytest test_main.py
```

If this does not work here is the alternative

```sh
python -m pytest
```
