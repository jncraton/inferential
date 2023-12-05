# Contributor

## Introduction to Packages

### Flask

Flask is a python package that is used to build lightweight web applications using the Python programming language, as well as using HTML, JavaScript, and CSS. In this project, flask is used to host the web application locally on a server. In addition, flask is also used to create the API used for running inference.[Flask Documentation](https://pypi.org/project/Flask/)

```python
>>> from flask import Flask

>>> app = Flask(__name__)

>>> @app.route("/")
>>> def hello_world():
        return "<p>Hello, World!</p>"
```

### Ctranslate2

Ctranslate2 us a C++ and Python Library that helps run efficient inference with transformer models. This package is used for running inference on compatible modles found in the [Ctranslate2](https://github.com/OpenNMT/CTranslate2) Documentation

### CTransformers

CTransformers is another Python library used for running inference on supported large language models. The difference between this and Ctranslate2 is CTransformers runs the encoding of tokens and decoding of tokens on the backend.[Ctransformers](https://github.com/marella/ctransformers)

```python
>>> from ctransformers import AutoModelForCausalLM

>>> llm = AutoModelForCausalLM.from_pretrained("marella/gpt-2-ggml", model_file="ggml-model.bin")

>>> for text in llm("Ai is going to", stream=True):
       print(text, end="", flush=True)
```

## Setup virtual environment

If you need a virtual environment use these commands this may be needed if you are on a mac.

Open your terminal

We will use homebrew to install the newest version of python.

```sh
$ brew install python
```

To verify the successful installation of the Python 3.x version, run the "python3" command, and the IDLE should start in your terminal.

To create the virtual environment type

```sh
python3 -m venv my_env
```

This will create a virtual environment for you with the following files in the virtual environment directory my_env:

- bin
- include
- lib
- pip-selfcheck.json
- pyvenv.cfg

To activate the virtual environment, run the following command:

```sh
source my_env/bin/activate
```

This will start the virtual environment and you should see the name of the virtual environment added before the directory name.

After you succesfully run the previous, your terminal should look similar to this

```sh
(myenv) filepath@filepath-MacBook ~ %
```

Now you can install anything in it, by running the "pip3 install" command, for example to install the requests module, run the following command:

```sh
pip3 install requests
```

To get out of the virtual environment, run the "exit" command.

### Requirements for installation:

- Must have git installed [Git Install](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Must have python version 3.11 installed [Python Install](https://www.python.org/downloads/)
- Must have x(This will change depending on the models) RAM available

Install requirements.txt after

```sh
pip install requirements.txt
```

If pip install does not work here is the alternative

```sh
python -m pip install requirements.txt
```

If you use python3

```sh
pip3 install requirements.txt
```

Install Pytest-Playwright

```sh
pip install pytest-playwright
```

If pip install does not work here is the alternative

```sh
python -m pip install pytest-playwright
```

If you use python3

```sh
pip3 install pytest pytest-playwright
```

Install the required browers

```sh
playwright install
```

Installing Pytest

```sh
pip install -U pytest
```

If pip install does not work here is the alternative

```sh
python -m pip install -U pytest
```

Here is the python3 alternative

```sh
pip3 install -U pytest
```

After everything is installed, now you can run the command to turn on the server

```sh
flask run
```

If this does not work here is the alternative

```sh
python -m flask run
```

If you use python3

```sh
python3 flask run
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

If you use python3

```sh
python3 pytest
```

## Error Codes

| Error Code | Message              |
| ---------- | -------------------- |
| 400        | Bad Request          |
| 413        | Content was to large |

## Add your Own Changes

If you wish to contribute to Inferential:

In your command line type

```sh
git checkout -b "Branch Name"
```

Make desired changes to the files.

To add changes to GitHub, use the following commands:

```sh
git add .
```

```sh
git commit -a -m "Commit Message"
```

```sh
git push --set-upstream origin BranchName
```

```sh
git push -a
```

## API Endpoints

### /api

This endpoint is where the inference and model selection is done. Data from the frontend is passed as a query parameter where the endpoint expects a value called input and models. From here it uses decision logic to figure out which model has been selected. This information gets passed to a function where the return value is a query. This query gets returned to the frontend as plaintext.

### /api/status

This endpoint returns a python dictionary featuring all of the models and the corresponding status if each model. The current download state of the model is represented by a boolean value.

## Set Inferential Web App Logo

### How Logo Gets Generated

In the config file, there is a the statr of a python dictionary called logo and it features a relative file path that calls a logo in the /logos/default.png. In app.py, two routes call a the logo dictionary from the config file.

### Steps to change logo

1.) Go into the [/logos](https://github.com/jncraton/inferential/tree/main/static/logos) folder and add your image

2.) In the [config file](https://github.com/jncraton/inferential/blob/main/config.yml) change the path of the logo to your new image

3.) Run the application and see the new logo
